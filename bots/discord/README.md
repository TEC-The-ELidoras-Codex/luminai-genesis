Discord bot (minimal)

This folder contains a minimal discord.py bot that responds to `!ping` with `Pong!`.

Environment variables:

- DISCORD_BOT_TOKEN — bot token from the Discord developer portal

Quick run:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export DISCORD_BOT_TOKEN="your-token-here"
python bot.py
```

Notes:

- Make sure the bot has `MESSAGE CONTENT INTENT` enabled in Discord Developer Portal if you want it to read message content.
- For production, use a process manager (systemd, Docker, or a host like Fly.io) and securely store the token in environment variables.
