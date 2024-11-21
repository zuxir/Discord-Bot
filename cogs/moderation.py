import discord
from discord.ext import commands
from discord import app_commands
import asyncio

class Mod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Moderation commands successfully loaded!")

# Clear / Purge Messages
    @app_commands.command(name="clear", description="Deletes a specified amount of messages from the channel.")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def delete_messages(self, interaction: discord.Interaction, amount: int):
        await interaction.response.defer()
        if amount < 1:
            await interaction.followup.send(f"{interaction.user.mention}, please specify a value greater than one.", ephemeral=True)
            return
        deleted_messages = await interaction.channel.purge(limit=amount, before=interaction.created_at)
        await interaction.followup.send(f"Successfully deleted {len(deleted_messages)} messages!", ephemeral=True)

# Kick Member
    @app_commands.command(name="kick", description="Kicks a specified member.")
    @app_commands.checks.has_permissions(kick_members=True)
    async def kick(self, interaction: discord.Interaction, member: discord.Member):
        await interaction.guild.kick(member)
        await interaction.response.send_message(f"Succesfully kicked {member.mention}!", ephemeral=True)

# Ban Member
    @app_commands.command(name="ban", description="Bans a specified member.")
    @app_commands.checks.has_permissions(ban_members=True)
    async def ban(self, interaction: discord.Interaction, member: discord.Member):
        await interaction.guild.ban(member)
        await interaction.response.send_message(f"Succesfully banned {member.mention}!", ephemeral=True)

# Unban Member
    @app_commands.command(name="unban", description="Unban a specified user by User ID.")
    @app_commands.checks.has_permissions(ban_members=True)
    async def unban(self, interaction: discord.Interaction, user_id: str):
        user = await self.bot.fetch_user(user_id)
        await interaction.guild.unban(user)
        await interaction.response.send_message(f"Successfully unbanned {user.name}!", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Mod(bot))