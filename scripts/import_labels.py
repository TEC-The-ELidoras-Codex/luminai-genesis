import os

import yaml
from github import Github

# Load GitHub token
token = os.getenv("GITHUB_TOKEN")
if not token:
    print("GITHUB_TOKEN not set")
    exit(1)

# Initialize GitHub client
g = Github(token)

# Get repo
repo = g.get_repo("TEC-The-ELidoras-Codex/luminai-genesis")

# Load labels from YAML
with open(".github/labels.yml") as f:
    labels_data = yaml.safe_load(f)

# Import labels
for label in labels_data:
    name = label["name"]
    color = label["color"]
    description = label.get("description", "")

    try:
        # Check if label exists
        existing = repo.get_label(name)
        # Update if exists
        existing.edit(name, color, description)
        print(f"Updated label: {name}")
    except Exception:
        # Create if not exists
        repo.create_label(name, color, description)
        print(f"Created label: {name}")

print("Labels imported successfully")
