#!/usr/bin/env python3
import os
from pathlib import Path

import yaml
from github import Github
from github.GithubException import UnknownObjectException

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
p = Path(".github/labels.yml")
with p.open(encoding="utf-8") as f:
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
    except UnknownObjectException:
        # Create if not exists
        repo.create_label(name, color, description)
        print(f"Created label: {name}")

print("Labels imported successfully")
