import discord
from discord import app_commands
from discord.ext import commands
from service.voice_setting_service import VoiceSettingService
from cogs.base_cog import BaseUserCog


class UserSetting(BaseUserCog):
    def __init__(self, bot: commands.Bot):
        super().__init__(bot)

    @app_commands.command(name="set_softalk", description="SofTalkの声を設定する")
    @app_commands.describe(
        key="キー",
        speed="デフォルトは120、下限0,上限300",
        pitch="デフォルトは100、下限0,上限300",
    )
    @app_commands.rename(key="キー", speed="スピード", pitch="ピッチ")
    async def set_softalk(
        self,
        interaction: discord.Interaction,
        key: int,
        speed: app_commands.Range[int, 0, 300] = 120,
        pitch: app_commands.Range[int, 0, 300] = 100,
    ):
        """SofTalkの声を設定する

        Parameters
        ----------
        interaction : discord.Interaction
            discord.Interaction
        key : int
            キー
        speed : app_commands.Range[int, 0, 300], optional
            スピード, by default 120
        pitch : app_commands.Range[int, 0, 300], optional
            ピッチ, by default 100
        """

        await VoiceSettingService.set_softalk(
            interaction,
            interaction.guild_id,
            interaction.user.id,
            key,
            speed,
            pitch,
        )

    @app_commands.command(name="set_voiceroid", description="VOICEROIDの声を設定する")
    @app_commands.describe(
        key="キー",
        speed="デフォルトは1.00、下限0.50,上限4.00",
        pitch="デフォルトは1.00、下限0.50,上限2.00",
    )
    @app_commands.rename(key="キー", speed="スピード", pitch="ピッチ")
    async def set_voiceroid(
        self,
        interaction: discord.Interaction,
        key: int,
        speed: app_commands.Range[float, 0.50, 4.00] = 1,
        pitch: app_commands.Range[float, 0.50, 2.00] = 1,
    ):
        """VOICEROIDの声を設定する

        Parameters
        ----------
        interaction : discord.Interaction
            discord.Interaction
        key : int
            キー
        speed : app_commands.Range[float, 0.50, 4.00], optional
            スピード, by default 1
        pitch : app_commands.Range[float, 0.50, 2.00], optional
            ピッチ, by default 1
        """

        await VoiceSettingService.set_voiceroid(
            interaction,
            interaction.guild_id,
            interaction.user.id,
            key,
            speed,
            pitch,
        )

    @app_commands.command(name="set_voicevox", description="VOICEVOXの声を設定する")
    @app_commands.describe(
        key="キー",
        speed="デフォルトは1.00、下限0.50,上限2.00",
        pitch="デフォルトは0.00、下限-0.15,上限0.15",
    )
    @app_commands.rename(key="キー", speed="スピード", pitch="ピッチ")
    async def set_voicevox(
        self,
        interaction: discord.Interaction,
        key: int,
        speed: app_commands.Range[float, 0.50, 2.00] = 1,
        pitch: app_commands.Range[float, -0.15, 0.15] = 0,
    ):
        """VOICEVOXの声を設定する

        Parameters
        ----------
        interaction : discord.Interaction
            discord.Interaction
        key : int
            キー
        speed : app_commands.Range[float, 0.50, 2.00], optional
            スピード, by default 1
        pitch : app_commands.Range[float,, optional
            ピッチ, by default 0
        """

        await VoiceSettingService.set_voicevox(
            interaction,
            interaction.guild_id,
            interaction.user.id,
            key,
            speed,
            pitch,
        )

    @app_commands.command(
        name="set_other_user_softalk", description="他のユーザーのSofTalkの声を設定する(管理者権限が必要です)"
    )
    @app_commands.describe(
        member="対象のユーザー",
        key="キー",
        speed="デフォルトは120、下限0,上限300",
        pitch="デフォルトは100、下限0,上限300",
    )
    @app_commands.rename(member="ユーザー", key="キー", speed="スピード", pitch="ピッチ")
    @app_commands.guild_only
    @app_commands.checks.has_permissions(administrator=True)
    async def set_other_user_softalk(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        key: int,
        speed: app_commands.Range[int, 0, 300] = 120,
        pitch: app_commands.Range[int, 0, 300] = 100,
    ):
        """SofTalkの声を設定する

        Parameters
        ----------
        interaction : discord.Interaction
            discord.Interaction
        key : int
            キー
        speed : app_commands.Range[int, 0, 300], optional
            スピード, by default 120
        pitch : app_commands.Range[int, 0, 300], optional
            ピッチ, by default 100
        """
        assert interaction.guild_id is not None
        await VoiceSettingService.set_guild_softalk(
            interaction, interaction.guild_id, member.id, key, speed, pitch
        )

    @app_commands.command(
        name="set_other_user_voiceroid",
        description="他のユーザーのVOICEROIDの声を設定する(管理者権限が必要です)",
    )
    @app_commands.describe(
        member="対象のユーザー",
        key="キー",
        speed="デフォルトは1.00、下限0.50,上限4.00",
        pitch="デフォルトは1.00、下限0.50,上限2.00",
    )
    @app_commands.rename(member="ユーザー", key="キー", speed="スピード", pitch="ピッチ")
    @app_commands.guild_only
    @app_commands.checks.has_permissions(administrator=True)
    async def set_other_user_voiceroid(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        key: int,
        speed: app_commands.Range[float, 0.50, 4.00] = 1,
        pitch: app_commands.Range[float, 0.50, 2.00] = 1,
    ):
        """VOICEROIDの声を設定する

        Parameters
        ----------
        interaction : discord.Interaction
            discord.Interaction
        key : int
            キー
        speed : app_commands.Range[float, 0.50, 4.00], optional
            スピード, by default 1
        pitch : app_commands.Range[float, 0.50, 2.00], optional
            ピッチ, by default 1
        """
        assert interaction.guild_id is not None
        await VoiceSettingService.set_guild_voiceroid(
            interaction, interaction.guild_id, member.id, key, speed, pitch
        )

    @app_commands.command(
        name="set_other_user_voicevox", description="他のユーザーのVOICEVOXの声を設定する(管理者権限が必要です)"
    )
    @app_commands.describe(
        member="対象のユーザー",
        key="キー",
        speed="デフォルトは1.00、下限0.50,上限2.00",
        pitch="デフォルトは0.00、下限-0.15,上限0.15",
    )
    @app_commands.rename(member="ユーザー", key="キー", speed="スピード", pitch="ピッチ")
    @app_commands.guild_only
    @app_commands.checks.has_permissions(administrator=True)
    async def set_other_user_voicevox(
        self,
        interaction: discord.Interaction,
        member: discord.Member,
        key: int,
        speed: app_commands.Range[float, 0.50, 2.00] = 1,
        pitch: app_commands.Range[float, -0.15, 0.15] = 0,
    ):
        """VOICEVOXの声を設定する

        Parameters
        ----------
        interaction : discord.Interaction
            discord.Interaction
        key : int
            キー
        speed : app_commands.Range[float, 0.50, 2.00], optional
            スピード, by default 1
        pitch : app_commands.Range[float,, optional
            ピッチ, by default 0
        """
        assert interaction.guild_id is not None
        await VoiceSettingService.set_guild_voicevox(
            interaction, interaction.guild_id, member.id, key, speed, pitch
        )

    @set_other_user_voiceroid.error
    @set_other_user_voiceroid.error
    @set_other_user_voicevox.error
    async def test_error(
        self, interaction: discord.Interaction, error: app_commands.AppCommandError
    ):
        await interaction.response.defer()
        await interaction.followup.send("権限がありません")


async def setup(bot: commands.Bot):
    await bot.add_cog(UserSetting(bot))
