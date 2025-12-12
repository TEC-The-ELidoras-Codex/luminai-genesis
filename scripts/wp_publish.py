"""Publish HTML files in dist/wordpress to a WordPress site via the WP REST API.

Usage: python3 scripts/wp_publish.py --dir dist/wordpress
    --base-url https://your-wordpress-site.com --user admin
    --password "app-password"

Expected environment variables if not passed as args:
- WP_BASE_URL
- WP_USER
- WP_APP_PASSWORD

The script:
1) Scans HTML files in the given directory
2) Optionally uploads referenced images from `papers/tgcr/figures` (or same directory)
3) Creates or updates a WordPress post with title, slug, and content
4) Uploads a PDF (if present) and links it in the post

IMPORTANT: Use an application password (Basic Auth) for the user; store
credentials in GitHub secrets for CI.
"""

import argparse
import base64
import json
import logging
import os
import re
import sys
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
try:
    import requests
    from bs4 import BeautifulSoup
except Exception:
    logger.exception(
        "Missing Python dependencies: requests, beautifulsoup4. Install them with pip.",
    )
    raise



def parse_html_for_images(html, base_dir: Path):
    soup = BeautifulSoup(html, "html.parser")
    images = []
    for img in soup.find_all("img"):
        src = img.get("src")
        if not src:
            continue
        # If it's a relative path, resolve it
        if src.startswith(("http://", "https://")):
            # ignore external images for now
            continue
        # Normalize path
        file_path = (base_dir / src).resolve()
        if not file_path.exists():
            # try relative to papers/tgcr/figures
            fallback = Path("papers/tgcr/figures") / Path(src).name
            if fallback.exists():
                images.append((img, fallback))
            else:
                logger.warning("Image not found locally: %s", src)
        else:
            images.append((img, file_path))
    return soup, images


def find_pdf_for_post(slug):
    # Look for tgcr.pdf in papers/tgcr
    pdf_candidate = Path("papers") / slug / f"{slug}.pdf"
    if Path(pdf_candidate).exists():
        return pdf_candidate
    # fallback to same-named pdf in papers/<slug>
    fallback = Path("papers") / slug / f"{slug}.pdf"
    if fallback.exists():
        return fallback
    # Generic fallback for tgcr
    other = Path("papers/tgcr/tgcr.pdf")
    if other.exists():
        return other
    return None


def get_or_create_category(base_url, category_name, auth, *, dry_run=False):
    if not category_name:
        return None
    slug = re.sub(r"[^a-z0-9-]", "", category_name.lower().replace(" ", "-"))
    if dry_run:
        logger.info(
            "[DRY-RUN] Would get/create category '%s' (slug: %s)",
            category_name,
            slug,
        )
        return None
    # Query categories by slug
    url = f"{base_url.rstrip('/')}/wp-json/wp/v2/categories?slug={slug}"
    r = requests.get(url, headers=auth, timeout=10)
    r.raise_for_status()
    data = r.json()
    if data:
        return data[0]["id"]
    # Create category
    url = f"{base_url.rstrip('/')}/wp-json/wp/v2/categories"
    r = requests.post(
        url, headers=auth, json={"name": category_name, "slug": slug}, timeout=10,
    )
    r.raise_for_status()
    return r.json()["id"]


def get_or_create_tag(base_url, tag_name, auth, *, dry_run=False):
    if not tag_name:
        return None
    slug = re.sub(r"[^a-z0-9-]", "", tag_name.lower().replace(" ", "-"))
    if dry_run:
        logger.info("[DRY-RUN] Would get/create tag '%s' (slug: %s)", tag_name, slug)
        return None
    url = f"{base_url.rstrip('/')}/wp-json/wp/v2/tags?slug={slug}"
    r = requests.get(url, headers=auth, timeout=10)
    r.raise_for_status()
    data = r.json()
    if data:
        return data[0]["id"]
    url = f"{base_url.rstrip('/')}/wp-json/wp/v2/tags"
    r = requests.post(url, headers=auth, json={"name": tag_name, "slug": slug}, timeout=10)
    r.raise_for_status()
    return r.json()["id"]


def upload_images(images, args, auth):
    """Upload a list of (img_tag, file_path) tuples. Return (media_map, first_media_id)."""
    media_map = {}
    first_media_id = None
    for img_tag, file_path in images:
        logger.info("Uploading image %s", file_path)
        media_resp = upload_media(
            args.base_url, Path(file_path), auth, dry_run=args.dry_run,
        )
        if media_resp and media_resp.get("source_url"):
            media_map[file_path.name] = media_resp["source_url"]
            img_tag["src"] = media_resp["source_url"]
            if not first_media_id and media_resp.get("id"):
                first_media_id = media_resp.get("id")
    return media_map, first_media_id


def auth_header(user, app_password):
    token = base64.b64encode(f"{user}:{app_password}".encode()).decode()
    return {"Authorization": f"Basic {token}"}


def get_post_by_slug(base_url, slug, auth, *, dry_run=False):
    if dry_run:
        logger.info("[DRY-RUN] Would query for existing post with slug=%s", slug)
        return None
    url = f"{base_url.rstrip('/')}/wp-json/wp/v2/posts?slug={slug}"
    r = requests.get(url, headers=auth, timeout=10)
    r.raise_for_status()
    data = r.json()
    return data[0] if data else None


def upload_media(base_url, file_path, auth, *, dry_run=False):
    filename = Path(file_path).name
    url = f"{base_url.rstrip('/')}/wp-json/wp/v2/media"
    headers = auth.copy()
    headers.update({"Content-Disposition": f'attachment; filename="{filename}"'})
    if dry_run:
        logger.info("[DRY-RUN] Would upload media %s to %s", file_path, url)
        return {"source_url": f"{base_url.rstrip('/')}/wp-content/uploads/{filename}", "id": 0}
    with Path(file_path).open("rb") as fh:
        r = requests.post(url, headers=headers, files={"file": (filename, fh)}, timeout=30)
    try:
        r.raise_for_status()
        return r.json()
    except requests.exceptions.RequestException:
        status_code = getattr(r, "status_code", "?")
        text = getattr(r, "text", "")
        logger.exception("Failed to upload media %s: %s %s", file_path, status_code, text)
        raise


def create_or_update_post(slug, title, content, client, opts=None):
    opts = opts or {}
    status = opts.get("status", "publish")
    dry_run = opts.get("dry_run", False)
    extra_fields = opts.get("extra_fields")
    base_url = client["base_url"]
    auth = client["auth"]
    existing = get_post_by_slug(base_url, slug, auth, dry_run=dry_run)
    if existing:
        post_id = existing["id"]
        url = f"{base_url.rstrip('/')}/wp-json/wp/v2/posts/{post_id}"
        payload = {"title": title, "content": content, "status": status, "slug": slug}
        if dry_run:
            logger.info(
                "[DRY-RUN] Would update post id=%s (slug=%s) with payload: %s",
                post_id,
                slug,
                payload,
            )
            return {"link": f"{base_url.rstrip('/')}/?p={post_id}"}
        r = requests.post(url, headers=auth, json=payload, timeout=30)
        try:
            r.raise_for_status()
            return r.json()
        except requests.exceptions.RequestException:
            status_code = getattr(r, "status_code", "?")
            text = getattr(r, "text", "")
            logger.exception("Failed to update post (slug=%s): %s %s", slug, status_code, text)
            raise
    else:
        url = f"{base_url.rstrip('/')}/wp-json/wp/v2/posts"
        payload = {"title": title, "content": content, "status": status}
        excerpt_match = re.search(r"<p>(.*?)</p>", content, re.DOTALL)
        if excerpt_match:
            excerpt = re.sub(r"<[^>]+>", "", excerpt_match.group(1)).strip()
            payload["excerpt"] = excerpt[:250]
        if extra_fields:
            payload.update(extra_fields)
        if dry_run:
            logger.info(
                "[DRY-RUN] Would create post (slug=%s) with payload: %s",
                slug,
                payload,
            )
            return {"link": f"{base_url.rstrip('/')}/?s={slug}"}
        r = requests.post(url, headers=auth, json=payload, timeout=30)
        try:
            r.raise_for_status()
            return r.json()
        except requests.exceptions.RequestException:
            status_code = getattr(r, "status_code", "?")
            text = getattr(r, "text", "")
            logger.exception("Failed to create post (slug=%s): %s %s", slug, status_code, text)
            raise


def process_file(html_file: Path, args, auth):
    """Process a single HTML file: upload media, PDF, and create/update post."""
    slug = html_file.stem
    logger.info("Processing: %s (slug=%s)", html_file, slug)
    html_text = html_file.read_text(encoding="utf-8")
    # Extract frontmatter JSON embedded by the builder script (if present)
    fm = {}
    fm_match = re.search(
        r"<script[^>]+id=\"frontmatter\"[^>]*>(.*?)</script>",
        html_text,
        re.DOTALL,
    )
    if fm_match:
        try:
            fm = json.loads(fm_match.group(1))
        except json.JSONDecodeError:
            fm = {}

    soup, images = parse_html_for_images(html_text, html_file.parent)

    _media_map = {}
    first_media_id = None
    _media_map, first_media_id = upload_images(images, args, auth)
    # Now rebuild html
    final_html = str(soup)


    # Upload PDF if exists
    pdf_path = find_pdf_for_post(slug)
    if pdf_path:
        logger.info("Uploading PDF %s", pdf_path)
        pdf_media = upload_media(
            args.base_url, Path(pdf_path), auth, dry_run=args.dry_run,
        )
        pdf_url = pdf_media.get("source_url") if pdf_media else None
        if pdf_url:
            final_html = (
                f'<p><a href="{pdf_url}" target="_blank">Download full PDF</a></p>\n'
                + final_html
            )

    title_match = re.search(r"<h1[^>]*>([^<]+)</h1>", final_html)
    title = title_match.group(1) if title_match else slug

    # Create or update the post
    status = "publish" if args.publish else "draft"
    # Determine tags: CLI args override frontmatter
    tags_cli = args.tags if args.tags else None
    if not tags_cli and fm.get("tags"):
        tags_cli = (
            ",".join(fm.get("tags"))
            if isinstance(fm.get("tags"), list)
            else fm.get("tags")
        )

    extra_fields = resolve_extra_fields(args, auth, first_media_id)

    client = {"base_url": args.base_url, "auth": auth}
    post = create_or_update_post(
        slug,
        title,
        final_html,
        client,
        opts={"status": status, "dry_run": args.dry_run, "extra_fields": extra_fields},
    )
    logger.info("Post published: %s", post.get("link") if post else "unknown")


def resolve_extra_fields(args, auth, first_media_id=None):
    """Return a dict of extra fields (featured_media, categories, tags)."""
    ef = {}
    if first_media_id:
        ef["featured_media"] = first_media_id
    if args.category:
        cat_id = get_or_create_category(args.base_url, args.category, auth, dry_run=args.dry_run)
        if cat_id:
            ef["categories"] = [cat_id]
    if args.tags:
        tag_ids = []
        for t in [x.strip() for x in args.tags.split(",") if x.strip()]:
            tag_id = get_or_create_tag(args.base_url, t, auth, dry_run=args.dry_run)
            if tag_id:
                tag_ids.append(tag_id)
        if tag_ids:
            ef["tags"] = tag_ids
    return ef


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dir",
        default="dist/wordpress",
        help="Directory with HTML files (default: dist/wordpress)",
    )
    parser.add_argument(
        "--base-url",
        default=os.getenv("WP_BASE_URL"),
        help="Base URL for WordPress site, e.g., https://example.com",
    )
    parser.add_argument(
        "--user",
        default=os.getenv("WP_USER"),
        help="WordPress username",
    )
    parser.add_argument(
        "--password",
        default=os.getenv("WP_APP_PASSWORD"),
        help=(
            "WordPress application password (for Basic Auth)"
        ),
    )
    parser.add_argument(
        "--publish",
        action="store_true",
        help="Publish immediately. Otherwise posts are created as drafts.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Do not send requests to WP; print actions and payloads only.",
    )
    parser.add_argument(
        "--category",
        default=None,
        help="Optional category name to assign to the posts",
    )
    parser.add_argument(
        "--tags",
        default=None,
        help="Comma-separated tags to add to the posts",
    )
    args = parser.parse_args()

    if not args.base_url or not args.user or not args.password:
        logger.error(
            "WP_BASE_URL, WP_USER and WP_APP_PASSWORD are required (either via env vars or args)",
        )
        sys.exit(1)

    auth = auth_header(args.user, args.password)

    base_dir = Path(args.dir)
    if not base_dir.exists():
        logger.error("Directory not found: %s", base_dir)
        sys.exit(1)

    html_files = list(base_dir.glob("*.html"))
    if not html_files:
        logger.info("No HTML files found in dist/wordpress; run build script first.")
        sys.exit(0)

    for html_file in html_files:
        process_file(html_file, args, auth)


if __name__ == "__main__":
    main()
