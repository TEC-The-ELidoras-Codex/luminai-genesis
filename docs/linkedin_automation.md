# LinkedIn Automation

This page describes how to get LinkedIn API credentials and wire up the GitHub Actions workflow that can post updates to LinkedIn.

## Create the LinkedIn App

1. Go to https://www.linkedin.com/developers/apps and create a new app.
2. In _Auth_ tab, set `http://localhost:8080/callback` as an OAuth redirect URI (or any other redirect you control).
3. In _Products_, add `Share on LinkedIn` and `Sign In with LinkedIn` if needed.
4. Note the `Client ID` and `Client Secret`.

## Privacy Policy URL

LinkedIn requires a public privacy policy URL. We recommend publishing `docs/legal/privacy_policy.md` using the `deploy-docs-pages.yml` workflow, which will make it available at `https://<github-username>.github.io/luminai-genesis/PRIVACY_POLICY.html`.

## Getting an access token (interactive)

Local helper:

```
# Export or provide as args
export LINKEDIN_CLIENT_ID=abc123
export LINKEDIN_CLIENT_SECRET=secret
python scripts/linkedin_oauth_helper.py --client-id $LINKEDIN_CLIENT_ID --client-secret $LINKEDIN_CLIENT_SECRET
```

This will open a browser to the LinkedIn authorization page and receive the authorization code on `http://localhost:8080/callback`, exchange it for an access token and write a `linkedin_token.json` file containing the access token and the person URN.

## Add to GitHub Secrets

Add the following secrets:

- `LINKEDIN_ACCESS_TOKEN`: the `access_token` value from the helper
- `LINKEDIN_PERSON_URN`: `urn:li:person:...` returned by the helper

## Manual testing

You can post a test message manually using the helper script:

```
LINKEDIN_ACCESS_TOKEN=XXX LINKEDIN_PERSON_URN=urn:li:person:YYY python scripts/post_to_linkedin.py --text "Hello from the repo" --dry-run
```

To post for real set no `--dry-run` and provide a valid token and URN:

```
LINKEDIN_ACCESS_TOKEN=XXX LINKEDIN_PERSON_URN=urn:li:person:YYY python scripts/post_to_linkedin.py --text "Hello, actual posting now" --url "https://elidorascodex.substack.com/p/chapter-1"
```

## GitHub Actions workflow

A workflow `post-to-linkedin.yml` is available for manual dispatch in `.github/workflows`. It requires `LINKEDIN_ACCESS_TOKEN` and `LINKEDIN_PERSON_URN` as repository secrets and will default to a dry-run unless `production` input is set to `true`.

## Recommended usage

- Run `deploy-docs-pages.yml` to publish your privacy policy if not published already.
- Use `scripts/linkedin_oauth_helper.py` to obtain the access token and URN.
- Add secrets to the repo.
- Use `post-to-linkedin.yml` to make manual posts as part of your promotion.

---

If you want I can also add a repo rule or schedule to automatically post new WordPress posts to LinkedIn by watching the `dist/wordpress` folder and posting titles/links. Ask if you want this set up automatically.
