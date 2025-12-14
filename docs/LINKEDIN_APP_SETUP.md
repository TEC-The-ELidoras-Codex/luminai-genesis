# LinkedIn App Setup (Minimal Checklist)

Use this page as a checklist when creating a LinkedIn developer app for automation (posting, OAuth, etc.).

Required items:

- **App name:** e.g., "Elidoras Codex Automation"
- **Website URL:** e.g., your Substack (`https://polkin.substack.com`) or GitHub Pages site (once available)
- **Privacy Policy URL:** e.g., `https://<github-username>.github.io/<repo>/PRIVACY_POLICY.html` (see `docs/PRIVACY_POLICY.md`)
- **OAuth redirect URI(s):** add a placeholder (e.g., `https://example.com/redirect`) if you do not yet use OAuth flows
- **Requested scopes:**
  - `r_liteprofile` (read basic profile)
  - `w_member_social` (post as member)

Notes:

- For development, the app can remain in "Development" mode. Production scopes require an application review by LinkedIn.
- Use the GitHub Pages URL (above) for the Website and Privacy Policy if you want everything to be hosted from this repository.
- Keep client secrets and tokens in repository secrets (Settings → Secrets) — never commit them to source.
