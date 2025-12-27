"""
TEC Wall of Names - Export carved names to text
"""

import json
from datetime import datetime
from pathlib import Path


def load_carved_names(save_file: Path) -> list[str]:
    """Load names from character save"""
    if not save_file.exists():
        return []

    with open(save_file) as f:
        data = json.load(f)
        return data.get("carved_names", [])


def export_wall(names: list[str], output: Path):
    """Export wall as formatted text"""
    with open(output, "w", encoding="utf-8") as f:
        f.write("╔═══════════════════════════════════════════╗\n")
        f.write("  THE WALL OF NAMES - THE ELIDORAS CODEX\n")
        f.write("╚═══════════════════════════════════════════╝\n\n")
        f.write(f"Generated: {datetime.now().isoformat()}\n")
        f.write(f"Total Names: {len(names)}\n\n")
        f.write("─" * 47 + "\n\n")

        f.writelines(f"{i:3d}. {name}\n" for i, name in enumerate(names, 1))

        f.write("\n" + "─" * 47 + "\n")
        f.write("\nNOT FORGOTTEN\n")


if __name__ == "__main__":
    print("=== WALL OF NAMES EXPORTER ===\n")

    # Example usage
    names = ["Timothy Sol Weeran", "Marcus Thane", "Elara Kess"]

    output = Path("wall_of_names.txt")
    export_wall(names, output)
    print(f"✅ Exported {len(names)} names to {output}")
