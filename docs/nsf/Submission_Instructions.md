NSF Seed Fund (SBIR/STTR) — Submission Instructions (Concise)

1. Portal Access

- Visit: https://seedfund.nsf.gov/
- Create or log into your account (Grants.gov/NSF credentials may be required for full proposals; the Project Pitch interface accepts short submissions).

2. Prepare Files

- Project Pitch: copy contents of `NSF_SBIR_Project_Pitch.md` (one-page) into the portal text box.
- Full Application (if requested): upload a PDF compiled from `NSF_SBIR_Application_Draft.md`, `Budget_and_Justification.md`, and `PI_Biosketch_Angelo_Hurley.md`.
- Letters: use templates in `Letters_of_Support_Templates.md` and request sign-offs; upload as PDFs.

3. Budget Upload

- Use the portal's simple budget form or upload a PDF of `Budget_and_Justification.md` converted to PDF.

4. Submission Checklist

- Ensure all placeholders (emails, degrees, advisor names, Ko‑fi URL if required) are filled.
- Convert final Markdown files to PDF for portal upload (recommended: use Pandoc or print-to-PDF).

5. Suggested Commands (local)
   Convert a single markdown to PDF via Pandoc:

```bash
pandoc docs/nsf/NSF_SBIR_Application_Draft.md docs/nsf/Budget_and_Justification.md \
  docs/nsf/PI_Biosketch_Angelo_Hurley.md -o docs/nsf/NSF_Application_Combined.pdf
```

Or render individual PDFs:

```bash
pandoc docs/nsf/NSF_SBIR_Project_Pitch.md -o docs/nsf/NSF_Project_Pitch.pdf
pandoc docs/nsf/Budget_and_Justification.md -o docs/nsf/Budget_and_Justification.pdf
```

6. Submit

- Paste the 1-page pitch and upload supporting PDFs. Keep a copy of submission confirmation emails and timestamps.
