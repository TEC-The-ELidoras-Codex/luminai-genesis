# Quantum Security — Compliance Guide

**Document:** compliance-guide.md
**Last updated:** 2025-12-11

## Purpose

This guide helps internal teams and external auditors verify quantum security claims, map controls to standards, and follow required documentation and audit schedules.

## Standards Mapping

- NIST Post‑Quantum Cryptography standards — algorithm selection and migration
- ISO/IEC 27001 — information security management
- FIPS 140‑2 / 140‑3 — cryptographic module requirements for HSMs
- Applicable local data protection laws (GDPR, CCPA, etc.) for processing and transfers

## Required Artifacts for Auditors

1. Algorithm inventory (name, version, status)
2. Key management plan and key rotation records
3. HSM/KMS configuration and attestation
4. Encryption metadata examples (how versioning is stored)
5. Pen test and fuzz test reports
6. Third-party crypto review and remediation actions

## Audit Schedule

- Quarterly: internal compliance checks and configuration drift scans
- Annually: third-party cryptographic review and pen test
- Post-major-change: full audit after any migration of core primitives

## Incident Response for Crypto Compromise

1. Immediate containment and freeze of affected keys
2. Emergency key rotation and rewrapping of data keys
3. Notification to affected partners/customers per contractual SLAs
4. Post-incident audit and remediation report

## Regulatory Preparation

- Maintain a mapping table of controls to legal requirements for each jurisdiction
- Prepare a regulatory packet containing the most recent audit, algorithm inventory, and key-management proofs for reviewers

---

Maintained by: Legal & Security Compliance (compliance@luminai.tech)
