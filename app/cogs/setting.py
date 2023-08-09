import os
import discord
from discord import app_commands
from discord.ext import commands
from service import read_limit

GUILD = int(os.getenv("GUILD"))


class HogeList(discord.ui.View):
    def __init__(self, items, callback_func):
        super().__init__()
        self.add_item(HugaList(items, callback_func))


class HugaList(discord.ui.Select):
    def __init__(self, items, callback_func):
        self.callback_func = callback_func
        options = []
        for item in items:
            options.append(discord.SelectOption(label=item, description=""))

        super().__init__(placeholder="", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        await self.callback_func(self, interaction)


class setting(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("loaded :" + self.__class__.__name__)
        await self.bot.tree.sync(guild=discord.Object(GUILD))
        print("sync:" + self.__class__.__name__)

    @app_commands.command(name="change_voice", description="声を変える")
    @app_commands.guilds(GUILD)
    async def change_voice(self, interaction: discord.Interaction):
        """声を変える"""
        user_id = interaction.user.id
        items = ["a", "b", "c"]

        async def callback_func(self, interaction: discord.Interaction):
            await interaction.response.send_message(
                f"{interaction.user.name}は{self.values[0]}を選択しました", ephemeral=True
            )

        await interaction.response.send_message(
            "Press", view=HogeList(items, callback_func), ephemeral=True
        )

    @app_commands.command(name="tune_voice", description="調声を行う")
    @app_commands.guilds(GUILD)
    async def tune_voice(self, interaction: discord.Interaction):
        """調声を行う"""
        user_id = interaction.user.id

    @app_commands.command(name="set_limit", description="読み上げ上限を設定")
    @app_commands.guilds(GUILD)
    async def set_limit(self, interaction: discord.Interaction, limit: int):
        """読み上げ上限を設定"""
        read_limit.set_limt(interaction.guild_id, limit)
        await interaction.response.send_message("上限を変更しました", ephemeral=True)

    @app_commands.command(name="add_dict", description="辞書を追加")
    @app_commands.guilds(GUILD)
    async def add_dict(self, interaction: discord.Interaction):
        """辞書を追加"""


async def setup(bot: commands.Bot):
    await bot.add_cog(setting(bot))
