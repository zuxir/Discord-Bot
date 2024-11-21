import discord
from discord.ext import commands
from discord import app_commands
import sqlite3
import math
import random

class LevelSys(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

# Load Level Cog
    @commands.Cog.listener()
    async def on_ready(self):
        print("Leveling system successfully loaded!")

    @commands.Cog.listener() # Listens for new messages to update member xp
    async def on_message(self, message: discord.message):
        if message.author.bot:
            return
        # Opens connection if member is NOT a bot
        connection = sqlite3.connect("./cogs/levels.db")
        cursor = connection.cursor()
        guild_id = message.guild.id
        user_id = message.author.id

        cursor.execute("SELECT * FROM Users WHERE guild_id = ? AND user_id = ?", (guild_id, user_id))

        result = cursor.fetchone() # Find first result that comes out as query

        if result is None: # Creates new data for members not in db
            cur_level = 0
            xp = 0
            level_up_xp = 100
            cursor.execute("INSERT INTO Users (guild_id, user_id, level, xp, level_up_xp) Values(?,?,?,?,?)", (guild_id, user_id, cur_level, xp, level_up_xp))

        else: # If member in db then defines data
            cur_level = result[2]
            xp = result[3]
            level_up_xp = result[4]

            xp += random.randint(1, 25) # Adds random amount of xp per message

        if xp >= level_up_xp: # Changes the ceiling cap of xp needed to level up to next level
            cur_level += 1
            new_level_up_xp = math.ceil(50 * cur_level ** 2 + 100 * cur_level + 50)

            await message.channel.send(f"{message.author.mention} has leveled up to level {cur_level}! GGs!")

            cursor.execute("UPDATE Users SET level = ?, xp = ?, level_up_xp = ? WHERE guild_id = ? AND user_id = ?", (cur_level, xp, new_level_up_xp, guild_id, user_id))


        cursor.execute("UPDATE Users SET xp = ? WHERE guild_id = ? AND user_id = ?", (xp, guild_id, user_id))

        connection.commit()
        connection.close()

# Command to retrieve level data for a member and post a message in chat
    @app_commands.command(name="level", description="Check a specified member's server level.")
    async def level(self, interaction: discord.Interaction, member: discord.Member=None):

        if member is None:
            member = interaction.user

        member_id = member.id
        guild_id = interaction.guild.id
        
        connection = sqlite3.connect("./cogs/levels.db")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Users WHERE guild_id = ? AND user_id = ?", (guild_id, member_id))
        result = cursor.fetchone()

        if result is None:
            await interaction.response.send_message(f"{member.name} is level 0.")
        else:
            level = result[2]
            xp = result[3]
            level_up_xp = result[4]

            await interaction.response.send_message(f"{member.name} is level {level}, with {xp} xp.\n{level_up_xp} xp is needed to level up.")

        connection.close()


async def setup(bot):
    await bot.add_cog(LevelSys(bot))