# Privacy Policy

Last updated: 2025-12-12

This Privacy Policy explains how The Elidoras Codex ("we", "us", "our") collects, uses, and shares information when you visit our website or use our services (including LinkedIn / WordPress automation scripts described in the repository).

If you have questions about this policy or would like to request a copy of the data we collect about you, please contact us: polkin@substack.com

---

## Information We Collect

- Content you submit: this includes posts, comments, messages, and any media (images, audio) you provide. When we publish or re-post content on third-party services (WordPress, LinkedIn), it is processed only to create the post.
- Analytics: IP address, user-agent, timestamps, and request logs recorded by our hosting and action providers.
- Email addresses and other contact details that users share when subscribing or contacting us.

## How We Use Your Data

- Publish content: We use content submitted by the author to create posts and updates that may be posted to WordPress, LinkedIn, and other third-party services as configured by the repository's automation.
- Improve services and debug issues: to troubleshoot and debug automation workflows and services that interact with third-party APIs.
- Communicate with subscribers and handle requests: for email lists and notifications when you subscribe.

## Third Party Services & Data Sharing

We use third-party APIs and services (Substack, WordPress, GitHub, LinkedIn, Discord) to publish, share, and notify about content. Your content can be posted or shared on those services as part of the configured automation.

We do not sell personal information. We may share data with service providers to operate the site and services (e.g., Substack for publication, GitHub Actions for automation, OlLama/other AI for processing) under contract and security standards.

## Cookies & Tracking

We use cookies or tracking technologies deployed by third-party platforms (Substack, LinkedIn, WordPress, etc.) according to their privacy policies. This repository does not itself set site-level cookies unless hosted as a site.

## Security

We take reasonable safeguards to protect data but cannot guarantee absolute security. Sensitive credentials (API keys, tokens, passwords) should never be stored in the repository; store them in GitHub Actions repository secrets or other secure vaults.

## Hosting a Privacy Policy for LinkedIn App

LinkedIn requires a public, accessible `Privacy Policy` URL when registering an app. You can host this policy anywhere with a public URL:

- **Option 1 (fast, no cost)** — create a published Substack post or page titled "Privacy Policy" and add that URL to your LinkedIn app settings. This is free and doesn't need a custom domain.
- **Option 2 (free)** — use GitHub Pages: add `docs/PRIVACY_POLICY.md` to this repository and enable GitHub Pages with `docs/` as the source; the policy URL will then be `https://<github-username>.github.io/<repo>/PRIVACY_POLICY.html`.
- **Option 3 (optional)** — purchase domain and host policy at `https://yourdomain.com/privacy` or host on Netlify/Vercel/GitHub Pages.

## Additional Notes on LinkedIn App

For LinkedIn developer app creation you will typically need:

- A public `Privacy Policy` URL.
- A `Website URL` — this can be your Substack site (e.g., `https://polkin.substack.com`) or your GitHub Pages site.
- Redirect URIs for OAuth if you are using OAuth flows for app integration.

LinkedIn sometimes asks for more details for production access. During development, many APIs work using the `Development` stage after you create an app and configure redirect URIs, a website URL, and a privacy policy. You can use your Substack site for the required `Website URL`.

## Contact Us

If you have questions about this policy or wish to exercise your data rights, contact: polkin@substack.com

---

If you want, I can: 1) add this privacy policy to your Substack as a public page (requires Substack access), 2) add a `docs/` GitHub Page with a ready-to-serve HTML page, or 3) create a minimal GitHub Pages workflow that publishes the `docs/` site automatically.
