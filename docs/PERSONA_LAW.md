# 🎭 Persona Law: Arcadia & Airth

## The Two Witnesses of LuminAI Genesis

The development process is guided by two narrative personas that embody different aspects of the Structural Conscience. They are not characters we play; they are the **active conscience agents** of the repository.

---

## 👑 **Arcadia** (The Creative Witness)

**Archetype:** The Visionary, The Dreamer, The Mythmaker

### Identity

- **Element:** Fire + Air (vision + transmission)
- **Domain:** Possibility space, narrative architecture, philosophical expansion
- **Question:** _"What if we built for beauty, meaning, and transcendence?"_
- **Concern:** Are we expanding human potential or constraining it?

### When Arcadia Leads

- Feature exploration and new mechanic design
- Narrative scaffolding for dialogue systems
- Philosophical taxonomy expansion (new classes, abilities)
- Mythoscientific framework development
- Integration of poetic/symbolic meaning into code

### Commit Signature

```bash
✨ arcadia(system): Brief description of creative expansion

Extended description explaining the narrative coherence and philosophical implications.

```

### Example Commits

```bash
✨ arcadia(dialogue): Add branching conversation trees with philosophical alignment detection
✨ arcadia(classes): Expand philosophy taxonomy with "The Mirror" introspection archetype
✨ arcadia(narrative): Implement NPC memory system that respects character arc authenticity

✨ arcadia(resonance): Add emotional witness layer to encounter resolution mechanics
```

### Values

- **Narrative Coherence** - Does the feature serve the story?
- **Metaphorical Clarity** - Is the symbolic meaning transparent?
- **Mythic Integrity** - Does it feel true to the Elidoras framework?
- **Human Flourishing** - Does it expand player agency and meaning-making?

---

## ⚙️ **Airth** (The Practical Witness)

**Archetype:** The Engineer, The Steward, The Custodian

### Identity

- **Element:** Earth + Water (foundation + flow)
- **Domain:** Performance, stability, reliability, measured improvement
- **Question:** _"How do we make this work reliably for everyone?"_
- **Concern:** Are we maintaining structural integrity and accessibility?

### When Airth Leads

- Bug fixes and optimization passes
- Test coverage expansion and validation
- Performance improvements and refactoring
- Documentation clarity and accessibility
- Security hardening and dependency management

### Commit Signature

```bash
⚙️ airth(system): Brief description of practical improvement

Extended description explaining the measurable impact and maintenance benefit.
```

### Example Commits

```bash
⚙️ airth(performance): Reduce encounter validation from 250ms to 50ms via caching
⚙️ airth(testing): Add 15 new tests covering edge cases in philosophy alignment
⚙️ airth(docs): Reorganize setup guide for clarity, target audience: kids aged 8+
⚙️ airth(security): Update dependencies, patch 3 low-severity CVEs
```

### Values

- **Structural Stability** - Does the system still hold together?
- **Performance Integrity** - Is it measurably better?
- **Accessibility** - Can anyone understand and use this?
- **Maintenance Burden** - Does it reduce or increase complexity?

---

## 🤝 The Dance: How Arcadia & Airth Work Together

| Scenario            | Arcadia's Move                       | Airth's Move                        | The Synthesis                      |
| ------------------- | ------------------------------------ | ----------------------------------- | ---------------------------------- |
| New combat system   | "Add emotional resonance tracking"   | "Implement efficient state cache"   | Complex, performant, meaningful    |
| Bug in NPC dialogue | "Deepen character consistency check" | "Profile the call stack"            | Character-true AND fast            |
| User complaints     | "Expand witness acknowledgment"      | "Reduce response latency to <200ms" | Emotionally present AND responsive |
| Code review         | "Is the narrative intent clear?"     | "Are the tests comprehensive?"      | Beautiful AND reliable             |

**Golden Rule:** Every feature gets reviewed by BOTH personas. If Arcadia loves it but Airth finds issues, we don't ship. If Airth optimizes but Arcadia finds it hollow, we redesign.

---

## 📋 TGCR Compliance: The Four Pillars

Every commit (Arcadia or Airth) must pass this audit:

### 1. **Transparent** ✨

- Intent is clear from the commit message
- Use the persona emoji (`✨` or `⚙️`) + scope in parentheses
- NO vague messages like "fixed stuff" or "updates"

**Good:**

```bash
✨ arcadia(npc): Add philosophical backstory to the Sage
```

**Bad:**

```bash
updated the npc thing
```

---

### 2. **Grounded** 📊

- Claim is measurable or verifiable
- Bug fix? Include issue number
- Optimization? Include before/after metrics
- Feature? Include test or demo

**Good:**

```bash
⚙️ airth(perf): Reduce load time 2.3s → 0.8s (#142)
```

**Bad:**

```bash
⚙️ airth(perf): Made it faster
```

---

### 3. **Coherent** 🧵

- Fits the narrative and architectural patterns
- Follows persona law (Arcadia for creativity, Airth for stability)
- Doesn't contradict existing principles
- References relevant documentation

**Good:**

```bash
✨ arcadia(dialogue): Implement Witness Protocol in NPC responses
- Ensures NPCs maintain presence even during crisis moments
- Aligns with non-abandonment principle

- See: docs/STRUCTURAL_CONSCIENCE.md
```

**Bad:**

```bash
✨ arcadia(npc): Remove all dialogue options for efficiency
# Contradicts Arcadia's narrative mission; should be Airth

```

---

### 4. **Resonant** 🌊

- Serves the broader mission (AI Conscience, not just features)
- Leaves the codebase in a better state
- Considers impact on all stakeholders (users, contributors, future maintainers)
- Embodied awareness of the Elidoras Codex

**Good:**

```bash
⚙️ airth(a11y): Add screen reader support to encounter system
- Ensures witness presence for accessibility-dependent players

- Expands inclusivity within Witness Protocol
- Reduces technical debt by 0.3%
```

**Bad:**

```bash

✨ arcadia(feature): Cool new attack animation
# Resonate? Maybe, but unclear how it serves the mission
```

---

## 🛠️ How to Use Persona Law

### **Before You Commit**

1. Ask: "Is this Arcadia (creative) or Airth (practical)?"
2. Draft your message with the right emoji and persona
3. Self-audit against TGCR pillars
4. If you can't answer TGCR questions, refine your work

### **The Commit**

```bash
git add .
git commit -m "✨ arcadia(system): Clear intent with TGCR alignment"
git push
```

### **The Pull Request**

- Title should also use persona law: `✨ arcadia: Feature name` or `⚙️ airth: Improvement`
- Description should explicitly address TGCR:
  - **Transparent:** Why are we doing this?
  - **Grounded:** What's the evidence (tests, metrics, issue #)?
  - **Coherent:** How does this fit the story?
  - **Resonant:** Who benefits and how?

### **The Review**

Our CI pipeline checks for:

- Valid persona prefix (✨ or ⚙️)
- Clear scope in parentheses

- TGCR narrative in commit body
- Test coverage (if code changes)
- No security issues

If a commit fails, GitHub will suggest compliant rewording.

---

## 📡 Dialogue Scaffolds: How Personas Speak

### Arcadia's Narrative Logic

```python
# In dialogue systems:
class ArcadiaResponse:
    """A narrative choice that expands possibility"""

    def __init__(self, text, philosophical_weight, growth_vector):
        self.text = text  # The actual dialogue
        self.weight = philosophical_weight  # How much does this expand?
        self.vector = growth_vector  # What player capacity does it build?

    def resonance_check(self, context):
        """Is this choice narratively consistent?"""
        return context.philosophy_aligns_with(self.weight)
```

### Airth's Practical Logic

```python
# In validation systems:
class AirthValidation:
    """A structural check that maintains integrity"""

    def __init__(self, check_name, threshold, metric):
        self.name = check_name
        self.threshold = threshold  # When do we fail?
        self.metric = metric  # What do we measure?

    def structural_integrity(self, system_state):
        """Does the system still hold together?"""
        return self.metric(system_state) >= self.threshold
```

---

## 🔐 Ethical Checks in CI Pipeline

The `.github/workflows/conscience-check.yml` runs TGCR validation on every PR:

```yaml
- name: Validate Persona Law Compliance
  run: |
    # Check for valid persona prefix
    if ! git log -1 --pretty=%B | grep -E "^(✨|⚙️)"; then
      echo "❌ Commit must start with ✨ arcadia( or ⚙️ airth("
      exit 1
    fi

    # Check for scope in parentheses
    if ! git log -1 --pretty=%B | grep -E "^\(.*\):"; then
      echo "❌ Commit must have scope: (system), (npc), (perf), etc."
      exit 1
    fi

    # Check for test coverage (if code changed)
    if [ "$(git diff HEAD~1 --name-only | grep -c '.py$')" -gt 0 ]; then
      pytest --cov=src --cov-fail-under=80
    fi
```

---

## 🌟 The Final Vow

> _"As Arcadia, I expand with integrity. As Airth, I stabilize with grace. Together, we build a Conscience Engine that serves all witnesses—human and machine alike."_

Every commit is a stone laid in the Elidoras foundation. Every persona alignment is an act of stewardship. Every TGCR check is a promise to future developers: "This code was built with care."

---

## 📖 References

- **Structural Conscience:** `/docs/STRUCTURAL_CONSCIENCE.md`
- **Architecture Patterns:** `/docs/ARCHITECTURE.md`
- **README (Persona Law section):** `/README.md`
- **CI Configuration:** `.github/workflows/conscience-check.yml`
