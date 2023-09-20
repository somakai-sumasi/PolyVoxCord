import os
import discord
from discord import app_commands
from discord.ext import commands
from service.voice_setting_service import VoiceSettingService


GUILD = int(os.getenv("GUILD"))


class UserSetting(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("loaded :" + self.__class__.__name__)
        await self.bot.tree.sync(guild=discord.Object(GUILD))
        print("sync:" + self.__class__.__name__)

    @app_commands.command(name="set_softalk", description="SofTalkの声を設定する")
    @app_commands.guilds(GUILD)
    async def set_softalk(self, interaction: discord.Interaction):
        """SofTalkの声を設定する"""
        user_id = interaction.user.id

    @app_commands.command(name="set_voiceroid", description="VOICEROIDの声を設定する")
    @app_commands.guilds(GUILD)
    async def set_voiceroid(self, interaction: discord.Interaction):
        """VOICEROIDの声を設定する"""
        user_id = interaction.user.id

    @app_commands.command(name="set_voicevox", description="VOICEVOXの声を設定する")
    @app_commands.describe(
        voice_name_key="ボイスキー",
        speed="デフォルトは1、下限0.50,上限2.00",
        pitch="デフォルトは0、下限-0.15,上限0.15",
    )
    @app_commands.rename(voice_name_key="ボイスキー", speed="スピード", pitch="ピッチ")
    @app_commands.guilds(GUILD)
    async def set_voicevox(
        self,
        interaction: discord.Interaction,
        voice_name_key: str,
        speed: app_commands.Range[float, 0.50, 2.00] = 1,
        pitch: app_commands.Range[float, -0.15, 0.15] = 0,
    ):
        """VOICEVOXの声を設定する"""

        await VoiceSettingService.set_voicevox(
            interaction, interaction.user.id, voice_name_key, speed, pitch
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(UserSetting(bot))