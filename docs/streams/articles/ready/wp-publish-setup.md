WordPress Publishing Setup (CI + Secrets)

This document describes how to configure the GitHub Action `wp-publish.yml` to automatically import `dist/wordpress/*.html` into your WordPress site.

1. Create an application password in WordPress

- Login to the WP admin as the user you'd like to publish as (e.g., `admin`)
- Profile -> Application Passwords -> Add New Application Password
- Copy the generated password; treat it as a secret

2. Create GitHub Secrets

- In your repo: Settings -> Secrets and variables -> Actions -> New repository secret
- Add: `WP_BASE_URL` (e.g. `https://your-site.com`)
- Add: `WP_USER` (the WP username that owns the app password)
- Add: `WP_APP_PASSWORD` (the app password generated earlier)

3. Enable access to the REST API

- No additional plugins are needed for the WordPress REST API if on WordPress 5.x or later, but ensure your site is accessible from the GitHub Action runner.

4. Add images/media and PDF linking

- The script `scripts/wp_publish.py` attempts to find images referenced in the HTML and uploads them. It will also attempt to upload `papers/<slug>/<slug>.pdf`.

5. Dry-run first

- You can test the workflow locally by running `python3 scripts/wp_publish.py --dir dist/wordpress --base-url https://example.com --user admin --password secret --dry-run`

Frontmatter metadata support
---------------------------------
The build script `scripts/aqueduct_build_wordpress_html.py` embeds the original Markdown frontmatter as JSON in the generated HTML. The publishing script parses this data and uses the `category` (or `categories`) and `tags` fields if present. Example frontmatter in `docs/streams/articles/ready/tgcr.md`:

```yaml
title: tgcr
slug: tgcr
date: 2025-12-11
author: Angelo Hurley
orcid: https://orcid.org/0009-0000-7615-6990
channels: [wordpress]
tags: [TGCR, consciousness, physics, AI]
category: Papers
```

If `--category` or `--tags` are passed as arguments to `scripts/wp_publish.py` they take precedence over frontmatter.

6. Optional: Secure the publish flow via a whitelist of IPs or GitHub Actions runner verification.

7. Hook the webhook plugin (optional)

- The repo includes a simple webhook receiver under `infrastructure/wp-github-webhook` that can accept GitHub webhooks and pull content or run a sync process. Use if your WP host supports uploading plugin files and running PHP scripts.

8. Troubleshooting

- If the script fails with 404 on /wp-json/, make sure the site is reachable and doesn't have JSON REST disabled.
- If the script returns 401: verify the WP_USER and WP_APP_PASSWORD are correct and that the app password is assigned to that user.

  ## PHP validation in VS Code

  If you see the VS Code error:

  > Cannot validate since a PHP installation could not be found. Use the setting 'php.validate.executablePath' to configure the PHP executable.

  Install PHP CLI (Ubuntu/Debian):

  ```bash
  sudo apt update
  sudo apt install -y php-cli php-xml php-curl php-mbstring
  ```

  Then set the workspace VS Code setting (add to `.vscode/settings.json`):

  ```json
  "php.validate.executablePath": "/usr/bin/php",
  "php.validate.run": "onSave"
  ```

  Reload VS Code to apply the setting.
