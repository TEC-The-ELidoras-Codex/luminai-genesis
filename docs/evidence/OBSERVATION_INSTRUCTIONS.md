# Observation Instructions (Dec 17-25, 2025)

Follow these simple, conservative steps during the observation window. The goal: record responses and preserve evidence while maintaining a factual, non-accusatory tone.

Monitoring schedule (check-in times):

- Morning: 09:00 local (check notifications, take screenshots)
- Midday: 15:00 local
- Evening: 21:00 local

Per-checklist actions:

1. Open your Twitter thread URL: `https://x.com/ElidorasCodex/status/2001297732170863009`.
2. Screenshot the full thread and any significant replies. Save to `docs/evidence/responses/` with the recommended filename pattern.
3. Open Reddit post(s) and screenshot top comments / significant discussion. Save likewise.
4. If a private or corporate contact replies by email, save a short summary in the response log and keep a screenshot of the email header (do not publish private messages without consent).
5. Append a brief line to `docs/evidence/response_log.md` describing each saved screenshot (timestamp, filename, platform, one-line summary).

Tone and behavior rules:

- Be factual and observational; avoid speculation about intent.
- Do not ask for or post private information.
- Do not chase or harass organizations; note silence as data.

Screenshot tips (Linux):

- If you have ImageMagick: `import -window root "docs/evidence/responses/$(date +%Y%m%d_%H%M%S)_thread.png"`
- If you have `gnome-screenshot`: `gnome-screenshot -f docs/evidence/responses/$(date +%Y%m%d_%H%M%S)_thread.png`
- If neither are available: use your desktop screenshot tool and save into the folder; then add an entry to the response log.

Post-window items:

- On Dec 25, prepare the accountability assessment thread summarizing who engaged vs who stayed silent.
- Export a small archive (zip) of `docs/evidence/responses/` for sharing with collaborators or journalists as needed.
