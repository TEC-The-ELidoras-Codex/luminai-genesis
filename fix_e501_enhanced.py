#!/usr/bin/env python3
"""Fix E501 line length violations in TEC scripts"""

import re
import textwrap
from pathlib import Path


def fix_file(filepath):
    """Fix line length violations in a Python file"""
    with open(filepath) as f:
        lines = f.readlines()

    new_lines = []
    i = 0

    while i < len(lines):
        line = lines[i]
        stripped = line.rstrip()

        # Skip if already under limit
        if len(stripped) <= 88:
            new_lines.append(line)
            i += 1
            continue

        indent = " " * (len(line) - len(line.lstrip()))

        # Fix case 1: Long "user": "..." strings
        match = re.search(r'"user":\s*"([^"]+)"', line)
        if match:
            user_text = match.group(1)
            # Split at natural sentence boundaries
            wrapped = textwrap.fill(
                user_text,
                width=80,
                break_long_words=False,
                break_on_hyphens=False,
            )
            # Rejoin as multiline string
            wrapped_lines = wrapped.split("\n")
            formatted = f'{indent}"user": (\n'
            for j, wline in enumerate(wrapped_lines):
                formatted += f'{indent}    "{wline}"'
                if j < len(wrapped_lines) - 1:
                    formatted += " "
                formatted += "\n"
            formatted += f"{indent}),"
            new_lines.append(formatted + "\n")
            i += 1
            continue

        # Fix case 2: Long template strings in triple quotes
        if '"""' in line or "'''" in line:
            # Keep as-is for docstrings (they're templates)
            new_lines.append(line)
            i += 1
            continue

        # Fix case 3: Long string literals
        string_match = re.search(r'(".*?")', line)
        if string_match and len(string_match.group(1)) > 80:
            string_content = string_match.group(1)[1:-1]  # Remove quotes
            # Split into multiple concatenated strings
            parts = textwrap.wrap(string_content, width=75)
            replacement = "(\n"
            for j, part in enumerate(parts):
                replacement += f'{indent}    "{part}"'
                if j < len(parts) - 1:
                    replacement += " "
                replacement += "\n"
            replacement += f"{indent})"
            new_line = line.replace(string_match.group(1), replacement)
            new_lines.append(new_line)
            i += 1
            continue

        # Fix case 4: Long function calls - split at commas
        if "(" in line and "," in line:
            # Find function call and split arguments
            match = re.match(r"(\s*)(\w+)\((.*)\)", line)
            if match:
                indent_str = match.group(1)
                func_name = match.group(2)
                args = match.group(3)

                # Split arguments
                arg_list = [a.strip() for a in args.split(",")]
                new_line = f"{indent_str}{func_name}(\n"
                for j, arg in enumerate(arg_list):
                    new_line += f"{indent_str}    {arg}"
                    if j < len(arg_list) - 1:
                        new_line += ","
                    new_line += "\n"
                new_line += f"{indent_str})\n"
                new_lines.append(new_line)
                i += 1
                continue

        # Fallback: Insert line continuation
        if len(stripped) > 88:
            new_lines.append(f"{stripped[:85]} \\\n")
            new_lines.append(f"{indent}    {stripped[85:]}\n")
        else:
            new_lines.append(line)

        i += 1

    with open(filepath, "w") as f:
        f.writelines(new_lines)

    print(f"✅ Fixed: {filepath}")


# Run fixes
REPO_ROOT = Path("/home/elidoras-codex/luminai-genesis")

files_to_fix = [
    REPO_ROOT / "scripts" / "generate_training_data.py",
    REPO_ROOT / "scripts" / "sanitize_codex_dump.py",
    REPO_ROOT / "scripts" / "run_combat_demo.py",
]

for filepath in files_to_fix:
    if filepath.exists():
        fix_file(filepath)
    else:
        print(f"⚠️  Not found: {filepath}")

print("\n✅ All E501 fixes applied!")
print("Run: ruff check --select E501 scripts/ to verify")
