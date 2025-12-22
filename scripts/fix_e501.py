import re
import textwrap


def fix_file(filepath):
    with open(filepath) as f:
        lines = f.readlines()

    new_lines = []

    for line in lines:
        stripped = line.rstrip()
        if len(stripped) > 88:
            # Check for "user": "long string"
            match = re.search(r'"user": "([^"]*)"', line)
            if match:
                user_text = match.group(1)
                if len(user_text) > 60:  # More aggressive wrapping
                    wrapped = textwrap.wrap(user_text, width=50)
                    new_user = '"\n            "'.join(wrapped) + '"'
                    indent = " " * (len(line) - len(line.lstrip()))
                    new_line = line.replace(
                        f'"user": "{user_text}"', f'"user": {new_user}',
                    )
                    new_lines.append(new_line)
                    continue
            # Handle other long lines by splitting at natural breaks
            if '"""' in line and len(line) > 120:
                # Split long template strings
                if "," in line and line.count(",") > 1:
                    parts = line.split(", ")
                    current = ""
                    indent = " " * (len(line) - len(line.lstrip()))
                    for i, part in enumerate(parts):
                        if len(current + part) > 80:
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

    with open(filepath, "w") as f:
        f.writelines(new_lines)


fix_file("/home/elidoras-codex/luminai-genesis/scripts/generate_training_data.py")

fix_file("/home/elidoras-codex/luminai-genesis/scripts/sanitize_codex_dump.py")
