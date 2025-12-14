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

- Option A (manual CLI):

  ```bash
  export LINKEDIN_CLIENT_ID=...
  export LINKEDIN_CLIENT_SECRET=...
  export LINKEDIN_REDIRECT_URI=https://tec-the-elidoras-codex.github.io/luminai-genesis/linkedin-callback.html
  python scripts/get_linkedin_token.py --code AUTH_CODE
  ```

- Option B (server exchange): run the small Flask server:

  ```bash
  export LINKEDIN_CLIENT_ID=...
  export LINKEDIN_CLIENT_SECRET=...
  export LINKEDIN_REDIRECT_URI=https://tec-the-elidoras-codex.github.io/luminai-genesis/linkedin-callback.html
  pip install flask requests
  python scripts/linkedin_exchange.py
  ```

  Then paste the callback `code` into the callback page backend field (or `curl -X POST http://localhost:8080/exchange-token -d '{"code":"..."}' -H 'Content-Type: application/json'`).

7. On success, you'll receive JSON with `access_token` and `expires_in`.

Security notes:

- Keep `LINKEDIN_CLIENT_SECRET` secret (use GitHub Actions secrets or a vault in production).
- Use HTTPS for any public exchange endpoints.
