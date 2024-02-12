import discord
from discord import app_commands
from discord.ext import commands
from service.voice_setting_service import VoiceSettingService
from service.guild_voice_setting_service import GuildVoiceSettingService


class UserSetting(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("loaded :" + self.__class__.__name__)
        await self.bot.tree.sync(guild=None)
        print("sync:" + self.__class__.__name__)

    @app_commands.command(name="set_softalk", description="SofTalkの声を設定する")
    @app_commands.describe(
        voice_name_key="ボイスキー",
        speed="デフォルトは120、下限0,上限300",
        pitch="デフォルトは100、下限0,上限300",
    )
    @app_commands.rename(voice_name_key="ボイスキー", speed="スピード", pitch="ピッチ")
    async def set_softalk(
        self,
        interaction: discord.Interaction,
        voice_name_key: str,
        speed: app_commands.Range[int, 0, 300] = 120,
        pitch: app_commands.Range[int, 0, 300] = 100,
    ):
        """SofTalkの声を設定する

        Parameters
        ----------
        interaction : discord.Interaction
            discord.Interaction
        voice_name_key : str
            ボイスキー
        speed : app_commands.Range[int, 0, 300], optional
            スピード, by default 120
        pitch : app_commands.Range[int, 0, 300], optional
            ピッチ, by default 100
        """

        await VoiceSettingService.set_softalk(
            interaction, interaction.guild_id, interaction.user.id, voice_name_key, speed, pitch
        )

    @app_commands.command(name="set_voiceroid", description="VOICEROIDの声を設定する")
    @app_commands.describe(
        voice_name_key="ボイスキー",
        speed="デフォルトは1.00、下限0.50,上限4.00",
        pitch="デフォルトは1.00、下限0.50,上限2.00",
    )
    @app_commands.rename(voice_name_key="ボイスキー", speed="スピード", pitch="ピッチ")
    async def set_voiceroid(
        self,
        interaction: discord.Interaction,
        voice_name_key: str,
        speed: app_commands.Range[float, 0.50, 4.00] = 1,
        pitch: app_commands.Range[float, 0.50, 2.00] = 1,
    ):
        """VOICEROIDの声を設定する

        Parameters
        ----------
        interaction : discord.Interaction
            discord.Interaction
        voice_name_key : str
            ボイスキー
        speed : app_commands.Range[float, 0.50, 4.00], optional
            スピード, by default 1
        pitch : app_commands.Range[float, 0.50, 2.00], optional
            ピッチ, by default 1
        """

        await VoiceSettingService.set_voiceroid(
            interaction, interaction.guild_id, interaction.user.id, voice_name_key, speed, pitch
        )

    @app_commands.command(name="set_voicevox", description="VOICEVOXの声を設定する")
    @app_commands.describe(
        voice_name_key="ボイスキー",
        speed="デフォルトは1.00、下限0.50,上限2.00",
        pitch="デフォルトは0.00、下限-0.15,上限0.15",
    )
    @app_commands.rename(voice_name_key="ボイスキー", speed="スピード", pitch="ピッチ")
    async def set_voicevox(
        self,
        interaction: discord.Interaction,
        voice_name_key: str,
        speed: app_commands.Range[float, 0.50, 2.00] = 1,
        pitch: app_commands.Range[float, -0.15, 0.15] = 0,
    ):
        """VOICEVOXの声を設定する

        Parameters
        ----------
        interaction : discord.Interaction
            discord.Interaction
        voice_name_key : str
            ボイスキー
        speed : app_commands.Range[float, 0.50, 2.00], optional
            スピード, by default 1
        pitch : app_commands.Range[float,, optional
            ピッチ, by default 0
        """

        await VoiceSettingService.set_voicevox(
            interaction, interaction.guild_id, interaction.user.id, voice_name_key, speed, pitch
        )

    @app_commands.command(name="set_other_user_softalk", description="他のユーザーのSofTalkの声を設定する(管理者権限が必要です)")
    @app_commands.describe(
        member="対象のユーザー",
        voice_name_key="ボイスキー",
        speed="デフォルトは120、下限0,上限300",
        pitch="デフォルトは100、下限0,上限300",
    )
    @app_commands.rename(member="ユーザー", voice_name_key="ボイスキー", speed="スピード", pitch="ピッチ")
    @app_commands.checks.has_permissions(administrator=True)
    async def set_other_user_softalk(
        self,
        interaction: discord.Interaction,
        member :discord.Member,
        voice_name_key: str,
        speed: app_commands.Range[int, 0, 300] = 120,
        pitch: app_commands.Range[int, 0, 300] = 100,
    ):
        """SofTalkの声を設定する

        Parameters
        ----------
        interaction : discord.Interaction
            discord.Interaction
        voice_name_key : str
            ボイスキー
        speed : app_commands.Range[int, 0, 300], optional
            スピード, by default 120
        pitch : app_commands.Range[int, 0, 300], optional
            ピッチ, by default 100
        """

        await GuildVoiceSettingService.set_softalk(
            interaction, interaction.guild_id, member.id, voice_name_key, speed, pitch
        )

    @app_commands.command(name="set_other_user_voiceroid", description="他のユーザーのVOICEROIDの声を設定する(管理者権限が必要です)")
    @app_commands.describe(
        member="対象のユーザー",
        voice_name_key="ボイスキー",
        speed="デフォルトは1.00、下限0.50,上限4.00",
        pitch="デフォルトは1.00、下限0.50,上限2.00",
    )
    @app_commands.rename(member="ユーザー", voice_name_key="ボイスキー", speed="スピード", pitch="ピッチ")
    @app_commands.checks.has_permissions(administrator=True)
    async def set_other_user_voiceroid(
        self,
        interaction: discord.Interaction,
        member :discord.Member,
        voice_name_key: str,
        speed: app_commands.Range[float, 0.50, 4.00] = 1,
        pitch: app_commands.Range[float, 0.50, 2.00] = 1,
    ):
        """VOICEROIDの声を設定する

        Parameters
        ----------
        interaction : discord.Interaction
            discord.Interaction
        voice_name_key : str
            ボイスキー
        speed : app_commands.Range[float, 0.50, 4.00], optional
            スピード, by default 1
        pitch : app_commands.Range[float, 0.50, 2.00], optional
            ピッチ, by default 1
        """

        await GuildVoiceSettingService.set_voiceroid(
            interaction, interaction.guild_id, member.id, voice_name_key, speed, pitch
        )

    @app_commands.command(name="set_other_user_voicevox", description="他のユーザーのVOICEVOXの声を設定する(管理者権限が必要です)")
    @app_commands.describe(
        member="対象のユーザー",
        voice_name_key="ボイスキー",
        speed="デフォルトは1.00、下限0.50,上限2.00",
        pitch="デフォルトは0.00、下限-0.15,上限0.15",
    )
    @app_commands.rename(member="ユーザー", voice_name_key="ボイスキー", speed="スピード", pitch="ピッチ")
    @app_commands.checks.has_permissions(administrator=True)
    async def set_other_user_voicevox(
        self,
        interaction: discord.Interaction,
        member :discord.Member,
        voice_name_key: str,
        speed: app_commands.Range[float, 0.50, 2.00] = 1,
        pitch: app_commands.Range[float, -0.15, 0.15] = 0,
    ):
        """VOICEVOXの声を設定する

        Parameters
        ----------
        interaction : discord.Interaction
            discord.Interaction
        voice_name_key : str
            ボイスキー
        speed : app_commands.Range[float, 0.50, 2.00], optional
            スピード, by default 1
        pitch : app_commands.Range[float,, optional
            ピッチ, by default 0
        """

        await GuildVoiceSettingService.set_voicevox(
            interaction, interaction.guild_id, member.id, voice_name_key, speed, pitch
        )

    @set_other_user_voiceroid.error
    @set_other_user_voiceroid.error
    @set_other_user_voicevox.error
    async def test_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        await interaction.response.defer()
        await interaction.followup.send("権限がありません")


async def setup(bot: commands.Bot):
    await bot.add_cog(UserSetting(bot))
