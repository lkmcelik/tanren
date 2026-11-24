#!/usr/bin/env python3
"""Write redirect pages for the old Tanren site URLs (lkmcelik.github.io/tanren/...).

The app was renamed from Tanren to Tagane (app repository ADR-0079), and the site repo moved from lkmcelik/tanren to
lkmcelik/tagane on 2026-11-24. GitHub Pages doesn't redirect a renamed project site, so this repo (published as
lkmcelik/tanren) answers every old page with a page that sends the visitor to the same path under /tagane/.

Usage: python3 tools/make_redirects.py <path to the site repo (tanren-site)>
Writes one page per HTML file of the site (except 404.html) plus 404.html, which rewrites any other /tanren/ path.
"""
import html
import subprocess
import sys
from pathlib import Path

OLD_BASE = "/tanren/"
NEW_URL = "https://lkmcelik.github.io/tagane/"
ROOT = Path(__file__).resolve().parent.parent

PAGE = """<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Tagane</title>
<meta name="robots" content="noindex">
<link rel="canonical" href="{url}">
<meta http-equiv="refresh" content="0; url={url}">
<script>location.replace({url_js} + location.search + location.hash);</script>
<style>body{{font:16px/1.5 -apple-system,system-ui,sans-serif;margin:3rem 1rem;text-align:center;color:#1c1714;background:#f7f2ec}}a{{color:#c2410c}}</style>
</head>
<body>
<p>Tanren is now <strong>Tagane</strong>. This page moved to <a href="{url}">{url_text}</a>.</p>
</body>
</html>
"""

NOT_FOUND = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Tagane</title>
<meta name="robots" content="noindex">
<script>
  var p = location.pathname;
  var rest = p.indexOf("{old}") === 0 ? p.slice({old_len}) : "";
  location.replace("{new}" + rest + location.search + location.hash);
</script>
<style>body{{font:16px/1.5 -apple-system,system-ui,sans-serif;margin:3rem 1rem;text-align:center;color:#1c1714;background:#f7f2ec}}a{{color:#c2410c}}</style>
</head>
<body>
<p>Tanren is now <strong>Tagane</strong>. Go to <a href="{new}">{new}</a>.</p>
</body>
</html>
"""


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    site = Path(sys.argv[1])
    files = subprocess.run(["git", "-C", str(site), "ls-files", "*.html"], capture_output=True, text=True,
                           check=True).stdout.split()
    pages = [f for f in files if f != "404.html" and not f.startswith(("src/", "tools/"))]
    for rel in pages:
        target = NEW_URL + ("" if rel == "index.html" else rel.removesuffix("index.html"))
        lang = rel.split("/")[0] if "/" in rel else "en"
        out = ROOT / rel
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(PAGE.format(lang=lang, url=html.escape(target), url_js='"' + target + '"',
                                   url_text=html.escape(target)), encoding="utf-8")
    (ROOT / "404.html").write_text(NOT_FOUND.format(old=OLD_BASE, old_len=len(OLD_BASE), new=NEW_URL), encoding="utf-8")
    (ROOT / ".nojekyll").write_text("", encoding="utf-8")
    print(f"wrote {len(pages)} redirect pages and 404.html")


if __name__ == "__main__":
    main()
