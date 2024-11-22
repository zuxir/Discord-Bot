import discord
from discord.ext import commands, tasks
import os
import asyncio
from dotenv import load_dotenv
import systemlogs

logger = systemlogs.logging.getLogger("bot")

load_dotenv(".env")
TOKEN: str = os.getenv("TOKEN")

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.event
async def on_ready():
    logger.info(f"Bot is online as User: {bot.user} (ID: {bot.user.id})!")
    guild_count = len(bot.guilds)
    activity = discord.Activity(type=discord.ActivityType.watching, name=f"over {guild_count} servers")
    await bot.change_presence(activity=activity)
    try:
        synced_commands = await bot.tree.sync()
        logger.info(f"Synced {len(synced_commands)} commands!")
    except Exception as e:
        logger.error(f"Error syncing application commands: ", e)

@tasks.loop(hours=1)
async def update_status():
    guild_count = len(bot.guilds)
    activity = discord.Activity(type=discord.ActivityType.watching, name=f"over {guild_count} servers")
    await bot.change_presence(activity=activity)


@bot.tree.command(name="hello", description="says hello back to the person who executed the command")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"{interaction.user.mention}, hello there!")

async def load_cogs():
    for filename in os.listdir("src/cogs"):
        if filename.endswith(".py"):
            try: 
                await bot.load_extension(f"cogs.{filename[:-3]}")
                logger.info(f"Loaded Cog: {filename}")
            except Exception as e:
                logger.error(f"Failed to load cog {filename}: {e}")

async def main():
    async with bot:
        await load_cogs()
        await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())