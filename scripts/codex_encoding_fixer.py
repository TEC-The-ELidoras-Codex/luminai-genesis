#!/usr/bin/env python3
"""
Elidoras Codex Encoding Fixer
Repairs corrupted UTF-8 encoding in Codex markdown files
"""

import logging
import re
from pathlib import Path
from typing import Dict

logger = logging.getLogger(__name__)

class EncodingFixer:
    """Fixes common UTF-8 encoding corruption patterns"""

    # Practical character replacement map
    REPLACEMENTS: Dict[str, str] = {
        # Common dash variants
        'â€"': '—',  # weirdly decoded em-dash
        'â€“': '–',
        '\u2013': '–',
        '\u2014': '—',

        # Approx / inequality
        'â‰ˆ': '≈',
        'â‰¥': '≥',
        'â‰ ': '≠',

        # Multiplication and division
        'Ã—': '×',
        'ÃƒÂ—': '×',
        'Ã·': '÷',
        'ÃƒÂ·': '÷',

        # Plus-minus
        'Â±': '±',

        # Degree, micro
        'Â°': '°',
        'Âµ': 'µ',

        # Currency
        'â‚¬': '€',

        # Trademark / other
        'â„¢': '™',

        # Replacement character and mojibake sequences
        '\ufffd': '',
        'ï¿½': '',

        # Misc common sequences
        'Ã¢â‚¬â€œ': '—',
        'â€\u0093': '—',

        # Emoji mojibake -> safe fallback if seen
        'ðŸœ‚': '🜂',
        'ðŸ§¬': '🧬',
    }

    @staticmethod
    def fix_text(text: str) -> str:
        """Apply all encoding fixes to text"""
        # Normalize line endings first
        text = text.replace('\r\n', '\n')

        # Apply character replacements
        for corrupted, fixed in EncodingFixer.REPLACEMENTS.items():
            if corrupted in text:
                text = text.replace(corrupted, fixed)

        # Fix common multi-byte sequences that got split (CO2, H2O)
        text = re.sub(r'CO\s*â‚‚', 'CO₂', text)
        text = re.sub(r'H\s*â‚‚O', 'H₂O', text)

        # Fix degree Celsius/Fahrenheit
        text = text.replace('Â°C', '°C').replace('Â°F', '°F')

        # Clean up spaces around em dashes
        text = re.sub(r'\s+—\s+', ' — ', text)

        # Fix percentage/per mille
        text = text.replace('â€°', '‰')

        # Trim trailing whitespace on lines
        text = '\n'.join(line.rstrip() for line in text.splitlines())

        return text

    @staticmethod
    def fix_file(input_path: Path, output_path: Path = None, in_place: bool = False) -> bool:
        """Fix encoding in a single file"""
        if not input_path.exists():
            logger.error("File not found: %s", input_path)
            return False

        try:
            original_text = input_path.read_text(encoding='utf-8', errors='replace')
            fixed_text = EncodingFixer.fix_text(original_text)

            if in_place:
                output = input_path
            elif output_path:
                output = output_path
            else:
                output = input_path.parent / f"{input_path.stem}_fixed{input_path.suffix}"

            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(fixed_text, encoding='utf-8')

            if original_text != fixed_text:
                changes = sum(1 for a, b in zip(original_text, fixed_text) if a != b) + abs(len(original_text) - len(fixed_text))
                logger.info("Fixed %s: ~%d character changes", input_path.name, changes)
            else:
                logger.info("%s: No changes needed", input_path.name)

            return True

        except Exception as exc:
            logger.exception("Error processing %s: %s", input_path.name, exc)
            return False

    @staticmethod
    def fix_directory(input_dir: Path, output_dir: Path = None, in_place: bool = False):
        """Fix all markdown and text files in a directory"""
        if not input_dir.exists():
            logger.error("Directory not found: %s", input_dir)
            return

        files = list(input_dir.glob('*.md')) + list(input_dir.glob('*.txt'))

        if not files:
            logger.error("No markdown or text files found in %s", input_dir)
            return

        logger.info("ELIDORAS CODEX ENCODING FIXER")
        logger.info("%s", "=" * 60)
        logger.info("Processing %d files...", len(files))

        success_count = 0
        for file_path in sorted(files):
            if output_dir and not in_place:
                out_path = Path(output_dir) / file_path.name
            else:
                out_path = None

            if EncodingFixer.fix_file(file_path, out_path, in_place):
                success_count += 1

        logger.info("%s", "=" * 60)
        logger.info("Successfully processed %d/%d files", success_count, len(files))
        if output_dir and not in_place:
            logger.info("Fixed files saved to: %s", output_dir)
        elif in_place:
            logger.info("Files updated in place: %s", input_dir)


def main():
    import argparse
    parser = argparse.ArgumentParser(
        description='Fix UTF-8 encoding issues in Elidoras Codex files',
    )
    parser.add_argument('input', type=Path, help='Input file or directory containing Codex files')
    parser.add_argument('-o', '--output', type=Path, help='Output directory or file (creates new files by default)')
    parser.add_argument('--in-place', action='store_true', help='Modify files in place (overwrites originals)')
    args = parser.parse_args()

    if args.input.is_file():
        EncodingFixer.fix_file(args.input, args.output, args.in_place)
    elif args.input.is_dir():
        EncodingFixer.fix_directory(args.input, args.output, args.in_place)
    else:
        logger.error("Invalid input: %s", args.input)
        return 1

    logger.info("Witness Protocol: Encoding Repair Complete")
    return 0

if __name__ == '__main__':
    exit(main())
