# import discord
# from discord.ext import commands
# from discord import app_commands
# from discord.ui import View, Select
# from db_manager import get_server_config, set_server_config
# import systemlogs

# logger = systemlogs.logging.getLogger("bot")

# class ConfigDropdown(discord.ui.Select):
#     def __init__(self, bot, guild_id):
#         self.bot = bot
#         self.guild_id = guild_id
#         options = [
#             discord.SelectOption(label="Moderation", description="Enable/disable the Moderation module"),
#             discord.SelectOption(label="Levels", description="Enable/disable the Levels module"),
#             discord.SelectOption(label="Utility", description="Enable/disable the Server Utitlity module")
#         ]
#         super().__init__(placeholder="Select a module to toggle", options=options)

#     async def callback(self, interaction: discord.Interaction):
#         selected_cog = self.values[0].lower()
#         config = get_server_config(self.guild_id)
#         if selected_cog in config:
#             config.remove(selected_cog)
#             await interaction.client.unload_extension(f"cogs.{selected_cog}")
#             await interaction.response.send_message(f"❌ Disabled '{selected_cog}' module!")
#         else: 
#             config.append(selected_cog)
#             await interaction.client.load_extension(f"cogs.{selected_cog}")
#             await interaction.response.send_message(f"✅ Enabled '{selected_cog} module!")
#         set_server_config(self.guild_id, config)

# class ConfigView(View):
#     def __init__(self, bot, guild_id):
#         super().__init__()
#         self.add_item(ConfigDropdown(bot, guild_id))

# class ServerConfig(commands.Cog):
#     def __init__(self, bot):
#         self.bot = bot

# # Load ServerConfig Cog
#     @commands.Cog.listener()
#     async def on_ready(self):
#         try:
#             logger.info("ServerConfig module successfully loaded!")
#         except Exception as e:
#             logger.error("ServerConfig module failed to load:", {e})

# # Config Command
#     @app_commands.command(name="config", description="Edit server configuration")
#     @app_commands.checks.has_permissions(administrator=True)
#     async def serverconfig(self, interaction: discord.Interaction):
#         view = ConfigView(self.bot, interaction.guild.id)
#         await interaction.response.send_message("Select a module to enable/disable:", view=view, ephemeral=True)

# async def setup(bot):
#     await bot.add_cog(ServerConfig(bot))