#!/usr/bin/env python3
"""
TEC: The Elidoras Codex - Book Compiler
Compiles Markdown chapters with proper screenplay-style formatting into PDF
"""

from pathlib import Path
import re
# Optional PDF dependencies (reportlab). Import lazily for `--check` mode.
HAS_REPORTLAB = True
try:
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.lib.enums import TA_CENTER, TA_LEFT
    from reportlab.platypus import (
        SimpleDocTemplate, Paragraph, Spacer, PageBreak, 
        Image, KeepTogether, Frame, PageTemplate
    )
    from reportlab.platypus.tableofcontents import TableOfContents
    from reportlab.lib.colors import HexColor
except Exception:
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
# Debug flag: perform a temporary page-count build and exit
PAGES_ONLY = False

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
            if c.exists() and (c.suffix in ['.md', '']):
                files.append(c)
                break

    # 2) other tec_chapter_*_*.md (e.g., tec_chapter_x_the_door.md)
    extra = sorted(base.glob('tec_chapter_*_*.md'))
    for ch in extra:
        if ch not in files:
            files.append(ch)

    # 3) include ODT chapter files (they will be listed but skipped during parse)
    odt_files = sorted(base.glob('CHAPTER *.odt'))
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
            if p.suffix.lower() not in ['.md', '']:
                msg = f"⚠️  {p.name}: Non-markdown file (skipping content checks)."
                print(msg)
                w.append(msg)
                warnings[p] = w
                continue

            lines = p.read_text(encoding='utf-8').splitlines()
        except Exception as e:
            msg = f"⚠️  Could not read {p}: {e}"
            print(msg)
            w.append(msg)
            warnings[p] = w
            ok = False
            continue

        # Heuristic checks
        if len(lines) < 10:
            msg = f"⚠️  {p.name}: Very short ({len(lines)} lines)"
            print(msg)
            w.append(msg)

        # Require '# CHAPTER' in first 8 lines unless filename implies chapter number
        has_chapter_heading = any(l.strip().upper().startswith('# CHAPTER') for l in lines[:8])
        filename_implies_chapter = bool(re.search(r'tec[_-]?chapter[_-]?\d+', p.name, re.IGNORECASE))
        if not has_chapter_heading:
            if filename_implies_chapter:
                msg = f"⚠️  {p.name}: Missing '# CHAPTER' heading in first 8 lines (auto-detected from filename)."
                print(msg)
                w.append(msg)
            else:
                msg = f"⚠️  {p.name}: Missing explicit '# CHAPTER' heading in first 8 lines"
                print(msg)
                w.append(msg)
                ok = False

        # Check for author/signature near end as a boarding heuristic
        if not any('— Angelo' in l or '— Angelo' in l for l in lines[-20:]):
            msg = f"⚠️  {p.name}: Missing author signature near the end (heuristic)."
            print(msg)
            w.append(msg)

        if w:
            warnings[p] = w
    return ok, warnings


def show_snippets_for_warnings(warnings):
    """Print first/last lines for files that had warnings to help review."""
    for p, msgs in warnings.items():
        print('\n---\n', f"Snippet for {p.name}:")
        try:
            lines = p.read_text(encoding='utf-8').splitlines()
            head = '\n'.join(lines[:6])
            tail = '\n'.join(lines[-6:])
            print('\n[First lines]\n')
            print(head)
            print('\n[Last lines]\n')
            print(tail)
        except Exception as e:
            print(f"Could not read {p}: {e}")
    print('\n---\n')

# Custom Styles
def create_custom_styles():
    """Create screenplay-style formatting for TEC."""
    styles = getSampleStyleSheet()

    # Optional custom fonts (register if available)
    default_title_font = 'Helvetica-Bold'
    if HAS_REPORTLAB:
        try:
            from reportlab.pdfbase import pdfmetrics
            from reportlab.pdfbase.ttfonts import TTFont
            if CUSTOM_FONT_PATH:
                custom_font_file = Path(CUSTOM_FONT_PATH)
                if custom_font_file.exists():
                    pdfmetrics.registerFont(TTFont('CustomTitle', str(custom_font_file)))
                    default_title_font = 'CustomTitle'
                    print(f"🔤 Registered custom font: {custom_font_file}")
            else:
                # look for a sensible bundled font
                bundled = Path('fonts') / 'Cyberpunk.ttf'
                if bundled.exists():
                    pdfmetrics.registerFont(TTFont('Cyberpunk', str(bundled)))
                    default_title_font = 'Cyberpunk'
                    print(f"🔤 Registered bundled font: {bundled}")
        except Exception:
            # If any font registration fails, fall back to defaults
            default_title_font = 'Helvetica-Bold'
    
    # Book Title (shown once on title page)
    styles.add(ParagraphStyle(
        name='BookTitle',
        parent=styles['Heading1'],
        fontSize=36,
        textColor=HexColor('#FF4400'),
        spaceAfter=20,
        alignment=TA_CENTER,
        fontName=default_title_font
    ))

    styles.add(ParagraphStyle(
        name='Subtitle',
        parent=styles['Normal'],
        fontSize=16,
        textColor=HexColor('#FFFFFF'),
        spaceAfter=12,
        alignment=TA_CENTER,
        fontName='Helvetica'
    ))

    styles.add(ParagraphStyle(
        name='AuthorName',
        parent=styles['Normal'],
        fontSize=14,
        textColor=HexColor('#00AAFF'),
        spaceAfter=6,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    ))

    # Chapter Title (smaller than book title; no author bylines in chapter headings)
    styles.add(ParagraphStyle(
        name='ChapterTitle',
        parent=styles['Heading1'],
        fontSize=20,
        textColor=HexColor('#FF4400'),
        spaceAfter=12,
        alignment=TA_CENTER,
        fontName=default_title_font
    ))

    # Scene Header (INT./EXT.)
    styles.add(ParagraphStyle(
        name='SceneHeader',
        parent=styles['Normal'],
        fontSize=11,
        fontName='Courier-Bold',
        textColor=HexColor('#00AAFF'),
        spaceAfter=6,
        spaceBefore=12,
        leftIndent=0
    ))

    # Author's Note (small, italic)
    styles.add(ParagraphStyle(
        name='AuthorsNote',
        parent=styles['Normal'],
        fontSize=9,
        fontName='Courier-Oblique',
        textColor=HexColor('#666666'),
        leftIndent=0.5*inch,
        rightIndent=0.5*inch,
        spaceAfter=8
    ))
    
    # Character Name (dialogue)
    styles.add(ParagraphStyle(
        name='CharacterName',
        parent=styles['Normal'],
        fontSize=10,
        fontName='Helvetica-Bold',
        textColor=HexColor('#FFFFFF'),
        spaceAfter=2,
        spaceBefore=6,
        leftIndent=1.5*inch,
        alignment=TA_LEFT
    ))
    
    # Dialogue
    styles.add(ParagraphStyle(
        name='Dialogue',
        parent=styles['Normal'],
        fontSize=10,
        fontName='Courier',
        leftIndent=1*inch,
        rightIndent=1.5*inch,
        spaceAfter=6
    ))
    
    # Parenthetical (stage direction in dialogue)
    styles.add(ParagraphStyle(
        name='Parenthetical',
        parent=styles['Normal'],
        fontSize=9,
        fontName='Courier-Oblique',
        leftIndent=1.2*inch,
        spaceAfter=2
    ))
    
    # Action/Description
    styles.add(ParagraphStyle(
        name='Action',
        parent=styles['Normal'],
        fontSize=10,
        fontName='Courier',
        spaceAfter=6
    ))
    
    # Narrator/Airth
    styles.add(ParagraphStyle(
        name='Narrator',
        parent=styles['Normal'],
        fontSize=10,
        fontName='Courier-Oblique',
        textColor=HexColor('#888888'),
        leftIndent=0.5*inch,
        rightIndent=0.5*inch,
        spaceAfter=12
    ))
    
    return styles

def parse_markdown_line(line, styles):
    """Parse a single line of Markdown into appropriate ReportLab flowable."""
    line = line.strip()
    
    # Empty line
    if not line:
        return Spacer(1, 0.1*inch)
    
    # Chapter title (# CHAPTER) — strip bylines if present
    if line.startswith('# CHAPTER'):
        clean = re.sub(r'By\s+Angelo.*$', '', line[2:]).strip()
        return Paragraph(clean, styles['ChapterTitle'])

    # Skip explicit bylines and obvious meta lines
    if 'By Angelo Hurley' in line:
        return None
    if line.lower().startswith('published:'):
        return None
    if line.startswith('A Note Before We Begin') or line.startswith('This is the first chapter'):
        return None
    if '100% of proceeds' in line or 'supporting the mission' in line:
        return None
    
    # Section headers (##)
    if line.startswith('## '):
        return Paragraph(line[3:], styles['Heading2'])
    
    # Scene headers (INT./EXT. or **INT.**)
    if re.match(r'\*\*INT\.|EXT\.|\bINT\.|EXT\.', line, re.IGNORECASE):
        clean = re.sub(r'\*\*|—', '', line).strip()
        return Paragraph(clean, styles['SceneHeader'])
    
    # Character name (all caps at start of line, often with **)
    if re.match(r'\*\*[A-Z][A-Z\s]+\*\*\s*$', line):
        name = re.sub(r'\*\*', '', line).strip()
        return Paragraph(name, styles['CharacterName'])
    
    # Parenthetical (inside dialogue, in italics)
    if re.match(r'\*\(.+\)\*', line):
        clean = re.sub(r'\*|\(|\)', '', line)
        return Paragraph(clean, styles['Parenthetical'])
    
    # Narrator (usually starts with NARRATOR or in italics)
    if line.startswith('*"') or 'NARRATOR' in line.upper():
        clean = re.sub(r'\*|NARRATOR.*?:', '', line).strip()
        return Paragraph(clean, styles['Narrator'])
    
    # Image markdown ![alt](path)
    m = re.match(r'!\[(.*?)\]\((.*?)\)', line)
    if m:
        alt, path = m.groups()
        if HAS_REPORTLAB and Image is not None and inch is not None:
            img_path = IMAGES_DIR / path
            if img_path.exists():
                try:
                    return Image(str(img_path), width=4*inch)
                except Exception as e:
                    print(f"⚠️ Could not insert image {img_path}: {e}")
        else:
            print(f"⚠️ Image reference ignored (PDF support missing): {path}")
        return Spacer(1, 0.1*inch)
    
    # Scene breaks (---)
    if line.startswith('---'):
        return Spacer(1, 0.3*inch)

    # Author's Note heading
    if re.match(r"^(\*\*)?Author'?s Note[:]?", line, re.IGNORECASE):
        clean = re.sub(r"\*|Author'?s Note[:]?", '', line).strip()
        return Paragraph(clean or "Author's Note", styles['AuthorsNote'])
    
    # Dialogue (plain text after character name)
    if line.startswith('"') or not line.startswith('*'):
        # Check if it's action (descriptive) or dialogue
        if any(char in line for char in ['**', '*', '(']):
            # Likely action with formatting
            clean = re.sub(r'\*\*|\*', '', line)
            return Paragraph(clean, styles['Action'])
        else:
            return Paragraph(line, styles['Dialogue'])
    
    # Default: treat as action
    clean = re.sub(r'\*\*|\*', '', line)
    return Paragraph(clean, styles['Action'])

def compile_chapter(chapter_path, styles):
    """Convert a chapter Markdown file to ReportLab flowables."""
    flowables = []
    
    try:
        with open(chapter_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"⚠️ Could not read {chapter_path}: {e}")
        # Return a placeholder so build can continue without crashing
        return [Paragraph(f"Error reading {chapter_path.name}", styles['Action']), PageBreak()]
    
    # Add chapter title page
    chapter_num = re.search(r'chapter[_\s]?(\d+|[a-z]+)', chapter_path.stem, re.IGNORECASE)
    if chapter_num:
        flowables.append(Spacer(1, 2*inch))
        title = f"CHAPTER {chapter_num.group(1).upper()}"
        flowables.append(Paragraph(title, styles['ChapterTitle']))
        flowables.append(Spacer(1, 0.5*inch))
    
    # Parse content
    for line in lines:
        flowable = parse_markdown_line(line, styles)
        if flowable:
            flowables.append(flowable)

    # Append author's note if present (CHAPTER_KEY_note.md)
    note_path = CHAPTERS_DIR / f"{chapter_path.stem}_note.md"
    if note_path.exists():
        flowables.append(Spacer(1, 0.2*inch))
        flowables.append(Paragraph("Author's Note", styles.get('Heading3', styles['Heading2'])))
        try:
            with open(note_path, 'r', encoding='utf-8') as nf:
                nlines = nf.readlines()
            for line in nlines:
                f = parse_markdown_line(line, styles)
                if f:
                    flowables.append(f)
        except Exception as e:
            print(f"⚠️ Could not read note {note_path}: {e}")

    flowables.append(PageBreak())
    return flowables

def add_title_page(styles):
    """Create the book title page (shown exactly once)."""
    flowables = []

    # Optional logo
    logo_path = IMAGES_DIR / "magmasox_logo.png"
    if logo_path.exists():
        flowables.append(Spacer(1, 1*inch))
        try:
            flowables.append(Image(str(logo_path), width=3*inch, height=3*inch))
        except Exception as e:
            print(f"⚠️ Could not insert logo image: {e}")

    flowables.append(Spacer(1, 1*inch))
    flowables.append(Paragraph("THE ELIDORAS CODEX", styles['BookTitle']))
    flowables.append(Spacer(1, 0.2*inch))
    flowables.append(Paragraph("A Story of Memory, Entropy, and the Names We Carve", styles['Subtitle']))
    flowables.append(Spacer(1, 0.3*inch))
    flowables.append(Paragraph("by Angelo Hurley", styles['AuthorName']))
    flowables.append(PageBreak())

    return flowables


def build_index_flowables(index_dict, styles):
    """Create flowables for the Index of Names from a dict mapping name -> sorted list of pages."""
    flowables = [PageBreak()]
    flowables.append(Paragraph("Index of Names", styles['ChapterTitle']))
    flowables.append(Spacer(1, 0.15*inch))

    if not index_dict:
        flowables.append(Paragraph("(No indexable names found)", styles['Action']))
        flowables.append(PageBreak())
        return flowables

    # Create an alphabetical listing
    for name in sorted(index_dict.keys(), key=lambda s: s.lower()):
        pages = sorted(index_dict[name])
        pages_str = ", ".join(str(p) for p in pages)
        line = f"{name} — {pages_str}"
        flowables.append(Paragraph(line, styles['Normal']))
        flowables.append(Spacer(1, 0.05*inch))

    flowables.append(PageBreak())
    return flowables

# A small DocTemplate subclass to capture chapter titles for the TOC
if HAS_REPORTLAB:
    class MyDocTemplate(SimpleDocTemplate):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self._toc = None
            self._index = {}

        def afterFlowable(self, flowable):
            # If it's a chapter title, notify TOC
            try:
                style_name = getattr(flowable, 'style').name
            except Exception:
                style_name = ''
            if style_name == 'ChapterTitle' and self._toc is not None:
                text = flowable.getPlainText()
                # level 0 for chapters
                self.notify('TOCEntry', (0, text, self.page))

            # Collect names (CharacterName style) for the Index
            if style_name == 'CharacterName':
                try:
                    name = flowable.getPlainText().strip()
                    if name:
                        # store as a set of page numbers to avoid duplicates
                        idx = getattr(self, '_index', None)
                        if idx is None:
                            self._index = {}
                            idx = self._index
                        idx.setdefault(name, set()).add(self.page)
                except Exception:
                    pass


def compile_book():
    """Main compilation function."""
    if not HAS_REPORTLAB:
        print("❌ Cannot build PDF: missing 'reportlab' library.")
        print("Tip: create a virtual environment and install reportlab: `python3 -m venv .venv && .venv/bin/pip install reportlab`")
        return 4

    print("🔥 Compiling TEC: The Elidoras Codex...")
    
    # Create output directory
    OUTPUT_PATH.parent.mkdir(exist_ok=True)
    
    # Create custom styles
    styles = create_custom_styles()
    # Note: the actual DocTemplate (MyDocTemplate) will be created later after TOC is prepared
    
    # Build content
    story = []
    
    # Title page
    story.extend(add_title_page(styles))
    print('→ Title page added; story length', len(story))

    # Table of Contents placeholder
    toc = TableOfContents()
    toc.levelStyles = [ParagraphStyle(name='TOCLevel0', parent=styles['Normal'], fontSize=12, leftIndent=20, firstLineIndent=-20, spaceBefore=6)]
    story.append(Paragraph('Contents', styles['ChapterTitle']))
    story.append(Spacer(1, 0.1*inch))
    story.append(toc)
    story.append(PageBreak())
    print('→ TOC placeholder added; story length', len(story))

    # Note: story bible is intentionally excluded from compiled narrative (kept as reference file)
    if STORY_BIBLE_PATH.exists():
        print("ℹ️ Story bible present but excluded from compiled narrative (kept as reference).")

    # Chapters (ordered)
    chapter_files = find_chapter_files()
    if not chapter_files:
        print('⚠️  No chapter files found. Make sure chapter files exist in the tec_book/ directory.')
        return 2

    print(f'Found {len(chapter_files)} chapter(s) to add.')
    for chapter_file in chapter_files:
        # Skip non-markdown chapter sources (ODT) with a warning
        if chapter_file.suffix.lower() not in ['.md', '']:
            print(f"⚠️ Skipping unsupported chapter format: {chapter_file.name}")
            continue
        print(f"Adding {chapter_file.stem}...")
        story.extend(compile_chapter(chapter_file, styles))

    print(f"→ Chapters added: story flowables ~ {len(story)}")

    # Ensure chapter titles start on a fresh page to avoid LayoutError (insert PageBreak before any ChapterTitle
    # that doesn't already follow a PageBreak).
    insert_positions = []
    for i, f in enumerate(story):
        try:
            style_name = getattr(f, 'style').name
        except Exception:
            style_name = ''
        if style_name == 'ChapterTitle' and i > 0:
            if not isinstance(story[i-1], PageBreak):
                insert_positions.append(i)
    # Insert PageBreaks in reverse order so indices remain valid
    for offset, pos in enumerate(reversed(insert_positions)):
        story.insert(pos, PageBreak())
    if insert_positions:
        print(f"→ Inserted {len(insert_positions)} pagebreak(s) before chapter titles to reduce layout issues")

    # Build PDF with footer and a Table of Contents. Use MyDocTemplate to capture TOC entries.
    toc = TableOfContents()
    toc.levelStyles = [
        ParagraphStyle(name='TOCLevel0', parent=styles['Normal'], fontSize=12, leftIndent=20, firstLineIndent=-20, spaceBefore=6)
    ]

    # Prepend a TOC if desired (we placed a placeholder earlier in story)
    # Create the document using MyDocTemplate so afterFlowable can notify TOC
    doc = MyDocTemplate(
        str(OUTPUT_PATH),
        pagesize=letter,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=0.75*inch,
        bottomMargin=0.75*inch
    )
    doc._toc = toc

    def make_footer(total_pages=None):
        def add_footer(canvas, doc):
            canvas.saveState()
            width = letter[0]
            canvas.setFont('Helvetica', 9)
            # left: book title
            canvas.drawString(0.75*inch, 0.5*inch, 'THE ELIDORAS CODEX')
            # right: page numbering (omit page 1)
            page_num = canvas.getPageNumber()
            if page_num > 1:
                if total_pages:
                    canvas.drawRightString(width - 0.75*inch, 0.5*inch, f"Page {page_num} of {total_pages}")
                else:
                    canvas.drawRightString(width - 0.75*inch, 0.5*inch, f"Page {page_num}")
            canvas.restoreState()
        return add_footer

    def _get_pdf_page_count(pdf_path):
        """Try to determine the page count using PyPDF2 first, then pdfinfo."""
        try:
            from PyPDF2 import PdfReader
            with open(pdf_path, 'rb') as fh:
                reader = PdfReader(fh)
                return len(reader.pages)
        except Exception:
            import shutil, subprocess
            pdfinfo = shutil.which('pdfinfo')
            if pdfinfo:
                try:
                    out = subprocess.check_output([pdfinfo, str(pdf_path)], universal_newlines=True, stderr=subprocess.DEVNULL)
                    m = re.search(r'Pages:\s+(\d+)', out)
                    if m:
                        return int(m.group(1))
                except Exception:
                    pass
        return None

    # Perform a two-pass build: first create a temporary PDF to discover total page count (which also populates the TOC),
    # then rebuild the final PDF with 'Page X of Y' in the footer.
    print('→ Reached temporary-build step')
    tmp_pdf = OUTPUT_PATH.with_suffix('.tmp.pdf')
    print("🔁 Building temporary PDF to calculate total pages, collect TOC and index entries...")
    tmp_doc = MyDocTemplate(str(tmp_pdf), pagesize=letter, rightMargin=0.75*inch, leftMargin=0.75*inch, topMargin=0.75*inch, bottomMargin=0.75*inch)
    tmp_doc._toc = toc
    import copy
    try:
        # deepcopy the story for the temporary build so flowables aren't consumed
        tmp_story = copy.deepcopy(story)
        # ensure the TableOfContents flowable in the copied story points to the same `toc` object
        for i, f in enumerate(tmp_story):
            from reportlab.platypus.tableofcontents import TableOfContents as _TOCCls
            if isinstance(f, _TOCCls):
                tmp_story[i] = toc
                break

        # Use multiBuild to ensure TOC entries are collected and the TOC flowable is properly populated
        print('→ Starting tmp_doc.multiBuild (this may take a moment)')
        # For temporary builds we don't render page numbers (stamping will add the final footer), so use a no-op footer
        def _no_footer(canvas, doc):
            return
        tmp_doc.multiBuild(tmp_story, onFirstPage=_no_footer, onLaterPages=_no_footer)
        print('→ tmp_doc.multiBuild finished')
        total_pages = _get_pdf_page_count(tmp_pdf)
        # collect index entries gathered during the multiBuild
        index_entries = getattr(tmp_doc, '_index', {}) or {}

        if total_pages is None:
            print("⚠️ Could not determine total pages automatically; final PDF will omit total pages in footer.")
        else:
            print(f"🔢 Total pages (determined): {total_pages}")

        if PAGES_ONLY:
            print(f"🔎 (pages-only) Total pages: {total_pages or 'unknown'}")
            if index_entries:
                print("🔎 Sample index entries:")
                for name in sorted(index_entries.keys())[:10]:
                    pages = sorted(index_entries[name])
                    print(f" - {name}: {', '.join(str(p) for p in pages)}")
            return 0
    finally:
        # Clean up the temporary file if it exists
        try:
            if tmp_pdf.exists():
                tmp_pdf.unlink()
        except Exception:
            pass

    # Final build with total pages if available
    print("🔨 Building final PDF...")
    final_doc = MyDocTemplate(
        str(OUTPUT_PATH),
        pagesize=letter,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=0.75*inch,
        bottomMargin=0.75*inch
    )
    final_doc._toc = toc

    final_story = copy.deepcopy(story)
    # replace TOC flowable in the final story with the populated `toc` instance
    for i, f in enumerate(final_story):
        from reportlab.platypus.tableofcontents import TableOfContents as _TOCCls
        if isinstance(f, _TOCCls):
            final_story[i] = toc
            break

    # If we collected index entries, append an Index page to the final story
    try:
        if index_entries:
            print(f"🔎 Adding Index of Names ({len(index_entries)} entries) to the final PDF...")
            index_flowables = build_index_flowables(index_entries, styles)
            final_story.extend(index_flowables)
    except Exception:
        # if index_entries isn't defined or any error occurs, continue without index
        pass

    # Because we may have appended an Index (or other end matter), do a final temp build to compute the
    # accurate total page count that includes everything, then rebuild with that accurate total.
    final_tmp = OUTPUT_PATH.with_suffix('.final.tmp.pdf')
    final_tmp_doc = MyDocTemplate(str(final_tmp), pagesize=letter, rightMargin=0.75*inch, leftMargin=0.75*inch, topMargin=0.75*inch, bottomMargin=0.75*inch)
    final_tmp_doc._toc = toc
    final_total_pages = None
    try:
        # Build a final temp PDF without page numbers so that stamping can apply clean footers.
        def _no_footer(canvas, doc):
            return
        final_tmp_doc.multiBuild(final_story, onFirstPage=_no_footer, onLaterPages=_no_footer)
        final_total_pages = _get_pdf_page_count(final_tmp)
    except Exception as e:
        print(f"⚠️ Could not produce final temp PDF for page-stamping: {e}")
        final_total_pages = None
    
    pages_for_footer = final_total_pages or total_pages
    print(f"🔨 Writing final PDF with accurate total pages: {pages_for_footer or 'unknown'}")

    # Prefer stamping the temp PDF with exact page numbers if PyPDF2/reportlab are available.
    stamped = False
    try:
        stamped = _stamp_page_numbers(final_tmp, OUTPUT_PATH, pages_for_footer)
    except Exception as e:
        print(f"⚠️ Stamping page numbers failed: {e}")

    # Clean up the temporary file if it exists
    try:
        if final_tmp.exists():
            final_tmp.unlink()
    except Exception:
        pass

    if stamped:
        print(f"✅ Book compiled: {OUTPUT_PATH}")
        print(f"📄 Total pages: {pages_for_footer or 'unknown (approx)'}")
        return 0

    # Fallback: attempt to build final directly, but catch LayoutError and then fallback to stamping the earlier temp.pdf
    print("⚠️ Falling back to building final PDF directly (no stamping). Will catch LayoutError and retry stamping if needed.")
    try:
        from reportlab.platypus.doctemplate import LayoutError
        try:
            final_doc.multiBuild(final_story, onFirstPage=make_footer(pages_for_footer), onLaterPages=make_footer(pages_for_footer))
            print(f"✅ Book compiled: {OUTPUT_PATH}")
            print(f"📄 Total pages: {pages_for_footer or 'unknown (approx)'}")
            return 0
        except Exception as e:
            if isinstance(e, LayoutError) or 'LayoutError' in repr(e):
                print(f"⚠️ LayoutError while building final PDF directly: {e}. Retrying by stamping the last temporary PDF.")
                # Try stamping the last known temp (final_tmp) if it exists
                if final_tmp.exists():
                    stamped = _stamp_page_numbers(final_tmp, OUTPUT_PATH, pages_for_footer)
                    if stamped:
                        print(f"✅ Book compiled via stamping fallback: {OUTPUT_PATH}")
                        print(f"📄 Total pages: {pages_for_footer or 'unknown (approx)'}")
                        return 0
                raise
            else:
                raise
    except Exception as e:
        print(f"❌ Final PDF build failed: {e}")
        return 5


def _stamp_page_numbers(src_pdf, dest_pdf, total_pages):
    """Overlay 'Page X of Y' footers onto `src_pdf` and write to `dest_pdf`.

    Strategy:
    - For each page create a small overlay PDF that clears a larger footer area and writes the new footer.
    - Try merging overlay onto base page in both candidate orders and pick the one whose extracted text contains the
      intended footer exactly once (best-effort validation).
    - If PyPDF2 or reportlab is unavailable or both merge strategies fail, copy the src_pdf to dest_pdf as a fallback.
    """
    try:
        from PyPDF2 import PdfReader, PdfWriter
        from reportlab.pdfgen import canvas
        import io

        reader = PdfReader(str(src_pdf))
        writer = PdfWriter()

        for i, base_page in enumerate(reader.pages, start=1):
            try:
                # Skip stamping on page 1 (title page)
                if i == 1:
                    writer.add_page(base_page)
                    continue

                # Determine page size from the page media box
                try:
                    mb = base_page.mediabox
                    width = float(mb.upper_right[0] - mb.lower_left[0])
                    height = float(mb.upper_right[1] - mb.lower_left[1])
                except Exception:
                    from reportlab.lib.pagesizes import letter
                    width, height = letter

                # Build the overlay page with a larger white rectangle to fully clear prior footers
                packet = io.BytesIO()
                can = canvas.Canvas(packet, pagesize=(width, height))
                # clear a broader footer band to fully obscure any prior footer content
                clear_h = 1.0 * inch
                # start slightly lower to be safe across different footer placements
                clear_y = 0.15 * inch
                can.setFillColorRGB(1, 1, 1)
                can.rect(0, clear_y, width, clear_h, stroke=0, fill=1)
                can.setFillColorRGB(0, 0, 0)
                can.setFont('Helvetica', 9)
                can.drawString(0.75*inch, 0.5*inch, 'THE ELIDORAS CODEX')
                # draw the full 'Page X of Y' on one line
                can.drawRightString(width - 0.75*inch, 0.5*inch, f"Page {i} of {total_pages}")
                can.save()
                packet.seek(0)
                overlay_src = PdfReader(packet)
                overlay_page = overlay_src.pages[0]

                merged_ok = False
                # Try two merge orders and validate by text extraction where possible
                candidates = []
                try:
                    # Order A: base_page then overlay on top
                    a = base_page.__class__(base_page) if False else base_page
                    try:
                        a.merge_page(overlay_page)
                    except Exception:
                        a.mergePage(overlay_page)
                    candidates.append(a)
                except Exception:
                    pass

                try:
                    # Order B: overlay page with base underneath
                    b = overlay_page.__class__(overlay_page) if False else overlay_page
                    try:
                        b.merge_page(base_page)
                    except Exception:
                        b.mergePage(base_page)
                    candidates.append(b)
                except Exception:
                    pass

                # Heuristic: select candidate whose extracted text contains the footer exactly once
                chosen = None
                footer_text = f"Page {i} of {total_pages}"
                for c in candidates:
                    try:
                        txt = c.extract_text() or ''
                    except Exception:
                        txt = ''
                    if txt.count(footer_text) == 1:
                        chosen = c
                        break

                # Fallback: if none matched the above heuristic, prefer candidate A if present, else B
                if chosen is None and candidates:
                    chosen = candidates[0]

                if chosen is None:
                    # give up on this page: include base page unmodified
                    writer.add_page(base_page)
                else:
                    writer.add_page(chosen)

            except Exception as page_e:
                # Log and continue with unmodified page so stamping doesn't fail completely
                print(f"⚠️ Stamping failed on page {i}: {page_e}")
                try:
                    writer.add_page(base_page)
                except Exception:
                    pass

        with open(dest_pdf, 'wb') as fh:
            writer.write(fh)
        return True

    except Exception as e:
        print(f"⚠️ Could not stamp page numbers ({e}); falling back to copying temp PDF to output.")
        try:
            import shutil
            shutil.copy(str(src_pdf), str(dest_pdf))
            return True
        except Exception as e2:
            print(f"⚠️ Could not copy file to final output: {e2}")
            return False
        total_pages = _get_pdf_page_count(tmp_pdf)
        # collect index entries gathered during the multiBuild
        index_entries = getattr(tmp_doc, '_index', {}) or {}

        if total_pages is None:
            print("⚠️ Could not determine total pages automatically; final PDF will omit total pages in footer.")
        else:
            print(f"🔢 Total pages (determined): {total_pages}")

        if PAGES_ONLY:
            print(f"🔎 (pages-only) Total pages: {total_pages or 'unknown'}")
            if index_entries:
                print("🔎 Sample index entries:")
                for name in sorted(index_entries.keys())[:10]:
                    pages = sorted(index_entries[name])
                    print(f" - {name}: {', '.join(str(p) for p in pages)}")
            return 0
    finally:
        # Clean up the temporary file if it exists
        try:
            if tmp_pdf.exists():
                tmp_pdf.unlink()
        except Exception:
            pass

    # Final build with total pages if available
    print("🔨 Building final PDF...")
    final_doc = MyDocTemplate(
        str(OUTPUT_PATH),
        pagesize=letter,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=0.75*inch,
        bottomMargin=0.75*inch
    )
    final_doc._toc = toc

    final_story = copy.deepcopy(story)
    # replace TOC flowable in the final story with the populated `toc` instance
    for i, f in enumerate(final_story):
        from reportlab.platypus.tableofcontents import TableOfContents as _TOCCls
        if isinstance(f, _TOCCls):
            final_story[i] = toc
            break

    # If we collected index entries, append an Index page to the final story
    try:
        if index_entries:
            print(f"🔎 Adding Index of Names ({len(index_entries)} entries) to the final PDF...")
            index_flowables = build_index_flowables(index_entries, styles)
            final_story.extend(index_flowables)
    except Exception:
        # if index_entries isn't defined or any error occurs, continue without index
        pass

    # Because we may have appended an Index (or other end matter), do a final temp build to compute the
    # accurate total page count that includes everything, then rebuild with that accurate total.

def main():
    parser = argparse.ArgumentParser(description='Compile the Elidoras Codex or run checks.')
    parser.add_argument('--check', action='store_true', help='Run validation checks and list chapter files without building the PDF.')
    parser.add_argument('--output', '-o', help='Override output PDF path.')
    parser.add_argument('--font', help='Path to a TTF font file to use for chapter titles (overrides bundled font).')
    parser.add_argument('--pages', action='store_true', help='Run a temporary build to determine total pages and print them (debug).')
    args = parser.parse_args()

    if args.pages:
        global PAGES_ONLY
        PAGES_ONLY = True

    if args.output:
        global OUTPUT_PATH
        OUTPUT_PATH = Path(args.output)

    if args.font:
        global CUSTOM_FONT_PATH
        CUSTOM_FONT_PATH = args.font
        if not Path(CUSTOM_FONT_PATH).exists():
            print(f"⚠️ Custom font {CUSTOM_FONT_PATH} not found; falling back to bundled/default fonts.")

    chapter_files = find_chapter_files()
    if args.check:
        print("🔍 Running validation checks...")
        if not chapter_files:
            print("⚠️  No chapter files found.")
            return 2
        ok, warnings = validate_chapters(chapter_files)
        if ok:
            print("✅ Validation passed. All chapters look boarded correctly.")
            print("Files inspected:")
            for p in chapter_files:
                print(f" - {p.name}")
            return 0
        else:
            print("❌ Validation found issues. See warnings above. Showing snippets for quick review...")
            show_snippets_for_warnings(warnings)
            return 3

    # Normal build
    return compile_book()

if __name__ == "__main__":
    raise SystemExit(main())
