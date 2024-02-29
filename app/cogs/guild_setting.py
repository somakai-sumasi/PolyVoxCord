import discord
from discord import app_commands
from discord.ext import commands
from service.read_limit_service import ReadLimitService
from service.reading_dict_service import ReadingDictService


class GuildSetting(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("loaded :" + self.__class__.__name__)
        await self.bot.tree.sync(guild=None)
        print("sync:" + self.__class__.__name__)

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
        await interaction.response.defer()

        ReadLimitService.set_limit(interaction.guild_id, upper_limit)
        await interaction.followup.send(
            f"読み上げ上限を{upper_limit}文字に変更しました", ephemeral=False
        )

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
        await interaction.response.defer()
        ReadingDictService.add_dict(interaction.guild_id, character, reading)
        await interaction.followup.send(
            f"辞書に{character}({reading})を追加しました", ephemeral=False
        )


    @app_commands.command(name="del_dict", description="辞書を削除")
    @app_commands.rename(character="書き")
    async def del_dict(
        self, interaction: discord.Interaction, character: str
    ):
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
        await interaction.response.defer()
        ReadingDictService.del_dict(interaction.guild_id, character)
        await interaction.followup.send(
            f"辞書に{character}を削除しました", ephemeral=False
        )

async def setup(bot: commands.Bot):
    await bot.add_cog(GuildSetting(bot))
