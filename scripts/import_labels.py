import logging
import os
import sys
from pathlib import Path

import yaml
from github import Github, GithubException

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(message)s")

# Load GitHub token
token = os.getenv("GITHUB_TOKEN")
if not token:
    logger.error("GITHUB_TOKEN not set")
    sys.exit(1)

# Initialize GitHub client
g = Github(token)

# Get repo
repo = g.get_repo("TEC-The-ELidoras-Codex/luminai-genesis")

# Load labels from YAML
with Path(".github/labels.yml").open(encoding="utf-8") as f:
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
        logger.info("Updated label: %s", name)
    except GithubException as exc:
        logger.debug("Label update failed for %s: %s", name, exc, exc_info=exc)
        # Create if not exists
        repo.create_label(name, color, description)
        logger.info("Created label: %s", name)

logger.info("Labels imported successfully")
