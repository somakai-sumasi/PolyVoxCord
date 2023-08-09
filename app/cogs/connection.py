import os
import discord
from discord import app_commands
from discord.ext import commands

GUILD = int(os.getenv("GUILD"))


class connection(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("loaded :" + self.__class__.__name__)
        await self.bot.tree.sync(guild=discord.Object(GUILD))
        print("sync:" + self.__class__.__name__)

    @app_commands.command(name="read_start", description="読み上げ開始")
    @app_commands.guilds(GUILD)
    async def read_start(self, interaction: discord.Interaction):
        """読み上げを開始する"""
        user = interaction.user
        if user.voice is None:
            await interaction.response.send_message("接続してません", ephemeral=True)
            return

        await user.voice.channel.connect()
        await interaction.response.send_message("接続しました", ephemeral=True)

    @app_commands.command(name="read_end", description="読み上げ開始")
    @app_commands.guilds(GUILD)
    async def read_end(self, interaction: discord.Interaction):
        """読み上げを終了する"""

        user = interaction.user
        if user.guild.voice_client is None:
            await interaction.response.send_message("接続してません", ephemeral=True)
            return

        await user.guild.voice_client.disconnect()
        await interaction.response.send_message("切断しました", ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(connection(bot))
