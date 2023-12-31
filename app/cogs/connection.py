import discord
from discord import app_commands
from discord.ext import commands
from service.presence_service import PresenceService
from service.read_service import ReadService


class connection(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("loaded :" + self.__class__.__name__)
        await self.bot.tree.sync(guild=None)
        print("sync:" + self.__class__.__name__)

    @app_commands.command(name="read_start", description="読み上げ開始")
    async def read_start(self, interaction: discord.Interaction):
        """読み上げを開始する

        Parameters
        ----------
        interaction : discord.Interaction
            discord.Interaction
        """
        await interaction.response.defer()

        user = interaction.user
        if user.voice is None:
            await interaction.followup.send("接続してません")
            return

        if user.guild.voice_client is None:
            await user.voice.channel.connect()

        await interaction.followup.send("接続しました")

        ReadService.add_text_channel(user.guild.id, interaction.channel.id)
        await PresenceService.set_presence(self.bot)

    @app_commands.command(name="read_end", description="読み上げ終了")
    async def read_end(self, interaction: discord.Interaction):
        """読み上げを終了する

        Parameters
        ----------
        interaction : discord.Interaction
            discord.Interaction
        """
        await interaction.response.defer()

        user = interaction.user
        if user.guild.voice_client is None:
            await interaction.followup.send("接続してません")
            return

        await user.guild.voice_client.disconnect()
        await interaction.followup.send("切断しました")

        ReadService.remove_guild(user.guild.id)
        await PresenceService.set_presence(self.bot)


async def setup(bot: commands.Bot):
    await bot.add_cog(connection(bot))
