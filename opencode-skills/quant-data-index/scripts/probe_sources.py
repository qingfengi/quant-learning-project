"""Probe the built-in public data sources with the Python standard library."""

import argparse
import json
import math
import sys
import time
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from http.client import HTTPException
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener


MAX_RESPONSE_BYTES = 2 * 1024 * 1024
USER_AGENT = "quant-data-index/1.0 (public research samples)"
SOURCES = {
    "gate-spot": ("crypto", "https://api.gateio.ws/api/v4/spot/candlesticks"),
    "gate-futures": ("crypto", "https://api.gateio.ws/api/v4/futures/usdt/candlesticks"),
    "binance": ("crypto", "https://api.binance.com/api/v3/klines"),
    "arxiv": ("papers", "https://export.arxiv.org/api/query"),
    "crossref": ("papers", "https://api.crossref.org/works"),
}
ATOM = "{http://www.w3.org/2005/Atom}"


def positive_timeout(value):
    try:
        result = float(value)
    except (TypeError, ValueError):
        raise argparse.ArgumentTypeError("timeout must be a number") from None
    if not math.isfinite(result) or not 0 < result <= 60:
        raise argparse.ArgumentTypeError("timeout must be greater than 0 and at most 60 seconds")
    return result


def sample_limit(value):
    try:
        result = int(value)
    except (TypeError, ValueError):
        raise argparse.ArgumentTypeError("limit must be an integer") from None
    if not 1 <= result <= 100:
        raise argparse.ArgumentTypeError("limit must be between 1 and 100")
    return result


def source_url(source, limit=5, query="quantitative trading"):
    if source not in SOURCES:
        raise ValueError("unknown source")
    sample_limit(limit)
    if not isinstance(query, str) or not query.strip() or len(query) > 500:
        raise ValueError("query must contain 1 to 500 characters")
    if source == "gate-spot":
        params = {"currency_pair": "BTC_USDT", "interval": "1d", "limit": limit}
    elif source == "gate-futures":
        params = {"contract": "BTC_USDT", "interval": "1d", "limit": limit}
    elif source == "binance":
        params = {"symbol": "BTCUSDT", "interval": "1d", "limit": limit}
    elif source == "arxiv":
        params = {"search_query": "all:" + query.strip(), "start": 0, "max_results": limit}
    else:
        params = {"query": query.strip(), "rows": limit}
    return SOURCES[source][1] + "?" + urlencode(params)


class PublicRedirectHandler(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        target = urlsplit(newurl)
        if (target.scheme != "https" or target.hostname != urlsplit(req.full_url).hostname
                or target.username or target.password or target.port not in (None, 443)):
            raise ValueError("refused redirect outside the source HTTPS host")
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def read_public(url, timeout):
    positive_timeout(timeout)
    request = Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json, application/atom+xml"})
    with build_opener(PublicRedirectHandler()).open(request, timeout=timeout) as response:
        if response.status != 200:
            raise ValueError("expected HTTP 200")
        body = response.read(MAX_RESPONSE_BYTES + 1)
        if not body:
            raise ValueError("empty response body")
        if len(body) > MAX_RESPONSE_BYTES:
            raise ValueError("response exceeds the 2 MiB sample limit")
        return body


def number(value, *, positive=False):
    if isinstance(value, bool) or not isinstance(value, (int, float, str)):
        raise ValueError("invalid numeric field")
    try:
        parsed = Decimal(str(value))
    except InvalidOperation:
        raise ValueError("invalid numeric field") from None
    if not parsed.is_finite() or parsed < 0 or (positive and parsed == 0):
        raise ValueError("numeric field must be finite and non-negative; prices must be positive")
    return str(value)


def candle(timestamp, opening, high, low, close, volume, unit, divisor=1):
    timestamp_text = number(timestamp)
    stamp = Decimal(timestamp_text)
    if stamp != stamp.to_integral_value():
        raise ValueError("timestamp must be an integer")
    try:
        opened = datetime.fromtimestamp(float(stamp / divisor), timezone.utc).isoformat()
    except (OverflowError, OSError, ValueError):
        raise ValueError("timestamp is outside the supported date range") from None
    prices = [number(item, positive=True) for item in (opening, high, low, close)]
    o, h, l, c = map(Decimal, prices)
    if not l <= min(o, c) <= max(o, c) <= h:
        raise ValueError("candle high/low do not contain open/close")
    return dict(open_time=opened, open=prices[0], high=prices[1], low=prices[2],
                close=prices[3], volume=number(volume), volume_unit=unit)


def text_field(value):
    if not isinstance(value, str) or not value.strip():
        raise ValueError("missing text field")
    return " ".join(value.split())


def parse_records(source, body):
    if source == "arxiv":
        document = body.decode("utf-8-sig")
        if "<!DOCTYPE" in document.upper() or "<!ENTITY" in document.upper():
            raise ValueError("XML declarations with entities are not accepted")
        root = ET.fromstring(document)
        if root.tag != ATOM + "feed":
            raise ValueError("expected an Atom feed")
        records = []
        for entry in root.findall(ATOM + "entry"):
            identifier = text_field(entry.findtext(ATOM + "id"))
            if "/api/errors" in identifier:
                raise ValueError("arXiv returned an API error entry")
            records.append({
                "id": identifier,
                "title": text_field(entry.findtext(ATOM + "title")),
                "published": text_field(entry.findtext(ATOM + "published")),
                "summary": text_field(entry.findtext(ATOM + "summary")),
                "authors": [text_field(author.findtext(ATOM + "name"))
                            for author in entry.findall(ATOM + "author")],
            })
        return records

    data = json.loads(body)
    if source == "crossref":
        if (not isinstance(data, dict) or data.get("status") != "ok"
                or data.get("message-type") != "work-list"
                or not isinstance(data.get("message"), dict)
                or not isinstance(data["message"].get("items"), list)):
            raise ValueError("expected a successful Crossref work-list response")
        records = []
        for item in data["message"]["items"]:
            if not isinstance(item, dict) or not isinstance(item.get("title"), list) or not item["title"]:
                raise ValueError("missing Crossref work title")
            records.append({"doi": text_field(item.get("DOI")), "title": text_field(item["title"][0]),
                            "url": text_field(item.get("URL"))})
        return records

    if source not in ("gate-spot", "gate-futures", "binance"):
        raise ValueError("unknown source")
    if not isinstance(data, list) or not data:
        raise ValueError("expected a non-empty candle list")
    records = []
    for row in data:
        if source == "gate-futures":
            if not isinstance(row, dict) or not all(key in row for key in ("t", "o", "h", "l", "c", "v")):
                raise ValueError("missing Gate futures candle fields")
            record = candle(row["t"], row["o"], row["h"], row["l"], row["c"], row["v"], "contracts")
        elif source == "gate-spot":
            if not isinstance(row, list) or len(row) < 6:
                raise ValueError("missing Gate spot candle fields")
            record = candle(row[0], row[5], row[3], row[4], row[2], row[1], "USDT")
        else:
            if not isinstance(row, list) or len(row) < 6:
                raise ValueError("missing Binance candle fields")
            record = candle(row[0], row[1], row[2], row[3], row[4], row[5], "BTC", divisor=1000)
        records.append(record)
    records.sort(key=lambda item: item["open_time"])
    if len({item["open_time"] for item in records}) != len(records):
        raise ValueError("duplicate candle timestamps")
    return records


def fetch_sample(source, *, limit=5, query="quantitative trading", timeout=15):
    url = source_url(source, limit, query)
    records = parse_records(source, read_public(url, timeout))
    if len(records) > limit:
        raise ValueError("source returned more records than requested")
    return {"source": source, "url": url, "fetched_at": datetime.now(timezone.utc).isoformat(),
            "count": len(records), "records": records}


def failure_message(error):
    if isinstance(error, HTTPError):
        return "HTTP %s (source access or rate limit)" % error.code
    if isinstance(error, (TimeoutError, URLError)):
        return "network or TLS request failed (%s)" % type(error).__name__
    if isinstance(error, (json.JSONDecodeError, ET.ParseError, UnicodeError)):
        return "response could not be parsed as the expected format"
    if isinstance(error, ValueError):
        # Parse errors never echo response bodies or supplied query text.
        return str(error)
    return "request failed (%s)" % type(error).__name__


def write_json(path, document):
    destination = Path(path)
    encoded = json.dumps(document, ensure_ascii=False, indent=2, allow_nan=False) + "\n"
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("x", encoding="utf-8", newline="\n") as handle:
        handle.write(encoded)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    selection = parser.add_mutually_exclusive_group(required=True)
    selection.add_argument("--group", choices=("crypto", "papers"))
    selection.add_argument("--source", choices=tuple(SOURCES))
    selection.add_argument("--all", action="store_true", help="probe all five built-in samples, not every reference URL")
    selection.add_argument("--list", action="store_true", help="list supported sources without network requests")
    parser.add_argument("--timeout", type=positive_timeout, default=15)
    parser.add_argument("--output", type=Path, help="optional new JSON report file; existing files are never overwritten")
    args = parser.parse_args(argv)
    if args.list:
        print(json.dumps({name: {"group": group, "endpoint": url}
                          for name, (group, url) in SOURCES.items()}, indent=2))
        return 0
    if args.output and args.output.exists():
        parser.error("output already exists; choose a new file")
    selected = [name for name, (group, _) in SOURCES.items()
                if args.all or name == args.source or group == args.group]
    results = []
    for index, source in enumerate(selected):
        if index:
            time.sleep(3 if selected[index - 1] == "arxiv" else 0.25)
        started = time.monotonic()
        result = {"source": source, "url": source_url(source, limit=1)}
        try:
            sample = fetch_sample(source, limit=1, timeout=args.timeout)
            if sample["count"] == 0:
                raise ValueError("probe query returned no sample records")
            result.update(ok=True, count=sample["count"])
        except (OSError, ValueError, ET.ParseError, HTTPException) as error:
            result.update(ok=False, error=failure_message(error))
        result["elapsed_seconds"] = round(time.monotonic() - started, 3)
        results.append(result)
    report = {"checked_at": datetime.now(timezone.utc).isoformat(), "results": results}
    if args.output:
        try:
            write_json(args.output, report)
        except OSError as error:
            print("Could not write report (%s)." % type(error).__name__, file=sys.stderr)
            return 1
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if all(item["ok"] for item in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
