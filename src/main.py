import discord
from discord.ext import commands, tasks
from discord import app_commands
import os
import asyncio
from dotenv import load_dotenv
import systemlogs

logger = systemlogs.logging.getLogger("bot")

# Retrieves secrets from .env
load_dotenv(".env")
TOKEN: str = os.getenv("TOKEN")

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

# Bot Main Component
@bot.event
async def on_ready():
    logger.info(f"Bot is online as User: {bot.user} (ID: {bot.user.id})!")
    await bot.change_presence(activity=discord.CustomActivity(name="Coming Soon! 😉",))
    try:
        synced_commands = await bot.tree.sync()
        logger.info(f"Synced {len(synced_commands)} commands!")
    except Exception as e:
        logger.error(f"Error syncing application commands: ", e)

# Loads all cogs at each start
async def load_cogs():
    for filename in os.listdir("src/cogs"):
        if filename.endswith(".py"):
            try: 
                await bot.load_extension(f"cogs.{filename[:-3]}")
                logger.info(f"Loaded Cog: {filename}")
            except Exception as e:
                logger.error(f"Failed to load cog {filename}: {e}")

# Function to startup bot
async def main():
    async with bot:
        await load_cogs()
        await bot.start(TOKEN)

# Calls main() function
if __name__ == "__main__":
    asyncio.run(main())