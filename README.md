# tanren (redirects only)

The app Tanren was renamed to **Tagane** on 2026-11-24, and its website moved from
`https://lkmcelik.github.io/tanren/` to **https://lkmcelik.github.io/tagane/** (repo `lkmcelik/tagane`).

GitHub Pages doesn't redirect a renamed project site, so this repo keeps the old addresses working: every old page
sends the visitor to the same page under `/tagane/`, and `404.html` does the same for any other path. The pages carry
`noindex` and a canonical link to the new address.

Regenerate after pages are added to the site: `python3 tools/make_redirects.py <path to the site repo>`.
