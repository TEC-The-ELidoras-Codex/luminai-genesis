# Hosting the Privacy Policy (Quick Guide)

If you need a publicly accessible privacy policy URL for LinkedIn app creation (or other OAuth apps), here are two simple options using GitHub and Cloudflare (you already own `elidorascodex.com` with Cloudflare):

Option 1 — GitHub Pages (fast, free):

1. Commit this repository's `docs/privacy-policy.md` or an HTML copy into the `docs/` folder.
2. Enable GitHub Pages for this repository using the `docs/` folder in repository settings. Choose `docs/` as the source.
3. GitHub provides a URL like `https://<user>.github.io/<repo>/privacy-policy.html` or `https://<user>.github.io/<repo>/` depending on your repo and settings.
4. (Optional) Use Cloudflare to map `https://elidorascodex.com/privacy` to the GitHub Pages site by adding a `CNAME` or use a redirect rule.

Option 2 — Cloudflare Pages (recommended if using Cloudflare):

1. In Cloudflare Pages, create a new site and connect this repo.
2. Configure the build to publish the `docs/` directory, or copy `privacy-policy.md` to a small static HTML file in a public directory.
3. Add the custom domain `elidorascodex.com` to the Pages site and update Cloudflare-managed DNS records to point to the site.
4. Ensure the privacy page is visible at `https://elidorascodex.com/privacy` or `https://privacy.elidorascodex.com`.

Option 3 — Upload to an existing origin (if you host a site already):

1. Add `privacy-policy.html` to your existing web root.
2. Place at `https://elidorascodex.com/privacy` and make sure the page is accessible.

LinkedIn app requirements summary:

- Privacy Policy URL (publicly accessible): required.
- Redirect URI (publicly accessible): required for OAuth flows.
- Both URLs must use HTTPS.

Bluesky handle/domain claim:

- Bluesky will provide a value to put in DNS to verify the domain.
- If you're using a custom domain with Substack, Substack helps to set up the necessary records; if you're not using Substack’s paid domain mapping, you can still map your domain to Cloudflare Pages or GitHub Pages to host a privacy policy or to claim your Bluesky handle.

Notes:

- You do NOT need to purchase a Substack custom domain to create a LinkedIn app or to host a privacy policy page. GitHub Pages or Cloudflare Pages are free alternatives.
- For the RSS feed workflows: the scripts will still use the Substack feed (https://polkin.substack.com/feed) and you don't need a custom domain for them to run.

If you'd like, I can add a `privacy-policy.html` (static) that will be ready to host in `docs/` and a sample Cloudflare DNS record example for you to paste to your Cloudflare DNS settings.
