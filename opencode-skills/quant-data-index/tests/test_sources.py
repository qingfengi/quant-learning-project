import argparse
import contextlib
import io
import json
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
from http.client import IncompleteRead
from pathlib import Path
from unittest.mock import Mock, patch
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qs, urlsplit
from urllib.request import Request

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import fetch_examples
import probe_sources as sources


def encoded(value):
    return json.dumps(value).encode()


SPOT = [["1700000000", "20.50", "65000", "66000", "63000", "64000", "0.001", "true"]]
FUTURES = [{"t": 1700000000, "v": 12, "o": "64000", "h": "66000", "l": "63000", "c": "65000"}]
BINANCE = [[1700000000000, "64000", "66000", "63000", "65000", "0.001"]]
CROSSREF = {"status": "ok", "message-type": "work-list", "message": {
    "items": [{"DOI": "10.0000/example", "title": ["Sample research"], "URL": "https://doi.org/10.0000/example"}]}}
ARXIV = b'''<feed xmlns="http://www.w3.org/2005/Atom"><entry>
    <id>https://arxiv.org/abs/0000.00000</id><title>Sample research</title>
    <published>2024-01-01T00:00:00Z</published><summary>Research summary</summary>
    <author><name>Example Author</name></author></entry></feed>'''


class SourceTests(unittest.TestCase):
    def test_all_source_requests_are_public_https(self):
        for source in sources.SOURCES:
            with self.subTest(source=source):
                parsed = urlsplit(sources.source_url(source))
                self.assertEqual(parsed.scheme, "https")
                self.assertIsNone(parsed.username)
                self.assertFalse({"key", "api_key", "token", "signature"} & parse_qs(parsed.query).keys())

    def test_query_is_encoded(self):
        params = parse_qs(urlsplit(sources.source_url("arxiv", 2, "BTC & risk")).query)
        self.assertEqual(params["search_query"], ["all:BTC & risk"])
        self.assertEqual(params["max_results"], ["2"])

    def test_timeout_bounds(self):
        for value in ("0", "-1", "nan", "inf", "61", "wrong"):
            with self.subTest(value=value), self.assertRaises(argparse.ArgumentTypeError):
                sources.positive_timeout(value)

    def test_limit_bounds(self):
        for value in ("0", "-1", "101", "1.5", "wrong"):
            with self.subTest(value=value), self.assertRaises(argparse.ArgumentTypeError):
                sources.sample_limit(value)

    def test_invalid_query_and_unknown_source(self):
        for source, query in (("missing", "test"), ("arxiv", "  "), ("crossref", "a" * 501)):
            with self.subTest(source=source), self.assertRaises(ValueError):
                sources.source_url(source, query=query)

    def test_valid_candles_keep_units_and_exact_decimal_text(self):
        for source, fixture, unit in (("gate-spot", SPOT, "USDT"), ("gate-futures", FUTURES, "contracts"),
                                     ("binance", BINANCE, "BTC")):
            with self.subTest(source=source):
                result = sources.parse_records(source, encoded(fixture))[0]
                self.assertEqual(result["volume_unit"], unit)
                self.assertEqual(result["open_time"], "2023-11-14T22:13:20+00:00")
                self.assertEqual(result["close"], "65000")
        self.assertEqual(sources.parse_records("gate-spot", encoded(SPOT))[0]["volume"], "20.50")

    def test_invalid_candles_and_business_errors(self):
        cases = [[], {}, {"label": "INVALID_PARAM"}, [[1, 2]], [{"t": 1}]]
        for value in cases:
            for source in ("gate-spot", "gate-futures", "binance"):
                with self.subTest(source=source, value=value), self.assertRaises(ValueError):
                    sources.parse_records(source, encoded(value))

    def test_invalid_financial_numbers(self):
        for value in ("NaN", "Infinity", "-1", True, None, [], "invalid"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                sources.number(value)

    def test_invalid_price_range_and_timestamp(self):
        for timestamp, high, low in (("1.5", "3", "1"), ("1e100", "3", "1"),
                                     (1, "1", "3"), (1, "0", "0")):
            with self.subTest(timestamp=timestamp), self.assertRaises(ValueError):
                sources.candle(timestamp, "2", high, low, "2", "0", "BTC")

    def test_candles_are_sorted_and_duplicates_rejected(self):
        later = [*SPOT[0]]
        later[0] = "1700000001"
        result = sources.parse_records("gate-spot", encoded([later, SPOT[0]]))
        self.assertLess(result[0]["open_time"], result[1]["open_time"])
        with self.assertRaisesRegex(ValueError, "duplicate"):
            sources.parse_records("gate-spot", encoded(SPOT + SPOT))

    def test_crossref_success_empty_and_error(self):
        self.assertEqual(sources.parse_records("crossref", encoded(CROSSREF))[0]["title"], "Sample research")
        empty = {"status": "ok", "message-type": "work-list", "message": {"items": []}}
        self.assertEqual(sources.parse_records("crossref", encoded(empty)), [])
        for value in ({"status": "failed"}, {"status": "ok", "message-type": "work-list", "message": {"items": [{}]}}):
            with self.subTest(value=value), self.assertRaises(ValueError):
                sources.parse_records("crossref", encoded(value))

    def test_arxiv_success_and_empty(self):
        result = sources.parse_records("arxiv", ARXIV)
        self.assertEqual(result[0]["authors"], ["Example Author"])
        self.assertEqual(sources.parse_records("arxiv", b'<feed xmlns="http://www.w3.org/2005/Atom"/>'), [])

    def test_arxiv_error_html_and_entities_rejected(self):
        for body in (b"<html>blocked</html>", b'<!DOCTYPE feed><feed/>',
                     '<!DOCTYPE feed [<!ENTITY title "example">]><feed/>'.encode("utf-16"),
                     ARXIV.replace(b"https://arxiv.org/abs/0000.00000", b"http://arxiv.org/api/errors")):
            with self.subTest(body=body), self.assertRaises(ValueError):
                sources.parse_records("arxiv", body)

    def test_invalid_json_and_xml(self):
        with self.assertRaises(json.JSONDecodeError):
            sources.parse_records("gate-spot", b"<html>blocked</html>")
        with self.assertRaises(ET.ParseError):
            sources.parse_records("arxiv", b"not XML")

    def test_response_size_status_and_empty_body(self):
        for status, body in ((200, b""), (200, b"a" * (sources.MAX_RESPONSE_BYTES + 1)), (204, b"ok")):
            response = Mock(status=status)
            response.read.return_value = body
            opener = Mock()
            opener.open.return_value.__enter__ = Mock(return_value=response)
            opener.open.return_value.__exit__ = Mock(return_value=False)
            with self.subTest(status=status, length=len(body)), patch.object(sources, "build_opener", return_value=opener):
                with self.assertRaises(ValueError):
                    sources.read_public(sources.source_url("gate-spot"), 1)

    def test_redirects_stay_on_source_https_host(self):
        handler = sources.PublicRedirectHandler()
        request = Request("https://export.arxiv.org/api/query")
        for target in ("http://export.arxiv.org/api/query", "https://localhost/", "https://other.example/",
                       "https://user:pass@export.arxiv.org/api/query", "https://export.arxiv.org:444/api/query"):
            with self.subTest(target=target), self.assertRaises(ValueError):
                handler.redirect_request(request, None, 302, "Found", {}, target)
        redirected = handler.redirect_request(request, None, 302, "Found", {}, "https://export.arxiv.org/api/query?x=1")
        self.assertEqual(urlsplit(redirected.full_url).hostname, "export.arxiv.org")

    def test_network_error_output_does_not_echo_server_text(self):
        for error in (HTTPError("https://example.com/private", 429, "private payload", {}, None),
                      URLError("private payload"), TimeoutError("private payload")):
            with self.subTest(error=type(error).__name__):
                self.assertNotIn("private", sources.failure_message(error))

    def test_fetch_sample_validates_response_count(self):
        with patch.object(sources, "read_public", return_value=encoded(SPOT)):
            result = sources.fetch_sample("gate-spot", limit=1)
            self.assertEqual(result["count"], 1)
        with patch.object(sources, "parse_records", return_value=[{}, {}]), patch.object(sources, "read_public", return_value=b"[]"):
            with self.assertRaisesRegex(ValueError, "more records"):
                sources.fetch_sample("gate-spot", limit=1)

    def test_write_does_not_overwrite_existing_file(self):
        with tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parent) as directory:
            destination = Path(directory) / "output" / "sample.json"
            sources.write_json(destination, {"value": 1})
            with self.assertRaises(FileExistsError):
                sources.write_json(destination, {"value": 2})
            self.assertEqual(json.loads(destination.read_text()), {"value": 1})


class CliTests(unittest.TestCase):
    def setUp(self):
        self.stack = contextlib.ExitStack()
        self.addCleanup(self.stack.close)
        self.stack.enter_context(contextlib.redirect_stdout(io.StringIO()))
        self.stderr = self.stack.enter_context(contextlib.redirect_stderr(io.StringIO()))

    def test_list_needs_no_network(self):
        with patch.object(sources, "fetch_sample") as fetch:
            self.assertEqual(sources.main(["--list"]), 0)
            fetch.assert_not_called()

    def test_probe_failure_does_not_stop_other_sources(self):
        with (patch.object(sources, "fetch_sample", side_effect=[TimeoutError(), {"count": 1}, {"count": 1}]) as fetch,
              patch.object(sources.time, "sleep")):
            self.assertEqual(sources.main(["--group", "crypto"]), 1)
            self.assertEqual(fetch.call_count, 3)

    def test_probe_empty_search_is_a_failure(self):
        with patch.object(sources, "fetch_sample", return_value={"count": 0}):
            self.assertEqual(sources.main(["--source", "arxiv"]), 1)

    def test_probe_all_success_and_report(self):
        with tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parent) as directory:
            destination = Path(directory) / "probe.json"
            with patch.object(sources, "fetch_sample", return_value={"count": 1}), patch.object(sources.time, "sleep"):
                self.assertEqual(sources.main(["--all", "--output", str(destination)]), 0)
            self.assertEqual(len(json.loads(destination.read_text())["results"]), 5)

    def test_explicit_selection_source_and_output_required(self):
        for main, args in ((sources.main, []), (sources.main, ["--all", "--group", "crypto"]),
                           (fetch_examples.main, ["--source", "gate-spot"]), (fetch_examples.main, ["--output", "sample.json"])):
            with self.subTest(args=args), self.assertRaises(SystemExit) as result:
                main(args)
            self.assertEqual(result.exception.code, 2)

    def test_fetch_existing_output_checked_before_network(self):
        with patch.object(fetch_examples, "fetch_sample") as fetch, self.assertRaises(SystemExit):
            fetch_examples.main(["--source", "gate-spot", "--output", __file__])
        fetch.assert_not_called()

    def test_failed_fetch_creates_no_output(self):
        with tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parent) as directory:
            destination = Path(directory) / "sample.json"
            with patch.object(fetch_examples, "fetch_sample", side_effect=URLError("test")):
                self.assertEqual(fetch_examples.main(["--source", "gate-spot", "--output", str(destination)]), 1)
            self.assertFalse(destination.exists())

    def test_incomplete_http_body_is_reported_without_output(self):
        with tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parent) as directory:
            destination = Path(directory) / "sample.json"
            with patch.object(fetch_examples, "fetch_sample", side_effect=IncompleteRead(b"private text")):
                self.assertEqual(fetch_examples.main(["--source", "gate-spot", "--output", str(destination)]), 1)
            self.assertFalse(destination.exists())
            self.assertNotIn("private text", self.stderr.getvalue())

    def test_fetch_success_writes_json(self):
        with tempfile.TemporaryDirectory(dir=Path(__file__).resolve().parent) as directory:
            destination = Path(directory) / "sample.json"
            with patch.object(fetch_examples, "fetch_sample", return_value={"count": 1, "records": [{"close": "1"}]}):
                self.assertEqual(fetch_examples.main(["--source", "gate-spot", "--output", str(destination)]), 0)
            self.assertEqual(json.loads(destination.read_text())["records"], [{"close": "1"}])


if __name__ == "__main__":
    unittest.main()
