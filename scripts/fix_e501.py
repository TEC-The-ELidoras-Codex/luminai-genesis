#!/usr/bin/env python3
import re
import textwrap
from pathlib import Path

# Config
MAX_LINE_LEN = 88
USER_WRAP_THRESHOLD = 60
TEMPLATE_LINE_BREAK_THRESHOLD = 120
SPLIT_CHUNK_WIDTH = 80


def fix_file(filepath):
    p = Path(filepath)
    with p.open() as f:
        lines = f.readlines()

    new_lines = []

    for line in lines:
        stripped = line.rstrip()
        if len(stripped) > MAX_LINE_LEN:
            # Check for "user": "long string"
            match = re.search(r'"user": "([^"]*)"', line)
            if match:
                user_text = match.group(1)
                if len(user_text) > USER_WRAP_THRESHOLD:  # More aggressive wrapping
                    wrapped = textwrap.wrap(user_text, width=50)
                    new_user = '"\n            "'.join(wrapped) + '"'
                    indent = " " * (len(line) - len(line.lstrip()))
                    new_line = line.replace(
                        f'"user": "{user_text}"', f'"user": {new_user}',
                    )
                    new_lines.append(new_line)
                    continue
            # Handle other long lines by splitting at natural breaks
            if '"""' in line and len(line) > TEMPLATE_LINE_BREAK_THRESHOLD:
                # Split long template strings
                if "," in line and line.count(",") > 1:
                    parts = line.split(", ")
                    current = ""
                    indent = " " * (len(line) - len(line.lstrip()))
                    for i, part in enumerate(parts):
                        if len(current + part) > SPLIT_CHUNK_WIDTH:
                            if current:
                                new_lines.append(current.rstrip() + "\n")
                            current = indent + part
                            if i < len(parts) - 1:
                                current += ", "
                        else:
                            current += part
                            if i < len(parts) - 1:
                                current += ", "
                    if current:
                        new_lines.append(current.rstrip() + "\n")
                    continue
        new_lines.append(line)

    with p.open("w", encoding="utf-8") as f:
        f.writelines(new_lines)


fix_file("/home/elidoras-codex/luminai-genesis/scripts/generate_training_data.py")

fix_file("/home/elidoras-codex/luminai-genesis/scripts/sanitize_codex_dump.py")
