Commit policy: private compiled books

- **Do not commit compiled PDFs or final compiled markdowns unless you explicitly authorize it.**
- Compiled PDFs (examples): `output/TEC_Book2_The_Vessel.pdf`, `output/book3_compiled.pdf`
- Final compiled markdowns pattern: `tec_book/*compiled.final.md`

If you *must* commit compiled books (rare, explicit decision by owner), do one of the following:
- Set the environment variable when committing:

  ALLOW_COMPILED_COMMIT=1 git commit -m "[allow-compiled] Commit compiled books (explicit consent)"

- Provide explicit approval in a PR description and coordinate with the repo owner.

Local protection:
- A local pre-commit hook blocks commits containing the above files by default. This hook is local-only and will not be pushed to remote automatically.

If you want this rule changed, tell me exactly how and I will update it.