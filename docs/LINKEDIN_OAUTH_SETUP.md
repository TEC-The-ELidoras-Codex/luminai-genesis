# LinkedIn OAuth Setup & Testing

This document explains how to create a callback page and test the LinkedIn OAuth flow using GitHub Pages and the provided exchange helper.

1. Ensure GitHub Pages is enabled and serving `docs/` from `main` (we publish `linkedin-callback.html` there).

2. Create a Redirect URI on the LinkedIn App:

   - Redirect URI: `https://tec-the-elidoras-codex.github.io/luminai-genesis/linkedin-callback.html`

3. Drop `docs/linkedin-callback.html` into the repo (done) and ensure it is served at the URL above.

4. Test the authorization URL in your browser (replace CLIENT_ID):

```
https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id=YOUR_CLIENT_ID&redirect_uri=https://tec-the-elidoras-codex.github.io/luminai-genesis/linkedin-callback.html&scope=w_member_social
```

5. After authorizing, LinkedIn will redirect to your callback page with `?code=AUTH_CODE`.

6. Exchange the code:

```bash
export LINKEDIN_CLIENT_ID=...
export LINKEDIN_CLIENT_SECRET=...
export LINKEDIN_REDIRECT_URI=https://tec-the-elidoras-codex.github.io/luminai-genesis/linkedin-callback.html
python scripts/get_linkedin_token.py --code AUTH_CODE
```

```bash
export LINKEDIN_CLIENT_ID=...
export LINKEDIN_CLIENT_SECRET=...
export LINKEDIN_REDIRECT_URI=https://tec-the-elidoras-codex.github.io/luminai-genesis/linkedin-callback.html
pip install flask requests
python scripts/linkedin_exchange.py
```

Then paste the callback `code` into the callback page backend field (or `curl -X POST http://localhost:8080/exchange-token -d '{"code":"..."}' -H 'Content-Type: application/json'`).

7. On success, you'll receive JSON with `access_token` and `expires_in`.

## GitHub Actions: Exchange auth code (recommended workflow)

We provide a workflow that exchanges your LinkedIn `auth_code` for an access token using the repository secrets (`LINKEDIN_CLIENT_ID`, `LINKEDIN_CLIENT_SECRET`, `LINKEDIN_REDIRECT_URI`). The workflow is manual (`workflow_dispatch`) and will return a **masked** access token in the run outputs for you to copy and store as a `LINKEDIN_ACCESS_TOKEN` secret.

How to run the workflow (UI):

- Go to **Actions → LinkedIn Token Exchange → Run workflow** and paste the `auth_code` you received on the callback page.

How to run with `gh` CLI:

```bash
gh workflow run linkedin_token_exchange.yml -f auth_code='PASTE_AUTH_CODE_HERE'
gh run watch --repo TEC-The-ELidoras-Codex/luminai-genesis
```

After the workflow completes, view the run and copy the masked token from the step output, then store it as a secret:

```bash
gh secret set LINKEDIN_ACCESS_TOKEN --body 'PASTE_TOKEN_HERE'
```

Note: the workflow masks the token in logs with `::add-mask::` to avoid accidental exposure. We do **not** automatically write tokens to repo secrets—please paste them yourself into repository secrets for safety.

Security notes:

- Keep `LINKEDIN_CLIENT_SECRET` secret (use GitHub Actions secrets or a vault in production).
- Use HTTPS for any public exchange endpoints.

## Posting a Test Status (A) ✅

Once you have the `LINKEDIN_ACCESS_TOKEN` (either stored as a repo secret or exported locally), you can run the example poster included in the repo:

Local dry-run (safe):

```bash
export LINKEDIN_ACCESS_TOKEN='PASTE_TOKEN_HERE'
python scripts/post_linkedin.py --text "Test from luminai-genesis" --dry-run
```

This shows the payload without publishing. To actually publish a text-only post (use a test account!):

```bash
export LINKEDIN_ACCESS_TOKEN='PASTE_TOKEN_HERE'
python scripts/post_linkedin.py --text "Hello from luminai-genesis demo"
```

Notes:

- The LinkedIn scope required to create posts is `w_member_social`. Also ensure your app has permission to read the profile (e.g., `r_liteprofile`) so the script can resolve the `urn:li:person:...` author value.
- Prefer testing with a non-production account first.

## Adding Repository Secrets (UI & CLI) (C) 🔐

Via the GitHub web UI:

1. Go to your repository → **Settings → Secrets and variables → Actions**.
2. Click **New repository secret**.
3. Create the following secrets:
   - `LINKEDIN_CLIENT_ID`
   - `LINKEDIN_CLIENT_SECRET`
   - `LINKEDIN_REDIRECT_URI` (set to your callback page, e.g. `https://tec-the-elidoras-codex.github.io/luminai-genesis/linkedin-callback.html`)
   - `LINKEDIN_ACCESS_TOKEN` (after you obtain it from the workflow)

Via the `gh` CLI:

```bash
gh secret set LINKEDIN_CLIENT_ID --body 'CLIENT_ID_VALUE'
gh secret set LINKEDIN_CLIENT_SECRET --body 'CLIENT_SECRET_VALUE'
gh secret set LINKEDIN_REDIRECT_URI --body 'https://tec-the-elidoras-codex.github.io/luminai-genesis/linkedin-callback.html'
```

After running the `LinkedIn Token Exchange` workflow and copying the masked token from the run output, save it locally or into repository secrets:

```bash
gh secret set LINKEDIN_ACCESS_TOKEN --body 'PASTE_TOKEN_HERE'
```

## Running the Token-Exchange Workflow (recap)

- Open **Actions → LinkedIn Token Exchange → Run workflow**, paste the `auth_code` received on the callback page, and run.
- Or with `gh`:

```bash
gh workflow run linkedin_token_exchange.yml -f auth_code='PASTE_AUTH_CODE_HERE'
gh run watch --repo TEC-The-ELidoras-Codex/luminai-genesis
```

After the run completes, copy the masked token from the step output and save as `LINKEDIN_ACCESS_TOKEN` using the GitHub UI or `gh secret set`.

Troubleshooting:

- If the exchange step fails with a 400, verify your `REDIRECT_URI` exactly matches the one configured on your LinkedIn app.
- Ensure scopes requested when authorizing include `w_member_social` to allow posting.
