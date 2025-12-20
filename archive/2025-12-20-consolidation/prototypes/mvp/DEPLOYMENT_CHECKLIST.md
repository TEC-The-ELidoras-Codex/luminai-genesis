# MVP Deployment Checklist (staging/demo)

Use this checklist before inviting human participants to any staging demo:

- [ ] Deploy to an isolated staging host (not public without approval).
- [ ] Set a secure `JWT_SECRET` and avoid the default `dev-secret-key`.
- [ ] Ensure the database folder is mounted and backups are configured.
- [ ] Limit access to the staging instance (IP allow list, VPN, or auth provider).
- [ ] Document consent and data retention policies clearly for pilot participants.
- [ ] Avoid collecting PHI until encryption, access controls, and policies are in place.
- [ ] Ensure a human clinician is available to respond to any safety escalations during pilot.
- [ ] Run integration tests and smoke tests (e.g., `npm test`) before opening to participants.

Reminder: This checklist is intentionally conservative — the current prototype is not production-ready and is designed to be used only for controlled pilots under supervision.
