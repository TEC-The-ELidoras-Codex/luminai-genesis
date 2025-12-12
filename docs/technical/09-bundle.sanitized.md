---title: "Bundle 9 (sanitized)"bundle_index: 9---# Bundle 9 — Copilot Master Directive & Governance (Sanitized)

This bundle contains the Copilot Master Directive, commit & PR conventions, labels, and governance reference material.

Purpose

- Provide authoritative instructions for commit messages, PR templates, labels, and agent persona routing.
- Keep personal conversational transcripts and PII out of canonical bundles; sensitive material has been redacted.

Key references

- `.github/COPILOT.md` — authoritative agent directives and persona routing.
- `.github/PULL_REQUEST_TEMPLATE.md` — PR checklist and governance items (if present).
- `scripts/validate_commit_msg.sh` — local commit-msg validator.

Summary (high level)

- Standard commit format: `<emoji> <type>(scope): short description` or `persona: scope: action` for agent-authored commits.
- Use the emoji legend and commit axioms stored in `docs/governance/` for commit semantics.
- Labels: use `bug`, `enhancement`, `documentation`, `infra`, `security`, `triage`, `help wanted`, `good first issue`.

Sanitization note

- The original bundle contained conversational transcripts and uploaded artifacts. Those were removed and replaced with this sanitized summary. If specific content is required for the canonical record, add a sanitized excerpt to `docs/streams/` and update the bundle in a follow-up commit.

---
End of sanitized bundle 09.
