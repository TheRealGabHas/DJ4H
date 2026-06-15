import discord
from discord import SlashCommandGroup
from discord.ext import commands

from config import MAGIC_COLOR
from utils.database.dao.rngdle import RNGdleDao


class RNGdle(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    rng_group = SlashCommandGroup(name="rngdle", description="RNGDLE commands")

    @rng_group.command(description="Register an RNGDLE user")
    async def register(
        self,
        ctx: discord.ApplicationContext,
        discord_user: discord.Member,
        username: str,
    ) -> None:
        """Register an RNGDLE user."""
        await ctx.defer()  # Defer the response to allow for longer processing time
        await RNGdleDao.register_user(discord_user.id, ctx.guild.id, username)
        message = discord.Embed(
            title="RNGDLE user",
            color=discord.Colour(MAGIC_COLOR),
            description=f"RNGDLE user `{username}` link to <@{discord_user.id}> successfully!",
        )
        await ctx.respond(embed=message)

    @rng_group.command(description="Show registered RNGDLE users")
    async def show(self, ctx: discord.ApplicationContext) -> None:
        """Show registered RNGDLE users."""
        await ctx.defer()
        if ctx.guild is None:
            await ctx.respond("This command can only be used in a server!")
            return

        await RNGdleDao.get_registered_users(ctx.guild.id)
        users = await RNGdleDao.get_registered_users(ctx.guild.id)
        if not users:
            await ctx.respond("No registered RNGDLE users found.")
            return

        all_users = "\n".join(
            f"<@{user.user_id}> -> {user.rng_username}" for user in users
        )
        message = discord.Embed(
            title="RNGDLE users",
            color=discord.Colour(MAGIC_COLOR),
            description=all_users,
        )
        await ctx.respond(embed=message)


def setup(bot):
    bot.add_cog(RNGdle(bot))
