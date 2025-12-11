# Filing Package — LuminAI Foundation & LuminAI Technologies LLC

This folder contains a prepared filing package to create filing-ready PDFs and a ZIP for the New York Department of State and for your records.

Included files

- `build_pdfs.sh` — script that uses `pandoc` to convert the Markdown files in `docs/legal/` to PDF and packages them into `filing_package.zip`.
- `ny_online_copy.txt` — prefilled plain-text copy of form fields you can paste into the NY DOS online filing form.
- `notarization_cover.txt` — printable cover sheet for notarization and signature guidance.

Source documents (already in repo)

- `docs/legal/nonprofit_articles.md`
- `docs/legal/llc_articles.md`
- `docs/legal/operating_agreement.md`
- `docs/legal/ip_license_full.md`

How to generate PDFs locally

1. Make sure you have `pandoc` and a PDF engine (e.g., `wkhtmltopdf` or LaTeX) installed. On Ubuntu:

```bash
sudo apt update
sudo apt install -y pandoc texlive-xetex zip
```

2. Run the build script from the repository root:

```bash
bash docs/legal/filing_package/build_pdfs.sh
```

3. Output:

- `docs/legal/filing_package/output/*.pdf` — individual PDFs
- `docs/legal/filing_package/filing_package.zip` — ZIP containing the PDFs and cover sheets

If you prefer, I can attempt to render the PDFs in this environment; tell me to proceed and I will run the script (requires `pandoc` and LaTeX availability in the environment).
