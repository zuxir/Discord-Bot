from discord.ext import commands
import systemlogs
import asyncio

logger = systemlogs.logging.getLogger("bot")

# Bot Owner Check
def is_developer():
    def predicate(ctx: commands.Context) -> bool:
        if ctx.author.id == 384813212396421122:
            return True
        raise commands.CheckFailure("You do not have permission to run this command!")
    return commands.check(predicate)

class DeveloperUtility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Logging functionality for "DeveloperUtility" cog
    @commands.Cog.listener()
    async def on_ready(self):
        try:
            logger.info("Developer Utility module successfully loaded!")
        except Exception as e:
            logger.error("Developer Utility module failed to load: ", e)

    # Reload Command
    @commands.command()
    @is_developer()
    async def reload(self, ctx, cog: str):
        try:
            await ctx.message.delete()
            await self.bot.reload_extension(f"cogs.{cog.lower()}")
            response = await ctx.send(f"Successfully reloaded {cog} cog!")
            await asyncio.sleep(2)
            await response.delete()
        except Exception as e:
            response = await ctx.send(f"<:Cross:1310203839495802890> **FAILURE**\nFailed to reload {cog} cog!\nError: {e}")
    # Permission Error
    @reload.error
    async def reload_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            response = await ctx.send("You do not have permissions to run this command!")
            await asyncio.sleep(2)
            await response.delete()
        else:
            raise error

    # Load Command
    @commands.command()
    @is_developer()
    async def load(self, ctx, cog: str):
        try:
            await ctx.message.delete()
            await self.bot.load_extension(f"cogs.{cog.lower()}")
            response = await ctx.send(f"Successfully loaded {cog} cog!")
            await asyncio.sleep(2)
            await response.delete()
        except Exception as e:
            await ctx.send(f"<:Cross:1310203839495802890> **FAILURE**\nFailed to load {cog} cog!\nError: {e}")
    # Permission Error
    @load.error
    async def load_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            response = await ctx.send("You do not have permissions to run this command!")
            await asyncio.sleep(2)
            await response.delete()
        else:
            raise error
        
    # Unload Command
    @commands.command()
    @is_developer()
    async def unload(self, ctx, cog: str):
        try:
            await ctx.message.delete()
            await self.bot.unload_extension(f"cogs.{cog.lower()}")
            response = await ctx.send(f"Successfully unloaded {cog} cog!")
            await asyncio.sleep(2)
            await response.delete()
        except Exception as e:
            await ctx.send(f"<:Cross:1310203839495802890> **FAILURE**\nFailed to unload {cog} cog!\nError: {e}")
    # Permission Error
    @unload.error
    async def unload_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            response = await ctx.send("You do not have permissions to run this command!")
            await asyncio.sleep(2)
            await response.delete()
        else:
            raise error

async def setup(bot):
    await bot.add_cog(DeveloperUtility(bot))