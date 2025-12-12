Ready Memos for WordPress

Place markdown files with YAML frontmatter into this folder. Fields supported:

- `title`, `slug`, `date`, `author`, `orcid`, `channels`: include `wordpress` to build an HTML file for WP.

Build HTML for WordPress:

```bash
python3 scripts/aqueduct_build_wordpress_html.py
# result -> dist/wordpress/*.html
```

Tip: For images and assets referenced by posts, ensure they are uploaded to WordPress or use absolute URLs accessible from the public web.
