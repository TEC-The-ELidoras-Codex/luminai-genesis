# Copilot & AI Contributor Guidance

## Project Ethos
- **Validation-seeking:** All code, documentation, and suggestions should be falsifiable, testable, and open to independent replication.
- **Transparency:** No hidden logic, no black boxes. All reasoning and design choices must be explicit.
- **Separation of Concerns:** Narrative, mythoscientific, and fictional content must be placed in `docs/lore/` — not in the main README or core documentation.
- **No Funding Pitches:** Remove all funding, location, or pitch content from main documentation. Focus on research, validation, and reproducibility.

## Copilot/AI Instructions
- Prioritize clarity, reproducibility, and validation in all suggestions.
- Do not generate or insert narrative, mythoscientific, or fictional content into README.md or core docs. Place such content in `docs/lore/` if needed.
- When in doubt, ask for independent validation or a test case.
- All code and documentation should be easy for a new contributor to understand and verify.

## Commit Message Guidance
- Use persona-based commit prefixes (see CONTRIBUTING.md):
  - `airth:` for practical, essential changes
  - `arcadia:` for creative, expansive changes
- Example: `⚙️ airth(docs): clarify validation protocol`

## Pull Request Guidance
- Every PR should state how it improves validation, transparency, or reproducibility.
- Tag at least one human and one persona reviewer.

## For Human Contributors
- If you see Copilot or another AI suggesting narrative or pitch content in the main docs, move it to `docs/lore/` or remove it.
- If you see unclear or untestable logic, request clarification or a test.

---

**This project is validation-first. If in doubt, seek independent replication.**
