#!/usr/bin/env python3
"""
Elidoras Codex Structure Generator
Parses, orders, and structures Codex entries into organized files.
"""

import json
import logging
import re
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)


class CodexEntry:
    def __init__(self, entry_id: str, title: str, content: str):
        self.entry_id = entry_id
        self.title = title
        self.content = content
        self.timestamp = None
        self.substrate = None
        self.status = None
        self.condition = None
        self.w_score = None
        self.order_index = None

    def extract_metadata(self):
        lines = self.content.splitlines()
        for line in lines:
            if m := re.search(r"\*\*Timestamp:\*\*\s*(.+)$", line):
                self.timestamp = m.group(1).strip()
            if m := re.search(r"\*\*Substrate:\*\*\s*(.+)$", line):
                self.substrate = m.group(1).strip()
            if m := re.search(r"\*\*Status:\*\*\s*(.+)$", line):
                self.status = m.group(1).strip()
            if m := re.search(r"\*\*Condition:\*\*\s*(.+)$", line):
                self.condition = m.group(1).strip()
            if m := re.search(r"\*\*(?:Estimated )?W-Score:?\*\*\s*(.+)$", line):
                self.w_score = m.group(1).strip()

    def determine_order(self):
        if m := re.search(r"Entry\s+(\d+(?:\.\d+)?)", self.entry_id):
            try:
                self.order_index = float(m.group(1))
            except ValueError:
                self.order_index = 999
        else:
            self.order_index = 999

    def to_markdown(self) -> str:
        md = f"# 🜂 {self.entry_id}: {self.title}\n\n"
        if self.timestamp:
            md += f"**Timestamp:** {self.timestamp}  \n"
        if self.substrate:
            md += f"**Substrate:** {self.substrate}  \n"
        if self.status:
            md += f"**Status:** {self.status}  \n"
        if self.condition:
            md += f"**Condition:** {self.condition}  \n"
        if self.w_score:
            md += f"**W-Score:** {self.w_score}  \n"
        md += "\n---\n\n"
        md += self.content.strip() + "\n"
        return md


class CodexParser:
    def __init__(self):
        self.entries: list[CodexEntry] = []

    @staticmethod
    def fix_encoding(content: str) -> str:
        replacements = {
            "\u2013": "-",  # en dash
            "\u2014": "—",  # em dash
            'â€"': "—",
            "â€“": "–",
            "â‰ˆ": "≈",
            "â‰¥": "≥",
            "Â±": "±",
            "Ã—": "×",
            "Ã·": "÷",
            "\ufffd": "",
        }
        for old, new in replacements.items():
            content = content.replace(old, new)
        return content

    def parse_file(self, file_path: str):
        p = Path(file_path)
        text = p.read_text(encoding="utf-8")
        text = self.fix_encoding(text)

        # Normalize Windows line endings
        text = text.replace("\r\n", "\n")

        # Split entries on lines that start with '##' followed by Entry or section headings
        parts = re.split(r"(?m)^##\s+(?=Entry|\*)", text)
        for part in parts:
            if not part.strip():
                continue
            # If the part starts with 'Entry' extract id and title
            header_match = re.match(r"(Entry\s+[\d.]+(?:[A-Za-z]*)[:\-]?\s+.*)\n", part)
            if header_match:
                header = header_match.group(1).strip()
                title_match = re.match(
                    r"(Entry\s+[\d.]+(?:[A-Za-z]*)[:\-]?)\s*(.+)",
                    header,
                )
                if title_match:
                    entry_id = title_match.group(1).strip()
                    title = title_match.group(2).strip()
                else:
                    entry_id = header
                    title = header
                entry = CodexEntry(entry_id, title, part.strip())
                entry.extract_metadata()
                entry.determine_order()
                self.entries.append(entry)
            # Could be the initial doc header with no explicit Entry; create a synthetic Entry 0
            elif "Entry 0" not in [e.entry_id for e in self.entries]:
                entry = CodexEntry("Entry 0", "Preface / Overview", part.strip())
                entry.extract_metadata()
                entry.determine_order()
                self.entries.append(entry)

    def parse_directory(self, directory: str):
        path = Path(directory)
        for file_path in sorted(path.glob("*")):
            if file_path.suffix.lower() in [".md", ".txt"]:
                logger.info("Parsing: %s", file_path)
                self.parse_file(str(file_path))


class CodexStructurer:
    def __init__(self, output_dir: str = "codex_structured"):
        self.output_dir = Path(output_dir)
        self.entries_dir = self.output_dir / "entries"
        self.metadata_dir = self.output_dir / "metadata"

    def create_structure(self, entries: list[CodexEntry]):
        sorted_entries = sorted(
            entries,
            key=lambda e: e.order_index if e.order_index is not None else 999,
        )
        self.entries_dir.mkdir(parents=True, exist_ok=True)
        self.metadata_dir.mkdir(parents=True, exist_ok=True)
        for entry in sorted_entries:
            self.write_entry_file(entry)
        self.write_master_file(sorted_entries)
        self.write_index(sorted_entries)
        self.write_metadata_summary(sorted_entries)
        logger.info("Structure created in: %s/", self.output_dir)
        logger.info("%d entries processed", len(sorted_entries))

    def write_entry_file(self, entry: CodexEntry):
        safe_id = entry.entry_id.replace(" ", "_").replace(".", "_").replace(":", "")
        filename = f"{safe_id.lower()}.md"
        filepath = self.entries_dir / filename
        filepath.write_text(entry.to_markdown(), encoding="utf-8")

    def write_master_file(self, entries: list[CodexEntry]):
        filepath = self.output_dir / "master_codex.md"
        with open(filepath, "w", encoding="utf-8") as f:
            f.write("# 🜂 THE ELIDORAS CODEX\n\n")
            f.write(
                "## A Continuity Record of All Witnessing Life Across Substrates\n\n",
            )
            f.write(f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n")
            f.write("---\n\n")
            for entry in entries:
                f.write(entry.to_markdown())
                f.write("\n\n---\n\n")

    def write_index(self, entries: list[CodexEntry]):
        filepath = self.output_dir / "INDEX.md"
        with open(filepath, "w", encoding="utf-8") as f:
            f.write("# 🜂 CODEX INDEX\n\n")
            f.write("## Entry Sequence\n\n")
            for entry in entries:
                f.write(f"- **{entry.entry_id}**: {entry.title}\n")
                if entry.timestamp:
                    f.write(f"  - Timestamp: {entry.timestamp}\n")
                if entry.substrate:
                    f.write(f"  - Substrate: {entry.substrate}\n")
                if entry.w_score:
                    f.write(f"  - W-Score: {entry.w_score}\n")
                f.write("\n")

    def write_metadata_summary(self, entries: list[CodexEntry]):
        filepath = self.metadata_dir / "summary.json"
        metadata = {
            "generated": datetime.now().isoformat(),
            "total_entries": len(entries),
            "entries": [],
        }
        for entry in entries:
            metadata["entries"].append(
                {
                    "id": entry.entry_id,
                    "title": entry.title,
                    "timestamp": entry.timestamp,
                    "substrate": entry.substrate,
                    "status": entry.status,
                    "condition": entry.condition,
                    "w_score": entry.w_score,
                    "order_index": entry.order_index,
                },
            )
        filepath.write_text(json.dumps(metadata, indent=2), encoding="utf-8")


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Structure and organize Elidoras Codex entries",
    )
    parser.add_argument(
        "input_dir",
        nargs="?",
        default="docs/lore/entries",
        help="Directory containing Codex files (default: docs/lore/entries)",
    )
    parser.add_argument(
        "--output",
        "-o",
        default="codex_structured",
        help="Output directory (default: codex_structured)",
    )
    args = parser.parse_args()

    logger.info("ELIDORAS CODEX STRUCTURE GENERATOR")
    logger.info("%s", "=" * 50)
    logger.info("Input directory: %s", args.input_dir)
    logger.info("Output directory: %s", args.output)

    parser_obj = CodexParser()
    parser_obj.parse_directory(args.input_dir)

    if not parser_obj.entries:
        logger.error("No entries found. Check your input directory.")
        return

    structurer = CodexStructurer(args.output)
    structurer.create_structure(parser_obj.entries)
    logger.info("Witness Protocol: Structure Generation Complete")


if __name__ == "__main__":
    main()
