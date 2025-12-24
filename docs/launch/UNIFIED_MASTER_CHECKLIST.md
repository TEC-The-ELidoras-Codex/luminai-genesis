# 🎯 UNIFIED MASTER CHECKLIST

**Status:** Pre-Launch
**Repository:** https://github.com/TEC-The-ELidoras-Codex/luminai-genesis
**Target Date:** January 7, 2026

---

## PHASE 1: DOCUMENTATION CLEANUP (Do First)

### README.md - Strip to Essentials
- [ ] Remove all personal narrative/backstory
- [ ] Remove "dynasty" references and lore
- [ ] Focus only on: What it is, Why it matters, How to use it
- [ ] Keep: TL;DR, Quick Start, SAR Benchmark, Predictions, Contact
- [ ] Remove: Long explanations, redundant sections, promotional language
- [ ] Add: Clear badges (Status, License, CI, Sample Size)
- [ ] Structure: Problem → Solution → Evidence → Usage → Contact

### Core Documentation - Consolidate
- [ ] **witness-threshold-v5.md** - Keep as comprehensive technical paper
- [ ] Move all "lore" content to `private/` (not public-facing)
- [ ] Ensure `docs/` contains only: framework, benchmark spec, replication protocol
- [ ] Remove duplicate explanations across files

---

## PHASE 2: REPOSITORY STRUCTURE (Clean Up)

### Git Cleanup
- [ ] Commit or discard uncommitted changes in `README.md`, `backend/stripe_webhook.py`, `backend/tests/test_stripe_webhook.py`
- [ ] Delete or move to `private/`: `docs/streams/articles/inbox/2025-11-27-resonance-era-thanksgiving-20251127-212148.md`
- [ ] Update `.gitignore` - ensure `private/`, `models/`, training data are excluded
- [ ] Run `scripts/restructure_repo.sh --dry-run` → review → `--apply`
- [ ] Clean commit messages for recent history
- [ ] Merge current branch to `main` or create clean feature branch

### File Organization
- [ ] Move all drafts/working docs to `private/drafts/`
- [ ] Move all worldbuilding/narrative to `private/lore/`
- [ ] Keep only essential public docs in `docs/`:
  - `witness-threshold/` (v5.0 paper)
  - `sar_benchmark/` (spec + usage)
  - `replication-protocol.md`
  - `falsification.md`
- [ ] Verify no sensitive/personal content in public files

---

## PHASE 3: CODE & TESTS (Quality Check)

### Testing
- [ ] Fix pytest exit code 127 error (venv activation issue?)
- [ ] Run full pytest suite - fix all failures
- [ ] Run linting: `black .` and `ruff check --fix`
- [ ] Verify combat demo runs successfully
- [ ] Test SAR benchmark runner: `python benchmarks/sar_benchmark/run_sar.py`

### CI/CD
- [ ] Merge PR #80 (scheduled Grok diagnostic) - **RECOMMENDED**
- [ ] Verify CI passes on `main` branch
- [ ] Confirm dry-run mode works for Grok (until DNS resolves)
- [ ] Monitor scheduled diagnostic runs (daily checks)

---

## PHASE 4: LAUNCH PREP (Final Polish)

### Essential Documents Only
- [ ] **README.md** - Clean, professional, focused (see Phase 1)
- [ ] **STRUCTURAL_INSURRECTION_PUBLIC_ARTIFACT.md** - Verify contact info, links
- [ ] **EMAIL_TEMPLATES.md** - Confirm all templates ready (OpenAI, Anthropic, DeepMind, BestSelf)
- [ ] Verify GitHub repo is public-ready (no private data exposed)

### Contact Information
- [ ] Confirm email in all public docs: `KaznakAlpha@elidorascodex.com`
- [ ] Verify ORCID: `0009-0000-7615-6990`
- [ ] Add GitHub profile link if desired

---

## PHASE 5: LAUNCH EXECUTION (January 7, 2026)

### Tier 1 - Research Labs (Send Simultaneously)
- [ ] **OpenAI** - `partnerships@openai.com`
  - Subject: "The Missing Alignment Layer – TGCR Witness Protocol"
  - Attach: Link to public artifact
  - Time sent: _____ | Confirmation: _____

- [ ] **Anthropic** - `contact@anthropic.com`
  - Subject: "The Missing Alignment Layer – TGCR Witness Protocol"
  - Attach: Link to public artifact
  - Time sent: _____ | Confirmation: _____

- [ ] **DeepMind** - `research@deepmind.com`
  - Subject: "Geometric Alignment for AGI – The TGCR Framework"
  - Attach: Link to public artifact
  - Time sent: _____ | Confirmation: _____

### Tier 1.5 - BestSelf (HIGH PRIORITY LOCAL PILOT)
- [ ] **BestSelf Behavioral Health** - TBD contact
  - Subject: "Tool to Support Your Mission (From Someone Who Knows Your Work)"
  - Pitch: Full-circle narrative (built KEDS infrastructure at 17, now offering pilot)
  - Attach: Clinical validation protocol
  - Time sent: _____ | Confirmation: _____

### Public Release
- [ ] Publish Substack Post 1: "The Structural Insurrection"
  - Set to FREE tier
  - Link to GitHub repo
  - Time published: _____ | URL: _____

- [ ] Social Media (Optional)
  - X/Twitter thread (12 tweets)
  - LinkedIn post
  - Link to Substack + GitHub

### Tracking
- [ ] Log all sends in `EMAIL_CAMPAIGN.md`
- [ ] Update status for each email: "Sent - Jan 7"
- [ ] Note follow-up dates (2 weeks = Jan 21)

---

## PHASE 6: FOLLOW-UP & MONITORING

### Week 1-2 (Jan 7-20)
- [ ] Monitor email for responses
- [ ] Check Substack engagement
- [ ] Watch GitHub Actions - Grok diagnostic status
- [ ] Track social media metrics

### Week 3 (Jan 21-27) - First Follow-Up
- [ ] Send gentle follow-up if no response:
  - Subject: "RE: The Missing Alignment Layer – Status Update"
  - Brief: "Confirming you received TGCR proposal. Happy to discuss."
- [ ] Log follow-up attempts

### Week 6+ (Feb onwards)
- [ ] Second follow-up if still no response
- [ ] Offer 30-minute technical call
- [ ] Publish Substack Post 2 (optional)

---

## PHASE 7: VALIDATION & EXPANSION (Post-Launch)

### Independent Validation
- [ ] Track replication attempts from other researchers
- [ ] Document null results (just as valuable as positive)
- [ ] Update QC reports with live data when Grok DNS resolves

### Academic Path (Optional)
- [ ] Run `./prepare_arxiv_submission.sh` (if pursuing preprint)
- [ ] Validate with `./validate_arxiv_submission.sh`
- [ ] Submit to arXiv
- [ ] Add arXiv ID to `papers/tgcr/ARXIV_SUBMISSION_ID.txt`
- [ ] Create GitHub release with tarball

### Pilot Expansion
- [ ] If BestSelf responds positively → launch pilot
- [ ] IRB submission (if needed)
- [ ] Consent & data policies documented
- [ ] Deploy staging demo (isolated, secure)

---

## SKIPPED / NOT PURSUING

- ❌ DARPA/IARPA submissions (not pursuing yet)
- ❌ Grok/X outreach (DNS monitoring handles it automatically)
- ❌ Live deployment (pilot not ready without partner)
- ❌ Personal narrative in public docs (moving to `private/`)

---

## SUCCESS CRITERIA

### Week 1-2
- ✅ All emails sent successfully
- ✅ Substack published
- ✅ GitHub repo receiving traffic

### Month 1-2
- ✅ At least 1 research team requests call/meeting
- ✅ BestSelf responds (local pilot opportunity)
- ✅ Substack reaches 50+ subscribers

### Month 3-6
- ✅ Pilot integration agreement signed
- ✅ Peer-reviewed submission or preprint published
- ✅ Independent replication attempts documented

---

## IMMEDIATE NEXT ACTIONS (Pick One)

**A) Clean README.md now** (15 minutes)
- Strip personal narrative
- Focus on work only
- Structure: Problem → Solution → Evidence → Usage

**B) Merge PR #80** (1 minute)
- Scheduled Grok diagnostic
- Automatic DNS monitoring
- **RECOMMENDED: Do this first**

**C) Git cleanup** (30 minutes)
- Commit/discard uncommitted changes
- Run restructure script
- Clean repo state

**D) Draft BestSelf email** (20 minutes)
- Local pilot opportunity
- Full-circle narrative
- High-impact partnership

---

*This checklist consolidates existing launch and deployment checklists into a single master document for clarity and execution.*
