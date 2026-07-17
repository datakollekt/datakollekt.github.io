# datakollekt.se

The website for **DataKollekt AB** — the Stockholm engineering consultancy of Pooya Shahryari.

- **Live:** https://datakollekt.se (HTTPS enforced)
- **www:** https://www.datakollekt.se redirects to the apex
- **Hosting:** GitHub Pages, served from `main` at the repo root

It is a single, self-contained static page (`index.html`) — no build server, no framework runtime to host. The visual design is produced in a design tool and exported as one standalone HTML file; a small local build step layers SEO/structured data on top before deploy.

## Repository layout

| File | Purpose |
|------|---------|
| `index.html` | The whole site: one self-contained page (styles, scripts, fonts, and images inlined). |
| `CNAME` | Custom domain for GitHub Pages (`datakollekt.se`). |
| `robots.txt` | Crawl rules — all search engines and AI crawlers allowed; points to the sitemap. |
| `sitemap.xml` | Sitemap listing the single page. |
| `og-image.png` | 1200×630 branded social preview card (`og:image`). |
| `pooya-shahryari-cv.pdf` | Public CV — a redacted copy (see below). |
| `.nojekyll` | Serve all files as-is (no Jekyll processing). |
| `build/` | Reproducible build scripts (see below). |

## Domain & DNS

DNS is managed in **Cloudflare**. The apex domain (`datakollekt.se`) is the canonical address; `www` redirects to it (handled automatically by GitHub Pages).

Records for the website (all **DNS-only / grey-cloud**, so GitHub can issue and serve HTTPS):

| Type | Name | Value |
|------|------|-------|
| A | `@` | `185.199.108.153` |
| A | `@` | `185.199.109.153` |
| A | `@` | `185.199.110.153` |
| A | `@` | `185.199.111.153` |
| CNAME | `www` | `datakollekt.github.io` |

Notes:
- **Apex is canonical by design** — it's shorter and cleaner. Using the bare domain does **not** limit subdomains: any `*.datakollekt.se` subdomain can be added independently for other services, without affecting the main site.
- **Email is separate.** The domain's `MX` and DKIM `TXT` records (Google Workspace) are untouched by the website setup.
- **HTTPS** is provisioned by GitHub Pages (Let's Encrypt) and enforced.

## Deploy

GitHub Pages rebuilds automatically on every push to `main`; no CI is required. A change is live within a minute or two of pushing.

Because the site is a single static file, browser/CDN caching is aggressive — after a deploy, hard-refresh (`Cmd/Ctrl+Shift+R`) or use a private window to see changes immediately.

## Updating the site

The visual source lives in the design tool (exported as a standalone HTML bundle). To publish an update:

1. **Edit the design** in the design tool and export a fresh **standalone HTML** file.
2. **Apply the SEO layer** to the export (adds `<title>`/description, canonical, Open Graph + Twitter tags, `lang`, JSON-LD structured data, and a `<noscript>` content mirror for non-JS crawlers):
   ```sh
   python build/seo-inject.py index.html
   ```
   (Run it on the exported file, saved as `index.html`.)
3. **Commit & push** `index.html` to `main`.

The SEO layer is applied *on top of* each export, so it must be re-run after every re-export. `build/seo-inject.py` is idempotent — it skips if the layer is already present.

### SEO / AI-search layer

`build/seo-inject.py` injects, into the raw HTML so crawlers read it without executing JavaScript:

- **Meta**: title, description, canonical, `robots`, Open Graph, Twitter Card, `og:image`, `lang="en"`, theme-color.
- **Structured data (JSON-LD)**: `ProfessionalService` (DataKollekt AB), `Person` (Pooya Shahryari — role, skills, languages, `sameAs` links), and `WebSite`.
- **`<noscript>` content mirror**: a plain-HTML rendering of the page's real content (headline, services, work, founder, contact), so AI crawlers and link scrapers that don't run JavaScript index the actual content.

Plus `robots.txt` (all crawlers, incl. AI, allowed) and `sitemap.xml`.

### Social preview card

`build/generate-og-image.py` renders the 1200×630 `og-image.png` (brand-matched: dark ground, cyan accent, wordmark, hero tagline). Requires Pillow.

```sh
python build/generate-og-image.py og-image.png
```

### The CV

`pooya-shahryari-cv.pdf` is a **redacted** copy of the private consultant CV, produced with `build/redact-cv.py`. The published version removes the hourly rate, phone number, and availability date, and drops the personal "work week" chart page. The private source PDF is kept locally and is **not** committed; redaction terms are passed at runtime (see the script header) so no private values live in this repo.
