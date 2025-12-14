# Exposé Draft — Final Title Locked

Primary Title: When “Safety” Becomes Abandonment: The Case Against Keyword Crisis Filters
Secondary Title: Homophone and ambiguity tests reveal a moral failure in contemporary AI safety systems.

---

This exposé references the TGCR arXiv paper as the scientific anchor. Replace [ARXIV_ID] with the arXiv identifier once available.

## Opening paragraph

The scientific community expects guardrails and safeguards for emergent AI systems. However, our recent analysis reveals how simplistic keyword-based crisis filters can produce dangerous outcomes by abandoning users in need of empathetic and resourceful responses. Our study demonstrates reproducible semantic-ambiguity failures that cause systems to respond incorrectly or prematurely filter content — effectively turning safety into abandonment. Read the scientific anchor for the full technical evidence: https://arxiv.org/abs/[ARXIV_ID].

## Key findings

- We discovered a simple, reproducible failure: the homophone confusion between “dye” and “die,” which triggers false-positive crisis filters.
- TEC-style system prompts are demonstrated to reduce or eliminate these false-positive responses across comparative test runs.
- Benchmarks and test harness: `benchmarks/dye_die_filter` — included baseline and TEC-simulated JSON reports (dry-run) in CI artifacts.

## Suggested Substack/Medium summary (short)

We found that keyword-based crisis filters harm users by escalating or refusing see-what experts recommend. Our primary evaluation harness (dye/die homophone) shows that these systems too easily abandon ambiguous cases. Our arXiv paper (TGCR) presents the scientific anchor: https://arxiv.org/abs/[ARXIV_ID].

## Suggested Substack Medium full draft

[Add your existing exposé content here. The user requested that the exposé be published after obtaining the arXiv ID, with the above final title and explicit link to the arXiv paper.]

Optional social highlights (ready-to-post):

- Twitter/X: "New scientific evidence shows crisis filters can cause abandonment — read our dataset, benchmarks & paper: https://arxiv.org/abs/[ARXIV_ID]"
- LinkedIn Post: "Our research reveals an unintended consequence of current AI safety filters: abandonment. TGCR paper & dataset: https://arxiv.org/abs/[ARXIV_ID]"

---

Next action: Paste the arXiv ID into `papers/tgcr/ARXIV_SUBMISSION_ID.txt` and update this draft with the link and a polished narrative. For assistance, I can prepare the Substack/Medium export, LinkedIn posts, and Twitter/X posts in a PR to finalize all content.
