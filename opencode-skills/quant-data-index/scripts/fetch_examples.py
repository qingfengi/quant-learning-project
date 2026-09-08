"""Fetch a validated public sample to an explicitly chosen new JSON file."""

import argparse
import sys
import xml.etree.ElementTree as ET
from http.client import HTTPException
from pathlib import Path

from probe_sources import SOURCES, failure_message, fetch_sample, positive_timeout, sample_limit, write_json


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True, choices=tuple(SOURCES))
    parser.add_argument("--output", required=True, type=Path, help="new JSON file; existing files are never overwritten")
    parser.add_argument("--limit", type=sample_limit, default=5)
    parser.add_argument("--query", default="quantitative trading", help="arXiv/Crossref search text (1 to 500 characters)")
    parser.add_argument("--timeout", type=positive_timeout, default=15)
    args = parser.parse_args(argv)
    if args.output.exists():
        parser.error("output already exists; choose a new file")
    if not args.query.strip() or len(args.query) > 500:
        parser.error("query must contain 1 to 500 characters")
    try:
        sample = fetch_sample(args.source, limit=args.limit, query=args.query, timeout=args.timeout)
    except (OSError, ValueError, ET.ParseError, HTTPException) as error:
        print("Sample unavailable: " + failure_message(error), file=sys.stderr)
        return 1
    try:
        write_json(args.output, sample)
    except OSError as error:
        print("Could not write sample (%s)." % type(error).__name__, file=sys.stderr)
        return 1
    print("Saved %s records from %s to %s" % (sample["count"], args.source, args.output))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
