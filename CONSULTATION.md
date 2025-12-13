# Consultation & Booking — LuminAI Genesis

This document contains copy-paste-ready text and implementation options to make the consultation offer actionable on the public README, website, or social channels.

## Quick Link (copy-paste)

If you want the fastest route, create a Stripe Payment Link in your Stripe dashboard and paste the URL below.

```markdown
## 💼 Book a Consultation

Building gradient-based safety systems requires specialized expertise. I offer paid consultations to help teams integrate TGCR, remediate false positives, and design persona-aware safety layers.

• **What I consult on:** TGCR integration, false positive analysis, custom persona-aware safety layers, architecture reviews.
• **Rate:** $150 / hour

👉 **Book Now (Calendly + Payment):** https://calendly.com/elidorascodex

If you prefer Stripe Payment Links instead of Calendly's payment integration, create a Stripe Payment Link and paste it below. After payment I recommend redirecting users to the Calendly URL above so they can schedule a time automatically.
```

## Stripe Product Description (copy-paste)

Use this when creating a Product in Stripe or a Payment Link description.

Title: LuminAI Genesis Consultation (1 hour)

Description (short): 1-hour consulting session — TGCR integration, false positive remediation, and persona-aware safety architecture.

Description (long): Deep-dive consultation on integrating the Theory of General Contextual Resonance (TGCR) into your system, diagnosing false-positive safety failures, and designing persona-aware safety layers. Includes a follow-up email with 2-3 action items and resource links. Price includes a 1-hour video call and a 1-page follow-up summary.

Price: $150.00 USD

Processing notes: Use Test Mode to verify flow before going live. Optionally redirect users on success to a Calendly booking page.

## Calendly + Stripe (recommended)

If you prefer an integrated booking + payment flow, create a Calendly event and connect Stripe to Calendly (Calendly Pro required for Stripe integration). Set the event price to $150 and require payment prior to booking. Use the Calendly public URL in your README.

Calendly CTA (copy-paste):

```markdown
👉 **[Book Now — Payment + Calendar (Calendly)](https://calendly.com/elidorascodex)**
```

## Local webhook testing (developer)

If you want to test webhook handling locally (recommended) use the Stripe CLI to forward events.

1. Create a local env file (example `.env.local`):

```bash
export STRIPE_SECRET_KEY="sk_test_..."
export STRIPE_WEBHOOK_SECRET="whsec_..."
```

2. Start the app locally:

```bash
pip install -r requirements.txt
uvicorn backend.main:app --reload --port 8000
```

3. In another terminal start Stripe CLI forwarding:

```bash
stripe listen --forward-to http://localhost:8000/webhook
```

4. Trigger a test event (checkout.session.completed):

```bash
stripe trigger checkout.session.completed
```

The webhook will log sessions to `/tmp/stripe_sessions.log` and call the placeholder email routine. If you don't set `STRIPE_WEBHOOK_SECRET` locally the handler will parse payloads without signature verification (development only).

## Post-payment Email Template (copy-paste)

Subject: LuminAI Genesis Consultation Confirmed — Let's Schedule

Hi [Name],

Thank you for booking a consultation! Your payment of $150 has been confirmed.

Next step: Please pick a time here: https://calendly.com/your-username/luminai-consultation

Before our call, please reply with a brief (3-sentence) summary of:

1. What you're building
2. The safety challenge you are facing
3. What success looks like

I'll prepare tailored examples and bring a short action plan to our session.

— Angelo (The Elidoras Codex)

## LinkedIn / X Announcement (copy-paste)

Short LinkedIn post (good for TL;DR):

> I'm opening a small number of 1-hour consultation slots to help teams integrate principled AI safety without hiding behind 'refusal'. LuminAI Genesis uses TGCR + Persona Law to diagnose false positives and design safer, more humane models. Book: https://calendly.com/elidorascodex — details & case studies: https://polkin.substack.com

X (Twitter) thread starter (4 tweets):

1/ I'm opening a small number of consulting slots to help teams operationalize AI safety without hiding behind 'refusal'. LuminAI Genesis is about presence, not avoidance. Read more: https://polkin.substack.com
2/ I consult on TGCR integration, false-positive remediation, and persona-aware safety layers. Practical, actionable, and tailored to your stack.
3/ $150/hour — payment supports open-source work. Book here: https://calendly.com/elidorascodex
4/ Reply or DM with questions. I'll also post a few case studies from recent work soon.

## Next steps checklist

- [ ] Create Stripe Payment Link (or Calendly event with Stripe)
- [ ] Test the flow in Stripe Test Mode
- [ ] Paste live link into `README.md` (replace placeholder)
- [ ] Test the booking flow end-to-end
- [ ] Optionally: add a dedicated `/consultation` page with embedded Calendly or Stripe Checkout

---

If you'd like, I can: (A) create the Payment Link & Calendly copy for you, (B) commit the live link into `README.md`, and (C) draft the LinkedIn/X announcement tailored to your voice and audience. Tell me which.
