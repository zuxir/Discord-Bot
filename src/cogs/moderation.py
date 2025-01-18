import discord
from discord.ext import commands
from discord import app_commands
from discord.app_commands import CheckFailure
import asyncio
import systemlogs
import datetime
from checks.permissioncheck import has_required_role

logger = systemlogs.logging.getLogger("bot")

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        try:
            logger.info("Moderation module successfully loaded!")
        except Exception as e:
            logger.error("Moderation module failed to load:", {e})

# Clear / Purge Messages
    @app_commands.command(name="clear", description="Deletes a specified amount of messages from the channel.")
    # @app_commands.checks.has_permissions(manage_messages=True)
    @discord.app_commands.check(has_required_role())
    async def delete_messages(self, interaction: discord.Interaction, amount: int):
        await interaction.response.defer()
        if amount < 1:
            await interaction.followup.send(f"{interaction.user.mention}, please specify a value greater than one.", ephemeral=True)
            return
        deleted_messages = await interaction.channel.purge(limit=amount, before=interaction.created_at)
        await interaction.followup.send(f"Successfully deleted {len(deleted_messages)} messages!", ephemeral=True)

# Kick Member
    @app_commands.command(name="kick", description="Kick a member.")
    @app_commands.checks.has_permissions(kick_members=True)
    async def kick(self, interaction: discord.Interaction, member: discord.Member):
        await interaction.guild.kick(member)
        await interaction.response.send_message(f"Succesfully kicked {member.mention}!", ephemeral=True)

# Ban Member
    @app_commands.command(name="ban", description="Ban a member.")
    @app_commands.checks.has_permissions(ban_members=True)
    async def ban(self, interaction: discord.Interaction, member: discord.Member):
        await interaction.guild.ban(member)
        await interaction.response.send_message(f"Succesfully banned {member.mention}!", ephemeral=True)

# Unban Member
    @app_commands.command(name="unban", description="Unban a user by User ID.")
    @app_commands.checks.has_permissions(ban_members=True)
    async def unban(self, interaction: discord.Interaction, user_id: str):
        user = await self.bot.fetch_user(user_id)
        await interaction.guild.unban(user)
        await interaction.response.send_message(f"Successfully unbanned {user.name}!", ephemeral=True)

# Timeout Member
    @app_commands.command(name="timeout", description="Times out a user for a set duration.")
    @app_commands.checks.has_permissions(moderate_members=True)
    async def timeout(self, interaction: discord.Interaction, member: discord.Member, duration: str, reason: str = None):
        times_units = {
            "s": 1,
            "m": 60,
            "h": 3600,
            "d": 86400
        }
        try:
            amount, unit = int(duration[:-1]), duration[-1].lower()
            seconds = amount * times_units[unit]
        except (ValueError, KeyError):
            return await interaction.response.send_message("Invalid duration format. Use 's' for seconds, 'm' for minutes, 'h' for hours, or 'd' for days.", ephemeral=True)
        
        if seconds > 2419200: # 28 days maximum
            return await interaction.response.send_message("Timeout duration cannot exceed 28 days.", ephemeral=True)
        
        until = datetime.datetime.utcnow() + datetime.timedelta(seconds=seconds)

        try:
            await member.timeout(until, reason=reason)
            await interaction.response.send_message(f"Successfully timed out {member.mention} for {duration}! Reason: {reason if reason else 'No reason provided.'}", ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message("I do not have permission to timeout that user.")

    @delete_messages.error
    async def on_error(self, interaction: discord.Interaction, error: Exception):
        if isinstance(error, CheckFailure):
            await interaction.response.send_message(str(error), ephemeral=True)
        else:
            raise error

async def setup(bot):
    await bot.add_cog(Moderation(bot))