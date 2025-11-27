import os
import discord
from discord.ext import commands

TOKEN = os.environ.get("DISCORD_BOT_TOKEN")
if not TOKEN:
    print("Warning: DISCORD_BOT_TOKEN not set. The bot will not connect.")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"Discord bot connected as {bot.user} (id={bot.user.id})")


@bot.command(name="ping")
async def ping(ctx):
    await ctx.send("Pong!")


if __name__ == "__main__":
    if TOKEN:
        bot.run(TOKEN)
    else:
        print("No DISCORD_BOT_TOKEN provided. Exiting.")
