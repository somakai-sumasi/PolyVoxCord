import os
import discord
from discord import app_commands
from discord.ext import commands
from service import read_limit
from common import ui

GUILD = int(os.getenv("GUILD"))


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
        items = [
            {"label": "aaa", "value": "1", "description": ""},
            {"label": "bbb", "value": "2", "description": ""},
        ]

        async def callback_func(self, interaction: discord.Interaction):
            print(self.options)

            await interaction.response.send_message(
                f"{interaction.user.name}は{self.values[0]}を選択しました", ephemeral=True
            )

        await interaction.response.send_message(
            "Press", view=ui.SelectView(items, callback_func), ephemeral=True
        )

    @app_commands.command(name="set_softalk", description="SofTalkの声を設定する")
    @app_commands.guilds(GUILD)
    async def set_sof_talk(self, interaction: discord.Interaction):
        """SofTalkの声を設定する"""
        user_id = interaction.user.id

    @app_commands.command(name="set_voiceroid", description="VOICEROIDの声を設定する")
    @app_commands.guilds(GUILD)
    async def set_voiceroid(self, interaction: discord.Interaction):
        """VOICEROIDの声を設定する"""
        user_id = interaction.user.id

    @app_commands.command(name="set_voicevox", description="VOICEVOXの声を設定する")
    @app_commands.guilds(GUILD)
    async def set_voicevox(self, interaction: discord.Interaction):
        """VOICEVOXの声を設定する"""
        user_id = interaction.user.id


    @app_commands.command(name="tune_voice", description="調声を行う")
    @app_commands.guilds(GUILD)
    async def tune_voice(self, interaction: discord.Interaction):
        """調声を行う"""
        user_id = interaction.user.id

    @app_commands.command(name="set_limit", description="読み上げ上限を設定")
    @app_commands.guilds(GUILD)
    async def set_limit(self, interaction: discord.Interaction, limit: int):
        """読み上げ上限を設定"""
        read_limit.set_limit(interaction.guild_id, limit)
        await interaction.response.send_message("上限を変更しました", ephemeral=True)

    @app_commands.command(name="add_dict", description="辞書を追加")
    @app_commands.guilds(GUILD)
    async def add_dict(self, interaction: discord.Interaction):
        """辞書を追加"""


async def setup(bot: commands.Bot):
    await bot.add_cog(setting(bot))
