import discord
from discord.ext import commands, tasks
import os
import asyncio
from dotenv import load_dotenv

load_dotenv(".env")
TOKEN: str = os.getenv("TOKEN")

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

@bot.event
async def on_ready():
    guild_count = len(bot.guilds)
    activity = discord.Activity(type=discord.ActivityType.watching, name=f"over {guild_count} servers")
    await bot.change_presence(activity=activity)
    print("Bot online!")
    try:
        synced_commands = await bot.tree.sync()
        print(f"Synced {len(synced_commands)} commands!")
    except Exception as e:
        print(f"Error syncing application commands: ", e)

@tasks.loop(hours=1)
async def update_status():
    guild_count = len(bot.guilds)
    activity = discord.Activity(type=discord.ActivityType.watching, name=f"over {guild_count} servers")
    await bot.change_presence(activity=activity)


@bot.tree.command(name="hello", description="says hello back to the person who executed the command")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"{interaction.user.mention}, hello there!")

async def load():
    for filename in os.listdir("cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")

async def main():
    async with bot:
        await load()
        await bot.start(TOKEN)

asyncio.run(main())