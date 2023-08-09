import discord
from discord import app_commands
from discord.ext import commands


class reset(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Successfully loaded : PostForum")
        await self.bot.tree.sync(guild=discord.Object(713594826343579681))
        print("sync")

    def check_if_it_is_me(interaction: discord.Interaction) -> bool:
        return interaction.user.id == 365830847653478400

    @app_commands.command(name="reset", description="リセット")
    @app_commands.guilds(713594826343579681)
    @app_commands.check(check_if_it_is_me)
    async def bottest(self, interaction: discord.Interaction):
        await interaction.response.send_message("リセットしました", ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(reset(bot))
