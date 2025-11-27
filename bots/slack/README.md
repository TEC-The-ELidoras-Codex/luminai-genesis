Slack slash command handler (minimal)

This folder contains a minimal Flask app to receive Slack slash commands and verify the request signature.

Environment variables (use repository secrets or local `.env`):

- SLACK_SIGNING_SECRET — required to verify incoming requests from Slack
- PORT — (optional) port to run the web server (default 5000)

Quick run (in WSL or Linux):

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export SLACK_SIGNING_SECRET="your-signing-secret"
python app.py
```

In Slack App configuration, add an "Slash Command" with a Request URL like `https://<your-host>/slack/commands` and the command name you want (e.g., `/luminai`).
