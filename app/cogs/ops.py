import discord
from discord import app_commands
from discord.ext import commands
from cogs.base_cog import BaseOpsCog
from common.user_message import MessageType


class Ops(BaseOpsCog):
    def __init__(self, bot: commands.Bot):
        super().__init__(bot)

    @app_commands.command(name="guilds_list", description="参加しているサーバーの一覧を返す")
    async def guilds_list(self, interaction: discord.Interaction):
        """参加しているサーバーの一覧を返す

        Parameters
        ----------
        interaction : discord.Interaction
            discord.Interaction
        """
        await interaction.response.defer()

        text = ""
        for guild in self.bot.guilds:
            text += f"`{guild.id}`   {guild.name}\n"

        await interaction.followup.send(
            embed=discord.Embed(
                title="参加サーバー", description=text, color=MessageType.INFO
            ),
            ephemeral=False,
        )

    @app_commands.command(name="exit_guild", description="参加しているサーバーから抜ける")
    async def exit_guild(
        self,
        interaction: discord.Interaction,
        guild_id: int,
    ):
        """参加しているサーバーから抜ける

        Parameters
        ----------
        interaction : discord.Interaction
            discord.Interaction
        """
        await interaction.response.defer()

        try:
            guild = next(obj for obj in self.bot.guilds if obj.id == guild_id)
            await guild.leave()
            await interaction.followup.send(f"{guild.name}から抜けました")
        except StopIteration:
            await interaction.followup.send("そのようなサーバーには入っていません")


async def setup(bot: commands.Bot):
    await bot.add_cog(Ops(bot))
