import sqlite3
from discord import Interaction
from discord.app_commands import CheckFailure

def has_required_role():
    async def predicate(interaction: Interaction):
        # Database Connection
        with sqlite3.connect("./src/databases/serversettings.db") as conn:
            cursor = conn.cursor()

            # Fetech required roles from guild
            cursor.execute("SELECT manager_role, staff_role FROM GuildSettings WHERE guild_id = ?", (interaction.guild.id,))
            result = cursor.fetchone()
            if not result:
                raise CheckFailure("Required roles are not configured for this guild.")
            
            manager_role_id, staff_role_id = result

            # Check if user has required roles for the command
            if not any(role.id in [manager_role_id, staff_role_id] for role in interaction.user.roles):
                raise CheckFailure("You do not have permission to run this command!")
        # Grant access if user possesses required roles
        return True 
    return predicate