---
title: "WordPress Site Fixes & Improvements"
slug: wp-site-fix
date: 2025-12-11
author: Angelo Hurley
channels: [wordpress]
---

This is a quick site-improvement checklist and plan for improving the LuminAI/Angelo Hurley WordPress site.

### Quick Wins

- Improve navigation — add a "Publications" page linking to papers and created posts.
- Add an "Author" page with ORCID and short bio: include `https://orcid.org/0009-0000-7615-6990`.
- Replace theme-mounted CSS with a responsive theme and add a child theme for custom overrides.
- Add `robots.txt` and OpenGraph meta for better sharing, and set `rel=canonical` for canonical pages.

### Performance & Security

- Use caching (WP Super Cache or FastCGI caching) and optimize images (WebP for modern browsers).
- Add HTTPS enforcement and secure the admin panel (2FA + strong passwords).
- Limit plugin usage; disable/replace any heavy or insecure plugins.

### Publishing Workflows

- Use `aqueduct_build_wordpress_html.py` to generate Gutenberg-ready HTML from repository content and a GitHub webhook plugin to automatically import new posts.
- Maintain a `docs/streams/articles/ready` folder with `channels: [wordpress]` frontmatter and the published HTML items in `dist/wordpress`.

### Next Steps

- Create a dedicated "Papers" page and upload the TGCR PDF and demo resources.
- Review theme for accessibility and ARIA compliance.

If you'd like, I can:

1. Generate a WordPress post for TGCR (the HTML is under `dist/wordpress/tgcr.html`)
2. Create a child theme and a starter `functions.php` snippet for custom fields
3. Create CI that auto-imports `dist/wordpress/*.html` to your WordPress site using the existing webhook plugin

Which of these should I prioritize next?
