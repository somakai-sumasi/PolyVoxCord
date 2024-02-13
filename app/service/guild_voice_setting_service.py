import discord
from entity.guild_voice_setting_entity import GuildVoiceSettingEntity
from repository.guild_voice_setting_repository import GuildVoiceSettingRepository
from voice_model.softalk import Softalk
from voice_model.voiceroid import Voiceroid
from voice_model.voicevox import Voicevox


class GuildVoiceSettingService:
    @classmethod
    async def set_voiceroid(
        cls,
        interaction: discord.Interaction,
        guild_id: int,
        user_id: int,
        voice_name_key: str,
        speed: float,
        pitch: float,
    ) -> bool:
        """VOICEROID2のユーザー設定を入れる

        Parameters
        ----------
        interaction : discord.Interaction
            Discord interaction
        guild_id : int
            guild_id
        user_id : int
            user_id
        voice_name_key : str
            ボイスのキーとなる名前
        speed : float
            スピード
        pitch : float
            ピッチ

        Returns
        -------
        bool
            可否
        """
        await interaction.response.defer()

        voice_list = Voiceroid.voice_list()
        if not (voice_name_key in voice_list):
            await interaction.followup.send(f"該当の声がありません", ephemeral=False)
            return False

        # 設定を登録
        voice_setting = GuildVoiceSettingRepository.get_by_user_id(
            guild_id=guild_id, user_id=user_id
        )
        entity = GuildVoiceSettingEntity(
            guild_id=guild_id,
            user_id=user_id,
            voice_type="VOICEROID",
            voice_name_key=voice_name_key,
            speed=speed,
            pitch=pitch,
        )
        if voice_setting == None:
            GuildVoiceSettingRepository.create(entity)
        else:
            GuildVoiceSettingRepository.update(entity)

        await interaction.followup.send(
            f"声を{voice_list[voice_name_key]} スピード:{speed} ピッチ:{pitch}で設定でしました",
            ephemeral=False,
        )
        return True

    @classmethod
    async def set_voicevox(
        cls,
        interaction: discord.Interaction,
        guild_id: int,
        user_id: int,
        voice_name_key: str,
        speed: float,
        pitch: float,
    ) -> bool:
        """VOICEVOXのユーザー設定を入れる

        Parameters
        ----------
        interaction : discord.Interaction
            Discord interaction
        guild_id : int
            guild_id
        user_id : int
            user_id
        voice_name_key : str
            ボイスのキーとなる名前
        speed : float
            スピード
        pitch : float
            ピッチ

        Returns
        -------
        bool
            可否
        """

        await interaction.response.defer()

        voice_list = Voicevox.voice_list()
        if not (voice_name_key in voice_list):
            await interaction.followup.send(f"該当の声がありません", ephemeral=False)
            return False

        # 設定を登録
        voice_setting = GuildVoiceSettingRepository.get_by_user_id(
            guild_id=guild_id, user_id=user_id
        )
        entity = GuildVoiceSettingEntity(
            guild_id=guild_id,
            user_id=user_id,
            voice_type="VOICEVOX",
            voice_name_key=voice_name_key,
            speed=speed,
            pitch=pitch,
        )
        if voice_setting == None:
            GuildVoiceSettingRepository.create(entity)
        else:
            GuildVoiceSettingRepository.update(entity)

        await interaction.followup.send(
            f"声を{voice_list[voice_name_key]} スピード:{speed} ピッチ:{pitch}で設定でしました",
            ephemeral=False,
        )
        return True

    @classmethod
    async def set_softalk(
        cls,
        interaction: discord.Interaction,
        guild_id: int,
        user_id: int,
        voice_name_key: str,
        speed: float,
        pitch: float,
    ) -> bool:
        """SofTalkのユーザー設定を入れる

        Parameters
        ----------
        interaction : discord.Interaction
            Discord interaction
        guild_id : int
            guild_id
        user_id : int
            user_id
        voice_name_key : str
            ボイスのキーとなる名前
        speed : float
            スピード
        pitch : float
            ピッチ

        Returns
        -------
        bool
            可否
        """
        await interaction.response.defer()

        voice_list = Softalk.voice_list()
        if not (voice_name_key in voice_list):
            await interaction.followup.send(f"該当の声がありません", ephemeral=False)
            return False

        # 設定を登録
        voice_setting = GuildVoiceSettingRepository.get_by_user_id(
            guild_id=guild_id, user_id=user_id
        )
        entity = GuildVoiceSettingEntity(
            guild_id=guild_id,
            user_id=user_id,
            voice_type="Softalk",
            voice_name_key=voice_name_key,
            speed=speed,
            pitch=pitch,
        )
        if voice_setting == None:
            GuildVoiceSettingRepository.create(entity)
        else:
            GuildVoiceSettingRepository.update(entity)

        await interaction.followup.send(
            f"声を{voice_list[voice_name_key]} スピード:{speed} ピッチ:{pitch}で設定でしました",
            ephemeral=False,
        )
        return True
