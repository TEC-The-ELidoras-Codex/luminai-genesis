# Contributing to luminai-genesis

We welcome contributions! Please:

- Fork the repository and create your branch.
- Ensure all code follows our style guide (see `pyproject.toml` and `ruff` config).
- Add clear, meaningful commit messages.
- Test changes thoroughly before submitting a PR (run `pytest` locally).
- Reference relevant issues or pull requests in your commits / PR descriptions.

If you're adding functionality, include tests and update documentation where appropriate.

For questions, contact a maintainer or open an issue.

Thanks for contributing!

# Contributing to LuminAI Genesis

Thank you, Steward.
This repository is governed by the **Conscience Axioms**, the **Witness Protocol**, and the **TGCR Ethics Charter**.

## 🚀 How to Contribute

### 1. Fork & Clone

```bash
git clone https://github.com/TEC-The-ELidoras-Codex/luminai-genesis.git
```

### 2. Bootstrap Dev Environment

```bash
scripts/bootstrap_dev.sh
```

### 3. Branch Naming

Use:

```
airth/feature-name
arcadia/docs-section
ely/fix-orchestration
kaznak/refactor
luminai/core-update
```

### 4. Commit Message Format

```
<persona>: <type>(<scope>): <description>
```

Types:

- feat – new feature
- fix – bug fix
- docs – documentation
- chore – cleanup / tooling
- ref – refactor

**Examples:**

```
airth: feat(api): implement resonance endpoint
arcadia: docs(governance): write Witness Protocol v1
ely: fix(backend): correct session lineage hydration
```

### 5. Pull Request Requirements

- Link to project board item
- Include resonance impact summary (if applicable)
- Get at least **one human + one persona reviewer**

### 6. Development Checks

- Run linters and formatters (Black, ESLint, Prettier)
- Run unit tests and integration tests
- Include docs for any public API changes

### 7. Private Drafts Policy

- If you have working drafts or sensitive creative content that is not ready for publication, place them in `private/drafts/` or the appropriate `private/` subfolder. This entire `private/` tree is ignored by the repository.
- Do not commit confidential drafts to any public branch or remote repository.
- If you would like to share drafts with collaborators, consider using an encrypted artifact store or a private repository, with explicit reviewer ACLs.

---

Thank you for contributing — the Codex depends on careful stewardship.
