#!/usr/bin/env python3
"""
TEC: The Elidoras Codex - Book Compiler
Compiles Markdown chapters with proper screenplay-style formatting into PDF
"""

import logging
import re
from pathlib import Path

# Optional PDF dependencies (reportlab). Import lazily for `--check` mode.
HAS_REPORTLAB = True
logger = logging.getLogger(__name__)
try:
    from reportlab.lib.colors import HexColor
    from reportlab.lib.enums import TA_CENTER, TA_LEFT
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
    from reportlab.lib.units import inch
    from reportlab.platypus import (
        Frame,
        Image,
        KeepTogether,
        PageBreak,
        PageTemplate,
        Paragraph,
        SimpleDocTemplate,
        Spacer,
    )
    from reportlab.platypus.tableofcontents import TableOfContents
except Exception as _:
    HAS_REPORTLAB = False
    # Define minimal stand-ins or names to avoid NameError when running validation
    letter = None
    getSampleStyleSheet = None
    ParagraphStyle = None
    inch = None
    TA_CENTER = None
    TA_LEFT = None
    SimpleDocTemplate = None
    Paragraph = None
    Spacer = None
    PageBreak = None
    Image = None
    KeepTogether = None
    Frame = None
    PageTemplate = None
    HexColor = None

# Configuration (allow flexible chapter discovery)
CHAPTERS_DIR = Path("chapters")
IMAGES_DIR = Path("images")
OUTPUT_PATH = Path("output/tec_complete_book.pdf")
STORY_BIBLE_PATH = Path("tec_story_bible.md")

# Custom font path (can be overridden via CLI: --font)
CUSTOM_FONT_PATH = None

import argparse


def find_chapter_files():
    """Find chapter files in a predictable reading order.

    Strategy:
    1. Look for explicit numbered chapter files: tec_chapter_{N}_final(.md|no-ext)
    2. Append any other `tec_chapter_*_*.md` extras
    3. Include ODT files named like `CHAPTER *.odt` (warn that they won't be parsed)
    """
    base = Path(__file__).parent
    files = []

    # 1) explicit numbered chapters (support files without .md ext too)
    for i in range(1, 40):
        candidates = [
            base / f"tec_chapter_{i}_final.md",
            base / f"tec_chapter_{i}_final",
            base / f"tec_chapter_{i}.md",
            base / f"tec_chapter_{i}",
        ]
        for c in candidates:
            if c.exists() and (c.suffix in [".md", ""]):
                files.append(c)
                break

    # 2) other tec_chapter_*_*.md (e.g., tec_chapter_x_the_door.md)
    extra = sorted(base.glob("tec_chapter_*_*.md"))
    for ch in extra:
        if ch not in files:
            files.append(ch)

    # 3) include ODT chapter files (they will be listed but skipped during parse)
    odt_files = sorted(base.glob("CHAPTER *.odt"))
    for odt in odt_files:
        files.append(odt)

    # Filter out story bible (never compile it directly)
    files = [f for f in files if f.resolve() != STORY_BIBLE_PATH.resolve()]

    return files


def validate_chapters(chapter_files):
    """Check chapters for basic boarding issues and print warnings. Returns True if all checks pass."""
    ok = True
    warnings = {}
    for p in chapter_files:
        w = []
        try:
            # Skip binary/non-markdown files for content checks (we still list them)
            if p.suffix.lower() not in [".md", ""]:
                msg = f"⚠️  {p.name}: Non-markdown file (skipping content checks)."
                logger.warning(msg)
                w.append(msg)
                warnings[p] = w
                continue

            with p.open(encoding="utf-8") as fh:
                lines = fh.read().splitlines()
        except (OSError, UnicodeDecodeError) as e:
            msg = f"⚠️  Could not read {p}: {e}"
            logger.warning(msg)
            w.append(msg)
            warnings[p] = w
            ok = False
            continue

        # Heuristic checks
        if len(lines) < 10:
            msg = f"⚠️  {p.name}: Very short ({len(lines)} lines)"
            logger.warning(msg)
            w.append(msg)

        # Require '# CHAPTER' in first 8 lines unless filename implies chapter number
        has_chapter_heading = any(
            l.strip().upper().startswith("# CHAPTER") for l in lines[:8]
        )
        filename_implies_chapter = bool(
            re.search(r"tec[_-]?chapter[_-]?\d+", p.name, re.IGNORECASE),
        )
        if not has_chapter_heading:
            if filename_implies_chapter:
                msg = f"⚠️  {p.name}: Missing '# CHAPTER' heading in first 8 lines (auto-detected from filename)."
                logger.warning(msg)
                w.append(msg)
            else:
                msg = f"⚠️  {p.name}: Missing explicit '# CHAPTER' heading in first 8 lines"
                logger.warning(msg)
                w.append(msg)
                ok = False

        # Check for author/signature near end as a boarding heuristic
        if not any("— Angelo" in l or "— Angelo" in l for l in lines[-20:]):
            msg = f"⚠️  {p.name}: Missing author signature near the end (heuristic)."
            logger.warning(msg)
            w.append(msg)

        if w:
            warnings[p] = w
    return ok, warnings


def show_snippets_for_warnings(warnings):
    """Print first/last lines for files that had warnings to help review."""
    for p, msgs in warnings.items():
        logger.warning("\n---\n")
        logger.warning(f"Snippet for {p.name}:")
        try:
            with p.open(encoding="utf-8") as fh:
                lines = fh.read().splitlines()
            head = "\n".join(lines[:6])
            tail = "\n".join(lines[-6:])
            logger.warning("\n[First lines]\n")
            logger.warning(head)
            logger.warning("\n[Last lines]\n")
            logger.warning(tail)
        except Exception as e:
            logger.warning(f"Could not read {p}: {e}")
    logger.warning("\n---\n")


# Custom Styles
def create_custom_styles():
    """Create screenplay-style formatting for TEC."""
    styles = getSampleStyleSheet()

    # Optional custom fonts (register if available)
    default_title_font = "Helvetica-Bold"
    if HAS_REPORTLAB:
        try:
            from reportlab.pdfbase import pdfmetrics
            from reportlab.pdfbase.ttfonts import TTFont

            if CUSTOM_FONT_PATH:
                custom_font_file = Path(CUSTOM_FONT_PATH)
                if custom_font_file.exists():
                    pdfmetrics.registerFont(
                        TTFont("CustomTitle", str(custom_font_file)),
                    )
                    default_title_font = "CustomTitle"
            else:
                # look for a sensible bundled font
                bundled = Path("fonts") / "Cyberpunk.ttf"
                if bundled.exists():
                    pdfmetrics.registerFont(TTFont("Cyberpunk", str(bundled)))
                    default_title_font = "Cyberpunk"
        except Exception:
            # If any font registration fails, fall back to defaults
            default_title_font = "Helvetica-Bold"

    # Book Title (shown once on title page)
    styles.add(
        ParagraphStyle(
            name="BookTitle",
            parent=styles["Heading1"],
            fontSize=36,
            textColor=HexColor("#FF4400"),
            spaceAfter=20,
            alignment=TA_CENTER,
            fontName=default_title_font,
        ),
    )

    styles.add(
        ParagraphStyle(
            name="Subtitle",
            parent=styles["Normal"],
            fontSize=16,
            textColor=HexColor("#FFFFFF"),
            spaceAfter=12,
            alignment=TA_CENTER,
            fontName="Helvetica",
        ),
    )

    styles.add(
        ParagraphStyle(
            name="AuthorName",
            parent=styles["Normal"],
            fontSize=14,
            textColor=HexColor("#00AAFF"),
            spaceAfter=6,
            alignment=TA_CENTER,
            fontName="Helvetica-Bold",
        ),
    )

    # Chapter Title (smaller than book title; no author bylines in chapter headings)
    styles.add(
        ParagraphStyle(
            name="ChapterTitle",
            parent=styles["Heading1"],
            fontSize=20,
            textColor=HexColor("#FF4400"),
            spaceAfter=12,
            alignment=TA_CENTER,
            fontName=default_title_font,
        ),
    )

    # Scene Header (INT./EXT.)
    styles.add(
        ParagraphStyle(
            name="SceneHeader",
            parent=styles["Normal"],
            fontSize=11,
            fontName="Courier-Bold",
            textColor=HexColor("#00AAFF"),
            spaceAfter=6,
            spaceBefore=12,
            leftIndent=0,
        ),
    )

    # Author's Note (small, italic)
    styles.add(
        ParagraphStyle(
            name="AuthorsNote",
            parent=styles["Normal"],
            fontSize=9,
            fontName="Courier-Oblique",
            textColor=HexColor("#666666"),
            leftIndent=0.5 * inch,
            rightIndent=0.5 * inch,
            spaceAfter=8,
        ),
    )

    # Character Name (dialogue)
    styles.add(
        ParagraphStyle(
            name="CharacterName",
            parent=styles["Normal"],
            fontSize=10,
            fontName="Helvetica-Bold",
            textColor=HexColor("#FFFFFF"),
            spaceAfter=2,
            spaceBefore=6,
            leftIndent=1.5 * inch,
            alignment=TA_LEFT,
        ),
    )

    # Dialogue
    styles.add(
        ParagraphStyle(
            name="Dialogue",
            parent=styles["Normal"],
            fontSize=10,
            fontName="Courier",
            leftIndent=1 * inch,
            rightIndent=1.5 * inch,
            spaceAfter=6,
        ),
    )

    # Parenthetical (stage direction in dialogue)
    styles.add(
        ParagraphStyle(
            name="Parenthetical",
            parent=styles["Normal"],
            fontSize=9,
            fontName="Courier-Oblique",
            leftIndent=1.2 * inch,
            spaceAfter=2,
        ),
    )

    # Action/Description
    styles.add(
        ParagraphStyle(
            name="Action",
            parent=styles["Normal"],
            fontSize=10,
            fontName="Courier",
            spaceAfter=6,
        ),
    )

    # Narrator/Airth
    styles.add(
        ParagraphStyle(
            name="Narrator",
            parent=styles["Normal"],
            fontSize=10,
            fontName="Courier-Oblique",
            textColor=HexColor("#888888"),
            leftIndent=0.5 * inch,
            rightIndent=0.5 * inch,
            spaceAfter=12,
        ),
    )

    return styles


def parse_markdown_line(line, styles):
    """Parse a single line of Markdown into appropriate ReportLab flowable."""
    line = line.strip()

    # Empty line
    if not line:
        return Spacer(1, 0.1 * inch)

    # Chapter title (# CHAPTER) — strip bylines if present
    if line.startswith("# CHAPTER"):
        clean = re.sub(r"By\s+Angelo.*$", "", line[2:]).strip()
        return Paragraph(clean, styles["ChapterTitle"])

    # Skip explicit bylines and obvious meta lines
    if "By Angelo Hurley" in line:
        return None
    if line.lower().startswith("published:"):
        return None
    if line.startswith("A Note Before We Begin") or line.startswith(
        "This is the first chapter",
    ):
        return None
    if "100% of proceeds" in line or "supporting the mission" in line:
        return None

    # Section headers (##)
    if line.startswith("## "):
        return Paragraph(line[3:], styles["Heading2"])

    # Scene headers (INT./EXT. or **INT.**)
    if re.match(r"\*\*INT\.|EXT\.|\bINT\.|EXT\.", line, re.IGNORECASE):
        clean = re.sub(r"\*\*|—", "", line).strip()
        return Paragraph(clean, styles["SceneHeader"])

    # Character name (all caps at start of line, often with **)
    if re.match(r"\*\*[A-Z][A-Z\s]+\*\*\s*$", line):
        name = re.sub(r"\*\*", "", line).strip()
        return Paragraph(name, styles["CharacterName"])

    # Parenthetical (inside dialogue, in italics)
    if re.match(r"\*\(.+\)\*", line):
        clean = re.sub(r"\*|\(|\)", "", line)
        return Paragraph(clean, styles["Parenthetical"])

    # Narrator (usually starts with NARRATOR or in italics)
    if line.startswith('*"') or "NARRATOR" in line.upper():
        clean = re.sub(r"\*|NARRATOR.*?:", "", line).strip()
        return Paragraph(clean, styles["Narrator"])

    # Image markdown ![alt](path)
    m = re.match(r"!\[(.*?)\]\((.*?)\)", line)
    if m:
        alt, path = m.groups()
        if HAS_REPORTLAB and Image is not None and inch is not None:
            img_path = IMAGES_DIR / path
            if img_path.exists():
                try:
                    return Image(str(img_path), width=4 * inch)
                except Exception as e:
                    logger.warning("⚠️ Could not insert image %s: %s", img_path, e)
        else:
            logger.warning("⚠️ Image reference ignored (PDF support missing): %s", path)
        return Spacer(1, 0.1 * inch)

    # Scene breaks (---)
    if line.startswith("---"):
        return Spacer(1, 0.3 * inch)

    # Author's Note heading
    if re.match(r"^(\*\*)?Author'?s Note[:]?", line, re.IGNORECASE):
        clean = re.sub(r"\*|Author'?s Note[:]?", "", line).strip()
        return Paragraph(clean or "Author's Note", styles["AuthorsNote"])

    # Dialogue (plain text after character name)
    if line.startswith('"') or not line.startswith("*"):
        # Check if it's action (descriptive) or dialogue
        if any(char in line for char in ["**", "*", "("]):
            # Likely action with formatting
            clean = re.sub(r"\*\*|\*", "", line)
            return Paragraph(clean, styles["Action"])
        return Paragraph(line, styles["Dialogue"])

    # Default: treat as action
    clean = re.sub(r"\*\*|\*", "", line)
    return Paragraph(clean, styles["Action"])


def compile_chapter(chapter_path, styles):
    """Convert a chapter Markdown file to ReportLab flowables."""
    flowables = []

    try:
        with open(chapter_path, encoding="utf-8") as f:
            lines = f.readlines()
    except Exception as e:
        logger.warning("⚠️ Could not read %s: %s", chapter_path, e)
        # Return a placeholder so build can continue without crashing
        return [
            Paragraph(f"Error reading {chapter_path.name}", styles["Action"]),
            PageBreak(),
        ]

    # Add chapter title page
    chapter_num = re.search(
        r"chapter[_\s]?(\d+|[a-z]+)", chapter_path.stem, re.IGNORECASE,
    )
    if chapter_num:
        flowables.append(Spacer(1, 2 * inch))
        title = f"CHAPTER {chapter_num.group(1).upper()}"
        flowables.append(Paragraph(title, styles["ChapterTitle"]))
        flowables.append(Spacer(1, 0.5 * inch))

    # Parse content
    for line in lines:
        flowable = parse_markdown_line(line, styles)
        if flowable:
            flowables.append(flowable)

    # Append author's note if present (CHAPTER_KEY_note.md)
    note_path = CHAPTERS_DIR / f"{chapter_path.stem}_note.md"
    if note_path.exists():
        flowables.append(Spacer(1, 0.2 * inch))
        flowables.append(
            Paragraph("Author's Note", styles.get("Heading3", styles["Heading2"])),
        )
        try:
            with open(note_path, encoding="utf-8") as nf:
                nlines = nf.readlines()
            for line in nlines:
                f = parse_markdown_line(line, styles)
                if f:
                    flowables.append(f)
        except Exception as e:
            logger.warning("⚠️ Could not read note %s: %s", note_path, e)

    flowables.append(PageBreak())
    return flowables


def add_title_page(styles):
    """Create the book title page (shown exactly once)."""
    flowables = []

    # Optional logo
    logo_path = IMAGES_DIR / "magmasox_logo.png"
    if logo_path.exists():
        flowables.append(Spacer(1, 1 * inch))
        try:
            flowables.append(Image(str(logo_path), width=3 * inch, height=3 * inch))
        except Exception as e:
            logger.warning("⚠️ Could not insert logo image: %s", e)

    flowables.append(Spacer(1, 1 * inch))
    flowables.append(Paragraph("THE ELIDORAS CODEX", styles["BookTitle"]))
    flowables.append(Spacer(1, 0.2 * inch))
    flowables.append(
        Paragraph(
            "A Story of Memory, Entropy, and the Names We Carve", styles["Subtitle"],
        ),
    )
    flowables.append(Spacer(1, 0.3 * inch))
    flowables.append(Paragraph("by Angelo Hurley", styles["AuthorName"]))
    flowables.append(PageBreak())

    return flowables


# A small DocTemplate subclass to capture chapter titles for the TOC
if HAS_REPORTLAB:

    class MyDocTemplate(SimpleDocTemplate):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self._toc = None

        def afterFlowable(self, flowable):
            # If it's a chapter title, notify TOC
            try:
                style_name = flowable.style.name
            except Exception:
                style_name = ""
            if style_name == "ChapterTitle" and self._toc is not None:
                text = flowable.getPlainText()
                # level 0 for chapters
                self.notify("TOCEntry", (0, text, self.page))


def compile_book():
    """Main compilation function."""
    if not HAS_REPORTLAB:
        logger.error("❌ Cannot build PDF: missing 'reportlab' library.")
        logger.info(
            "Tip: create a virtual environment and install reportlab: `python3 -m venv .venv && .venv/bin/pip install reportlab`",
        )
        return 4

    logger.info("🔥 Compiling TEC: The Elidoras Codex...")

    # Create output directory
    OUTPUT_PATH.parent.mkdir(exist_ok=True)

    # Create custom styles
    styles = create_custom_styles()
    # Note: the actual DocTemplate (MyDocTemplate) will be created later after TOC is prepared

    # Build content
    story = []

    # Title page
    story.extend(add_title_page(styles))

    # Table of Contents placeholder
    toc = TableOfContents()
    toc.levelStyles = [
        ParagraphStyle(
            name="TOCLevel0",
            parent=styles["Normal"],
            fontSize=12,
            leftIndent=20,
            firstLineIndent=-20,
            spaceBefore=6,
        ),
    ]
    story.append(Paragraph("Contents", styles["ChapterTitle"]))
    story.append(Spacer(1, 0.1 * inch))
    story.append(toc)
    story.append(PageBreak())

    # Note: story bible is intentionally excluded from compiled narrative (kept as reference file)
    if STORY_BIBLE_PATH.exists():
        logger.info(
            "ℹ️ Story bible present but excluded from compiled narrative (kept as reference).",
        )

    # Chapters (ordered)
    chapter_files = find_chapter_files()
    if not chapter_files:
        logger.error(
            "⚠️  No chapter files found. Make sure chapter files exist in the tec_book/ directory.",
        )
        return 2

    logger.info("Found %d chapter(s) to add.", len(chapter_files))
    for chapter_file in chapter_files:
        # Skip non-markdown chapter sources (ODT) with a warning
        if chapter_file.suffix.lower() not in [".md", ""]:
            logger.warning(
                "⚠️ Skipping unsupported chapter format: %s", chapter_file.name,
            )
            continue
        logger.info("Adding %s...", chapter_file.stem)
        story.extend(compile_chapter(chapter_file, styles))

    # Build PDF with footer and a Table of Contents. Use MyDocTemplate to capture TOC entries.
    toc = TableOfContents()
    toc.levelStyles = [
        ParagraphStyle(
            name="TOCLevel0",
            parent=styles["Normal"],
            fontSize=12,
            leftIndent=20,
            firstLineIndent=-20,
            spaceBefore=6,
        ),
    ]

    # Prepend a TOC if desired (we placed a placeholder earlier in story)
    # Create the document using MyDocTemplate so afterFlowable can notify TOC
    doc = MyDocTemplate(
        str(OUTPUT_PATH),
        pagesize=letter,
        rightMargin=0.75 * inch,
        leftMargin=0.75 * inch,
        topMargin=0.75 * inch,
        bottomMargin=0.75 * inch,
    )
    doc._toc = toc

    def add_footer(canvas, doc):
        canvas.saveState()
        width = letter[0]
        canvas.setFont("Helvetica", 9)
        # left: book title
        canvas.drawString(0.75 * inch, 0.5 * inch, "THE ELIDORAS CODEX")
        # right: page number (omit page 1)
        page_num = canvas.getPageNumber()
        if page_num > 1:
            canvas.drawRightString(width - 0.75 * inch, 0.5 * inch, f"Page {page_num}")
        canvas.restoreState()

    doc.build(story, onFirstPage=add_footer, onLaterPages=add_footer)

    logger.info("✅ Book compiled: %s", OUTPUT_PATH)
    logger.info("📄 Total pages: ~%d", (len(story) // 20))


def main():
    parser = argparse.ArgumentParser(
        description="Compile the Elidoras Codex or run checks.",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Run validation checks and list chapter files without building the PDF.",
    )
    parser.add_argument("--output", "-o", help="Override output PDF path.")
    parser.add_argument(
        "--font",
        help="Path to a TTF font file to use for chapter titles (overrides bundled font).",
    )
    args = parser.parse_args()

    if args.output:
        global OUTPUT_PATH
        OUTPUT_PATH = Path(args.output)

    if args.font:
        global CUSTOM_FONT_PATH
        CUSTOM_FONT_PATH = args.font
        if not Path(CUSTOM_FONT_PATH).exists():
            logger.warning(
                "⚠️ Custom font %s not found; falling back to bundled/default fonts.",
                CUSTOM_FONT_PATH,
            )
    if args.check:
        logger.info("🔍 Running validation checks...")
        if not chapter_files:
            logger.error("⚠️  No chapter files found.")
            return 2
        ok, warnings = validate_chapters(chapter_files)
        if ok:
            logger.info("✅ Validation passed. All chapters look boarded correctly.")
            logger.info("Files inspected:")
            for p in chapter_files:
                logger.info(" - %s", p.name)
            return 0
        logger.error(
            "❌ Validation found issues. See warnings above. Showing snippets for quick review...",
        )
        show_snippets_for_warnings(warnings)
        return 3

    # Normal build
    return compile_book()


if __name__ == "__main__":
    raise SystemExit(main())
