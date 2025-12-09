# Launch Checklist — Structural Insurrection

**Goal:** Prepare LuminAI Genesis repository for professional research team review  
**Target:** OpenAI, Anthropic, DeepMind safety/alignment teams  
**Status:** Pre-launch cleanup phase

---

## ✅ Completed

- [x] **Public artifact created** — `STRUCTURAL_INSURRECTION_PUBLIC_ARTIFACT.md`
- [x] **Email templates drafted** — `EMAIL_TEMPLATES.md` (OpenAI, Anthropic, DeepMind, Generic)
- [x] **Repository audit** — Git status reviewed, uncommitted changes identified

---

## 🔄 In Progress

### Documentation Polish

- [ ] Review and update `README.md` for clarity and professionalism
- [ ] Ensure `ARCHITECTURE.md` is complete and technically accurate
- [ ] Create `docs/TGCR_MATHEMATICAL_FRAMEWORK.md` (standalone math reference)
- [ ] Verify all links in public artifact point to correct files
- [ ] Add contact information to public artifact (email, LinkedIn)

### Code Organization

- [ ] Review `src/` structure for clarity
- [ ] Ensure TGCR implementation exists and is documented
- [ ] Verify Witness Protocol implementation is accessible
- [ ] Add docstrings to key classes/functions
- [ ] Create simple usage examples

### Evidence Documentation

- [ ] Verify `docs/evidence/` contains reproducible failure cases
- [ ] Add screenshots/logs if not present
- [ ] Ensure dye-die filter failure is well-documented
- [ ] Document PETA advocacy vs. snuff framing comparison

---

## 📋 Not Started

### Git Cleanup

**Current branch:** `chore/add-ubuntu-setup`  
**Uncommitted changes:**

- Modified: `README.md`, `backend/stripe_webhook.py`, `backend/tests/test_stripe_webhook.py`
- Deleted: `docs/streams/articles/inbox/2025-11-27-resonance-era-thanksgiving-20251127-212148.md`
- Untracked: Multiple files (training data, models, infrastructure scripts)

**Actions needed:**

1. Review modified files — decide to commit or discard
2. Add relevant untracked files to git
3. Update `.gitignore` for large files (models, training data)
4. Clean commit messages for recent history
5. Merge to main or create clean feature branch

### Testing

- [ ] Run pytest suite — ensure tests pass
- [ ] Fix pytest exit code 127 error (missing venv activation?)
- [ ] Run linting (Ruff, Black)
- [ ] Verify combat demo runs successfully

### Final Touches

- [ ] Convert `STRUCTURAL_INSURRECTION_PUBLIC_ARTIFACT.md` to PDF
- [ ] Create one-page visual diagram of TGCR architecture
- [ ] Add LICENSE file (MIT already present, verify it's complete)
- [ ] Create CITATION.cff for academic citation
- [ ] Add badges to README (build status, license, etc.)

---

## 🎯 Priority Order

### Phase 1: Critical for Launch (Do First)

1. Fix git status (commit or discard changes)
2. Update contact info in public artifact
3. Verify all links work
4. Run tests and fix failures
5. Polish README.md

### Phase 2: High Value (Do Before Sending)

1. Create TGCR mathematical framework doc
2. Organize evidence folder
3. Add code examples
4. Convert artifact to PDF

### Phase 3: Nice to Have (Can Do After)

1. Create visual diagrams
2. Add CITATION.cff
3. Polish all documentation
4. Create video walkthrough

---

## 🚀 Launch Sequence

Once checklist is complete:

1. **Commit all changes** — Clean git history
2. **Push to GitHub** — Make repository public-ready
3. **Create PDF** — Convert markdown artifact to professional PDF
4. **Test all links** — Verify nothing is broken
5. **Send emails** — Use templates, attach PDF
6. **Post to Substack** — Publish public artifact
7. **Share on LinkedIn** — Announce research availability
8. **Monitor responses** — Prepare for technical questions

---

## 📧 Contact Information Needed

**Before launch, add to public artifact:**

- [ ] Professional email address
- [ ] LinkedIn profile URL
- [ ] Optional: Twitter/X handle
- [ ] Optional: Personal website

---

## 📝 Notes

- Repository is on branch `chore/add-ubuntu-setup`, 1 commit ahead of origin
- Last commit: `docs(philosophy): add AI safety framework documentation`
- Pytest is failing (exit code 127) — likely venv issue
- Models folder is large and untracked — should stay in .gitignore
- Training data is untracked — should stay in .gitignore

---

**Next Immediate Action:** Review uncommitted changes and decide whether to commit or discard.
