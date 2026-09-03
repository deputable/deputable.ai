# Deputable AI - website

Plain HTML/CSS/JS site, no build step. Six static pages sharing `css/style.css` and `js/main.js`:

- `index.html` - Home
- `services.html` - What We Do (includes the interactive workflow demo)
- `how-it-works.html` - process/timeline
- `about.html` - company, sectors, founders
- `trust.html` - trust & security Q&A
- `contact.html` - demo request form (currently front-end only, see below)

## Run locally

No build tools needed. From this folder:

```
python3 -m http.server 8000
```

then open `http://localhost:8000`.

## Deploy to GitHub Pages with the deputable.ai domain

1. Push this folder to a GitHub repo (e.g. `deputable-ai/website`), with these files at the **repo root**.
2. In the repo, go to **Settings → Pages**. Under "Build and deployment", set **Source** to `Deploy from a branch`, branch `main`, folder `/ (root)`.
3. The `CNAME` file already contains `deputable.ai`, so GitHub Pages will pick it up automatically once Pages is enabled.
4. At your domain registrar, point `deputable.ai` at GitHub Pages:
   - Add an `A` record for the apex domain (`@`) to GitHub's four Pages IPs:
     `185.199.108.153`, `185.199.109.153`, `185.199.110.153`, `185.199.111.153`
   - (Optional) add a `CNAME` record for `www` → `<your-github-username>.github.io`
5. Back in **Settings → Pages**, once DNS has propagated, tick **Enforce HTTPS**.

`.nojekyll` is included so GitHub Pages serves the files as-is without running them through Jekyll.

## Things still marked as placeholders in the content

- Home and About pages have a "drop image here" placeholder where a real team/workshop photo and founder portraits should go.
- Founder bios on the About page are drafts - LinkedIn details need confirming.
- Trust & Security answers are drafted and flagged for sign-off before publishing (certifications, DPA wording).
- The contact form (`contact.html`) currently just shows a confirmation message on submit - it isn't wired to send anywhere yet. Easiest options: point the `<form>` at a service like Formspree, or add a small serverless function / GitHub Pages-compatible form handler.

## Editing content

There's no CMS or templating at runtime - each page is a self-contained HTML file. If you're making the same change across all six pages (e.g. nav wording, footer), it's easiest to edit `/tmp`-style via a regenerate script rather than by hand; ask Claude to regenerate from the shared source if you have it, or just edit the repeated header/footer markup in each file.
