# Ground Line Tree & Stump

Static website for Houston tree trimming, tree removal, and stump grinding.
Business contact: **(832) 501-9594**.

## Run locally

```sh
python3 -m http.server 8765 --directory dist
```

Open http://localhost:8765. No dependency installation or build is required.

## Check

```sh
python3 scripts/check_site.py
node --check dist/app.js
```

The site check validates internal links and fragments, assets, canonical URLs,
sitemap coverage, structured-data JSON, page titles, and primary headings.

## Files

- `dist/index.html`: homepage and estimate request form.
- `dist/stump-grinding-houston/index.html`: stump grinding service page.
- `dist/tree-removal-houston/index.html`: tree removal service page.
- `dist/tree-trimming-houston/index.html`: tree trimming service page.
- `dist/service-areas/index.html`: Greater Houston community directory and coverage inquiry guide.
- `dist/styles.css` and `dist/app.js`: shared presentation and interactions.
- `dist/robots.txt` and `dist/sitemap.xml`: crawler discovery files.
- `.openai/hosting.json`: existing Sites project identity and static hosting directory.

Edit the HTML directly. Keep shared navigation, contact details, and form behavior
consistent across all five pages. No third-party tracking is installed.

## Estimate requests

The form prepares an SMS addressed to the business. It does not send or store a
lead on a server. Customers must review and send the message in their messaging
app. The copy option supports desktop visitors. Do not imply that submitting the
form has contacted the business.

## Publishing and SEO

Existing website: https://ground-line-tree-stump.sunset-tune-1548.chatgpt.site

This GitHub repository stores the website source. A GitHub push does not by itself
deploy to Sites; publish through the Sites workflow using the retained project ID.
The deployed site must allow public access before search engines can crawl it.
Confirm its audience in Sites before changing access.

When moving to a custom domain, update the canonical URL, Open Graph URL,
structured-data URLs, robots sitemap URL, and all sitemap entries together.
After public launch, verify the site in Google Search Console and submit
`/sitemap.xml`. These files do not automatically verify or submit the site.

Organization and Service structured data use the confirmed business name,
telephone number, and Houston service area. Do not add an unverified address,
ratings, certifications, opening hours, or personal owner details.
The hero artwork is illustrative generated imagery, not a completed-job photo.
