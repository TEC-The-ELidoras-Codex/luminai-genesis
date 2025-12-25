#!/usr/bin/env python3
"""
TEC: The Elidoras Codex - Book Compiler
Compiles Markdown chapters with proper screenplay-style formatting into PDF
"""

from pathlib import Path
import re
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, 
    Image, KeepTogether, Frame, PageTemplate
)
from reportlab.lib.colors import HexColor

# Configuration
CHAPTERS_DIR = Path("chapters")
IMAGES_DIR = Path("images")
OUTPUT_PATH = Path("output/tec_complete_book.pdf")
STORY_BIBLE_PATH = Path("tec_story_bible.md")

# Custom Styles
def create_custom_styles():
    """Create screenplay-style formatting for TEC."""
    styles = getSampleStyleSheet()
    
    # Chapter Title
    styles.add(ParagraphStyle(
        name='ChapterTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=HexColor('#FF4400'),
        spaceAfter=12,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
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
    
    # Chapter title (# CHAPTER)
    if line.startswith('# CHAPTER'):
        return Paragraph(line[2:], styles['ChapterTitle'])
    
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
    
    # Scene breaks (---)
    if line.startswith('---'):
        return Spacer(1, 0.3*inch)
    
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
    
    with open(chapter_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
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
    
    flowables.append(PageBreak())
    return flowables

def add_title_page(styles):
    """Create the book title page."""
    flowables = []
    
    # Logo
    logo_path = IMAGES_DIR / "magmasox_logo.png"
    if logo_path.exists():
        flowables.append(Spacer(1, 1*inch))
        flowables.append(Image(str(logo_path), width=3*inch, height=3*inch))
    
    # Title
    flowables.append(Spacer(1, 0.5*inch))
    title = "THE ELIDORAS CODEX"
    subtitle = "A Story of Memory, Entropy, and the Names We Carve"
    flowables.append(Paragraph(title, styles['ChapterTitle']))
    flowables.append(Paragraph(subtitle, styles['Heading2']))
    flowables.append(Spacer(1, 0.3*inch))
    flowables.append(Paragraph("by Angelo Hurley", styles['Normal']))
    flowables.append(PageBreak())
    
    return flowables

def compile_book():
    """Main compilation function."""
    print("🔥 Compiling TEC: The Elidoras Codex...")
    
    # Create output directory
    OUTPUT_PATH.parent.mkdir(exist_ok=True)
    
    # Initialize PDF
    doc = SimpleDocTemplate(
        str(OUTPUT_PATH),
        pagesize=letter,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=0.75*inch,
        bottomMargin=0.75*inch
    )
    
    # Create custom styles
    styles = create_custom_styles()
    
    # Build content
    story = []
    
    # Title page
    story.extend(add_title_page(styles))
    
    # Story bible
    if STORY_BIBLE_PATH.exists():
        print(f"Adding story bible...")
        story.extend(compile_chapter(STORY_BIBLE_PATH, styles))
    
    # Chapters (sorted)
    chapter_files = sorted(CHAPTERS_DIR.glob("*.md"))
    for chapter_file in chapter_files:
        print(f"Adding {chapter_file.stem}...")
        story.extend(compile_chapter(chapter_file, styles))
    
    # Build PDF
    doc.build(story)
    print(f"✅ Book compiled: {OUTPUT_PATH}")
    print(f"📄 Total pages: ~{len(story) // 20}")

if __name__ == "__main__":
    compile_book()
