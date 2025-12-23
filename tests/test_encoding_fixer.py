from scripts.codex_encoding_fixer import EncodingFixer


def test_fix_co2_and_degree():
    # Use corrupted sequences to ensure fixer normalizes them
    text = 'This is COâ‚‚ at 25Â°C and some weird dash â€" and ellipsis...'
    fixed = EncodingFixer.fix_text(text)
    assert "CO₂" in fixed
    assert "25°C" in fixed
    assert "—" in fixed
    assert "..." in fixed


def test_no_changes_on_clean_text():
    clean = "Normal text — CO₂ — 100%"
    assert EncodingFixer.fix_text(clean) == clean
