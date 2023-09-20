import os
import discord
from discord import app_commands
from discord.ext import commands
from service.read_limit_service import ReadLimitService
from service.reading_dict_service import ReadingDictService

GUILD = int(os.getenv("GUILD"))


class GuildSetting(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("loaded :" + self.__class__.__name__)
        await self.bot.tree.sync(guild=discord.Object(GUILD))
        print("sync:" + self.__class__.__name__)

    @app_commands.command(name="set_limit", description="読み上げ上限を設定")
    @app_commands.rename(upper_limit="読み上げ上限数")
    @app_commands.guilds(GUILD)
    async def set_limit(self, interaction: discord.Interaction, upper_limit: int):
        """読み上げ上限を設定"""
        ReadLimitService.set_limit(interaction.guild_id, upper_limit)
        await interaction.response.send_message(
            f"読み上げ上限を{upper_limit}に変更しました", ephemeral=False
        )

    @app_commands.command(name="add_dict", description="辞書を追加")
    @app_commands.rename(character="書き", reading="読み方")
    @app_commands.guilds(GUILD)
    async def add_dict(
        self, interaction: discord.Interaction, character: str, reading: str
    ):
        """辞書を追加"""
        ReadingDictService.add_dict(interaction.guild_id, character, reading)
        await interaction.response.send_message(
            f"辞書に{character}({reading})を追加しました", ephemeral=False
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(GuildSetting(bot))
