import logging
import os

import discord
from discord.ext import commands

TOKEN = os.environ.get("DISCORD_BOT_TOKEN")
logger = logging.getLogger(__name__)
if not TOKEN:
    logger.warning("DISCORD_BOT_TOKEN not set. The bot will not connect.")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    logger.info("Discord bot connected as %s (id=%s)", bot.user, bot.user.id)


@bot.command(name="ping")
async def ping(ctx):
    await ctx.send("Pong!")


if __name__ == "__main__":
    if TOKEN:
        bot.run(TOKEN)
    else:
        logger.error("No DISCORD_BOT_TOKEN provided. Exiting.")
