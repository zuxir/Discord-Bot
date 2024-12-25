import discord
from discord.ext import commands
from discord import app_commands
import systemlogs

logger = systemlogs.logging.getLogger("bot")

class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

# Logging functionality for Utility Cog
    @commands.Cog.listener()
    async def on_ready(self):
        try:
            logger.info("Utility module successfully loaded!")
        except Exception as e:
            logger.error("Utility module failed to load: ", {e})

# Ping Command
    @app_commands.command(name="ping", description="Retrive the bot's ping (ms)")
    async def ping(self, interaction: discord.Interaction):
        # Check bot's latency
        latency = round(self.bot.latency * 1000)

        # Embed Design for "Ping" Response
        pingEmbed = discord.Embed(color=0x00b0f4)
        # pingEmbed.set_author(name="Lunar", icon_url=self.bot.user.avatar_url)
        pingEmbed.add_field(name="Ping", value=f"> {latency}ms", inline=False)
        
        await interaction.response.send_message(embed=pingEmbed)

async def setup(bot):
    await bot.add_cog(Utility(bot))