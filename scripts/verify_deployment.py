"""Post-deployment check: public HTML and first-party assets match this commit.

Usage: python scripts/verify_deployment.py --url https://example.github.io/site/
"""
import argparse
import hashlib
from html.parser import HTMLParser
from pathlib import Path
import time
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]


class Assets(HTMLParser):
    def __init__(self):
        super().__init__()
        self.paths = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        path = a.get("src") if tag == "script" else a.get("href") if tag == "link" else None
        if path and path.split("?", 1)[0] in (
            "assets/app.js", "assets/data.js", "assets/styles.css"
        ):
            self.paths.append(path)


def fetch(url):
    req = Request(url, headers={"User-Agent": "DantasCozinha-DeployVerification/1.0", "Cache-Control": "no-cache"})
    with urlopen(req, timeout=20) as response:
        if response.status != 200:
            raise RuntimeError(f"HTTP {response.status}: {url}")
        return response.read()


def verify(url):
    local_html = (ROOT / "index.html").read_bytes()
    local = Assets()
    local.feed(local_html.decode("utf-8"))
    if len(local.paths) != 3 or len(set(local.paths)) != 3:
        raise RuntimeError("index.html must reference the three versioned first-party assets")
    remote_html = fetch(url)
    remote = Assets()
    remote.feed(remote_html.decode("utf-8"))
    if set(local.paths) != set(remote.paths):
        raise RuntimeError(f"Published asset versions do not match: {remote.paths!r}")
    for asset in local.paths:
        relative = asset.split("?", 1)[0]
        expected = (ROOT / relative).read_bytes()
        actual = fetch(urljoin(url, asset))
        if hashlib.sha256(actual).digest() != hashlib.sha256(expected).digest():
            raise RuntimeError(f"Published asset differs from this commit: {relative}")
    print("PASS: public HTML references current assets; all three match this commit")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True)
    parser.add_argument("--attempts", type=int, default=8)
    parser.add_argument("--delay", type=int, default=10)
    args = parser.parse_args()
    if urlparse(args.url).scheme != "https":
        parser.error("--url must use HTTPS")
    for attempt in range(1, args.attempts + 1):
        try:
            verify(args.url)
            return
        except Exception as exc:
            print(f"Attempt {attempt}/{args.attempts}: {exc}", flush=True)
            if attempt == args.attempts:
                raise SystemExit(1) from exc
            time.sleep(args.delay)


if __name__ == "__main__":
    main()
