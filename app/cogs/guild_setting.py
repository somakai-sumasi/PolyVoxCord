import discord
from discord import app_commands
from discord.ext import commands
from service.read_limit_service import ReadLimitService
from service.reading_dict_service import ReadingDictService
from cogs.base_cog import BaseUserCog


class GuildSetting(BaseUserCog):
    def __init__(self, bot: commands.Bot):
        super().__init__(bot)

    @app_commands.guild_only
    @app_commands.command(name="set_limit", description="読み上げ上限数を設定")
    @app_commands.rename(upper_limit="読み上げ上限数")
    async def set_limit(self, interaction: discord.Interaction, upper_limit: int):
        """読み上げ上限数を設定

        Parameters
        ----------
        interaction : discord.Interaction
            discord.Interaction
        upper_limit : int
            読み上げ上限数
        """
        await ReadLimitService.set_limit(interaction, interaction.guild_id, upper_limit)

    @app_commands.guild_only
    @app_commands.command(name="add_dict", description="辞書を追加")
    @app_commands.rename(character="書き", reading="読み方")
    async def add_dict(
        self, interaction: discord.Interaction, character: str, reading: str
    ):
        """辞書を追加

        Parameters
        ----------
        interaction : discord.Interaction
            discord.Interaction
        character : str
            読み
        reading : str
            書き
        """

        await ReadingDictService.add_dict(
            interaction, interaction.guild_id, character, reading
        )

    @app_commands.guild_only
    @app_commands.command(name="del_dict", description="辞書を削除")
    @app_commands.rename(character="書き")
    async def del_dict(self, interaction: discord.Interaction, character: str):
        """辞書を削除

        Parameters
        ----------
        interaction : discord.Interaction
            discord.Interaction
        character : str
            読み
        reading : str
            書き
        """

        await ReadingDictService.del_dict(interaction, interaction.guild_id, character)


async def setup(bot: commands.Bot):
    await bot.add_cog(GuildSetting(bot))
