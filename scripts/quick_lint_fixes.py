"""Quick lint fixes for low-risk issues.

Run: python scripts/quick_lint_fixes.py
"""

import re
from pathlib import Path


# 1. Remove shebangs from non-executable scripts
def remove_shebangs():
    files_to_fix = [
        "scripts/post_linkedin.py",
        "scripts/post_to_linkedin.py",
    ]

    for filepath in files_to_fix:
        path = Path(filepath)
        if not path.exists():
            continue
        content = path.read_text(encoding="utf-8")
        if content.startswith("#!/usr/bin/env python3\n"):
            content = content.replace("#!/usr/bin/env python3\n", "", 1)
            path.write_text(content, encoding="utf-8")


# 2. Fix Unicode ambiguities in a small set of files
def fix_unicode_ambiguities():
    fixes = {
        "src/tgcr_core.py": [("φ^t × ψ^r", "φ^t x ψ^r")],
        "tests/test_encoding_fixer.py": [
            (
                "text = 'This is COâ\u201a‚ at 25Â°C",
                "text = 'This is CO_2_ at 25_deg_C",
            ),
        ],
        "scripts/convert_markdown_to_pdf.py": [
            ('# "November 12th, 2347" – strip', '# "November 12th, 2347" - strip'),
        ],
    }

    for filepath, replacements in fixes.items():
        path = Path(filepath)
        if not path.exists():
            continue
        content = path.read_text(encoding="utf-8")
        original = content
        for old, new in replacements:
            content = content.replace(old, new)
        if content != original:
            path.write_text(content, encoding="utf-8")


# 3. Add HTTP constants and replace magic checks
def add_http_constants():
    # upload_to_zenodo.py
    zenodo_path = Path("scripts/publish/upload_to_zenodo.py")
    if zenodo_path.exists():
        content = zenodo_path.read_text(encoding="utf-8")
        if "HTTP_BAD_REQUEST = 400" not in content:
            insert_at = content.find("\ndef create_deposition")
            if insert_at > 0:
                constants = "\n# HTTP status constants\nHTTP_BAD_REQUEST = 400\n\n"
                content = content[:insert_at] + constants + content[insert_at:]
                content = content.replace(
                    "if r.status_code >= 400:", "if r.status_code >= HTTP_BAD_REQUEST:",
                )
                zenodo_path.write_text(content, encoding="utf-8")

    # LinkedIn helpers
    linkedin_files = [
        "scripts/linkedin_oauth_helper.py",
        "scripts/linkedin_exchange.py",
    ]
    for filepath in linkedin_files:
        path = Path(filepath)
        if not path.exists():
            continue
        content = path.read_text(encoding="utf-8")
        if "HTTP_OK = 200" not in content:
            token_url_pos = content.find("TOKEN_URL = ")
            if token_url_pos > 0:
                line_end = content.find("\n", token_url_pos)
                constants = "\n# HTTP status constants\nHTTP_OK = 200\n"
                content = content[: line_end + 1] + constants + content[line_end + 1 :]
                content = content.replace(
                    "if r.status_code != 200:", "if r.status_code != HTTP_OK:",
                )
                content = content.replace(
                    "if me.status_code != 200:", "if me.status_code != HTTP_OK:",
                )
                path.write_text(content, encoding="utf-8")


# 4. Fix redundant exception objects in logging.exception calls
def fix_logging_exception():
    files_to_fix = ["scripts/convert_markdown_to_pdf.py", "scripts/post_linkedin.py"]
    for filepath in files_to_fix:
        path = Path(filepath)
        if not path.exists():
            continue
        content = path.read_text(encoding="utf-8")
        original = content
        content = re.sub(
            r"logger\.exception\((.*?),\s*exc\s*\)", r"logger.exception(\1)", content,
        )
        # Also fix patterns that pass getattr(e,...) usage in post_linkedin
        content = content.replace(
            'logger.exception(\n            "HTTP error during LinkedIn API call. Response: %s",\n            getattr(getattr(e, "response", None), "text", "<no body>"),\n        )',
            'logger.exception("HTTP error during LinkedIn API call. Response: %s", getattr(getattr(e, "response", None), "text", "<no body>"))',
        )
        if content != original:
            path.write_text(content, encoding="utf-8")


# 5. Sanitize bundles: extract constant and fix loop shadow
def fix_sanitize_bundles():
    path = Path("scripts/sanitize_bundles.py")
    if not path.exists():
        return
    content = path.read_text(encoding="utf-8")
    if "MAX_CONSECUTIVE_BLANK_LINES = 2" not in content:
        # insert after BACKUP_SUFFIX line
        content = content.replace(
            'BACKUP_SUFFIX = datetime.now(tz=UTC).strftime("bak.%Y%m%dT%H%M%SZ")\n\nMARKERS',
            'BACKUP_SUFFIX = datetime.now(tz=UTC).strftime("bak.%Y%m%dT%H%M%SZ")\n\nMAX_CONSECUTIVE_BLANK_LINES = 2\n\nMARKERS',
        )
        content = content.replace(
            "if blank_count <= 2:", "if blank_count <= MAX_CONSECUTIVE_BLANK_LINES:",
        )
        content = content.replace(
            'line = PATH_RE.sub("[REDACTED_PATH]", line)\n        line = EMAIL_RE.sub("[REDACTED_EMAIL]", line)\n        out_lines.append(line)',
            'redacted_line = PATH_RE.sub("[REDACTED_PATH]", line)\n        redacted_line = EMAIL_RE.sub("[REDACTED_EMAIL]", redacted_line)\n        out_lines.append(redacted_line)',
        )
        path.write_text(content, encoding="utf-8")


def main():
    remove_shebangs()
    fix_unicode_ambiguities()
    add_http_constants()
    fix_logging_exception()
    fix_sanitize_bundles()


if __name__ == "__main__":
    main()
