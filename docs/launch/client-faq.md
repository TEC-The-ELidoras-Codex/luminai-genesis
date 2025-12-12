# Quantum Security — Client FAQ

**Document:** client-faq.md
**Last updated:** 2025-12-11

Q: What does "quantum-resistant" mean?  
A: It means we use cryptographic algorithms and key-management practices that are designed to remain secure even if large-scale quantum computers become available.

Q: Do you already use quantum computers to encrypt my data?  
A: No. We use post-quantum cryptographic algorithms (classical algorithms designed to resist quantum attacks) and are piloting QKD for specialized links.

Q: Will this slow down my experience?  
A: For most users no — PQC computations are modestly more expensive but engineered at the protocol layer to minimize client impact. We use hybrid modes to preserve compatibility.

Q: How do I verify your claims?  
A: We publish audit summaries annually and can provide additional technical documentation to enterprise customers under NDA.

Q: What happens if an algorithm is broken?  
A: We have an algorithm deprecation and key rotation policy; we'll re-encrypt affected data and notify impacted customers per our SLA.

Q: Who should I contact with security questions?  
A: security@luminai.tech
