# Deploying `docs/` to elidorascodex.com with GitHub Pages + Cloudflare

This repository already contains a `docs/` folder with our site content including a privacy policy (`docs/privacy-policy.md`) and our legal privacy policy (`docs/legal/privacy_policy.md`). The repository also includes an automated workflow to deploy the `docs/` folder to the `gh-pages` branch on pushes to `main`.

Quick checklist to make the privacy policy available at https://elidorascodex.com:

1. Verify the site builds locally:

```bash
python -m http.server --directory docs 8000
# Visit http://localhost:8000 and confirm the privacy pages are present
```

2. Confirm `docs/CNAME` contains your domain:

```bash
cat docs/CNAME
# should print: elidorascodex.com
```

3. Push changes to `main` to trigger the action (or trigger the action manually under the repo Actions tab). The action `Deploy docs to GitHub Pages` will publish the site to `gh-pages` branch.

4. Configure GitHub Pages (Admin required):

   - In GitHub repo Settings > Pages, set the Source to `gh-pages` branch (root). The site should show a URL like `https://<owner>.github.io/<repo>/` and your custom domain `elidorascodex.com` (if the CNAME file is present).
   - If GitHub asks to set HTTPS (Enable 'Enforce HTTPS.') allow it; the certificate may take a few minutes to configure.

5. Configure Cloudflare DNS:

   - Add DNS records for your domain:
     - For apex domain `elidorascodex.com`, add A records pointing to GitHub Pages IP addresses (recommended):
       - 185.199.108.153
       - 185.199.109.153
       - 185.199.110.153
       - 185.199.111.153
     - Alternatively, you can use a CNAME for `www` that points to `<owner>.github.io` and create a CNAME flattening rule at the apex.
   - Important: Disable Cloudflare proxy (turn off orange cloud; make zone DNS-only) while GitHub issues SSL certificates to avoid conflicts. After Pages shows HTTPS enabled, you can optionally re-enable proxy.

6. Wait for TLS cert to issue (GitHub Pages + Let's Encrypt); once issued you can open https://elidorascodex.com and verify the privacy policy is accessible.

7. Use the privacy policy URL in LinkedIn app as the app privacy policy link. It should be a stable HTTPS URL like `https://elidorascodex.com/privacy-policy/` or `https://elidorascodex.com/legal/privacy_policy.html` depending on full paths (verify the generated HTML paths after the Pages build completes).

Notes:

- If you prefer using Cloudflare Pages (not GitHub Pages), enable the Cloudflare Pages integration and use the existing `docs/` folder as the source; verify the domain and enable automatic deployments.
- Once your Pages site publishes and HTTPS is validated, LinkedIn and Bluesky will accept the privacy URL.
