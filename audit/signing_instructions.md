Signing Instructions — Create a PGP detached signature for `audit/evidence_bundle.zip`

You requested a signed archive. I created an unsigned ZIP at:

- `audit/evidence_bundle.zip`
- SHA256 checksum file: `audit/evidence_bundle.sha256`

I cannot sign with your private key. Below are safe, copy-paste commands you can run locally to create a PGP detached signature (recommended) or create a new GPG key if you don't have one.

A. If you already have a GPG key (recommended)

1. List your keys to confirm the key ID to use:

```bash
gpg --list-secret-keys --keyid-format LONG
```

2. Create a detached, ASCII-armored signature for the ZIP (replace `YOUR_KEY_ID` if needed):

```bash
gpg --default-key YOUR_KEY_ID --output audit/evidence_bundle.zip.sig --detach-sign --armor audit/evidence_bundle.zip
```

3. Verify the signature (anyone with your public key can run this):

```bash
gpg --verify audit/evidence_bundle.zip.sig audit/evidence_bundle.zip
```

B. If you do NOT have a GPG key and want to create one (quick)

1. Create a new key (follow prompts):

```bash
gpg --full-generate-key
```

2. Then run the `--detach-sign` step from A.

C. If you prefer SHA256+timestamp proof only (no PGP)

1. I already created `audit/evidence_bundle.sha256` containing the checksum. You can publish that alongside the ZIP.
2. For immutability/timestamping, consider stamping the SHA256 record into a public immutability service (OpenTimestamps) or anchoring it on a blockchain-based timestamping service.

D. Recommended public distribution pattern

- Publish `audit/evidence_bundle.zip` and `audit/evidence_bundle.sha256` to the public release or a verified location.
- Publish `audit/evidence_bundle.zip.sig` (PGP detached signature) so others can verify with your public key.
- Publish your GPG public key (or a key fingerprint) so media and counsel can verify signatures.

If you want, I can:

- Generate a `zip` plus `sha256` (done).
- Create a draft `git tag` and release notes referencing these artifacts.
- Help you create a PGP key locally (guide) or prepare a GPG command snippet customized to your chosen key id.

Tell me which of the above you'd like me to do next.
