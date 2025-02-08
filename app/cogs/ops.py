import discord
from cogs.base_cog import BaseOpsCog
from common.user_message import MessageType
from config.discord import MANAGEMENT_GUILD_ID
from discord import app_commands
from discord.ext import commands
from base.bot import BaseBot


class Ops(BaseOpsCog):
    def __init__(self, bot: commands.Bot):
        super().__init__(bot)

    @app_commands.command(description="ホットリロード")
    async def reload_extensions(self, interaction: discord.Interaction):
        await interaction.response.defer()

        bot: BaseBot = self.bot
        cogs = bot.get_cogs()

        for cog in cogs:
            await bot.reload_extension(cog)

        await interaction.followup.send("リロードしました")

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

    @app_commands.command(name="guild_details", description="参加しているサーバーの詳細を見る")
    async def guild_details(
        self,
        interaction: discord.Interaction,
        guild_id: str,
    ):
        """参加しているサーバーから抜ける

        Parameters
        ----------
        interaction : discord.Interaction
            discord.Interaction
        """
        await interaction.response.defer()

        try:
            guild = next(obj for obj in self.bot.guilds if obj.id == int(guild_id))

            embed = discord.Embed(title=guild.name, color=MessageType.INFO)
            owner = guild.owner

            embed.add_field(name="管理者", value=owner.global_name)
            embed.set_image(url=owner.display_avatar.url)
            embed.add_field(name="参加人数", value=f"{len(guild.members)}人")
            embed.add_field(name="参加者", value=f"{len(guild.members)}人")

            await interaction.followup.send(
                embed=embed,
                ephemeral=False,
            )

        except StopIteration:
            await interaction.followup.send("そのようなサーバーには入っていません")

    @app_commands.command(name="exit_guild", description="参加しているサーバーから抜ける")
    async def exit_guild(
        self,
        interaction: discord.Interaction,
        guild_id: str,
    ):
        """参加しているサーバーから抜ける

        Parameters
        ----------
        interaction : discord.Interaction
            discord.Interaction
        """
        await interaction.response.defer()

        try:
            guild = next(obj for obj in self.bot.guilds if obj.id == int(guild_id))
            await guild.leave()
            await interaction.followup.send(f"{guild.name}から抜けました")
        except StopIteration:
            await interaction.followup.send("そのようなサーバーには入っていません")


async def setup(bot: commands.Bot):
    await bot.add_cog(Ops(bot), guild=discord.Object(id=MANAGEMENT_GUILD_ID))
