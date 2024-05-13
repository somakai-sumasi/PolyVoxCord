import discord
from entity.guild_voice_setting_entity import GuildVoiceSettingEntity
from entity.voice_setting_entity import VoiceSettingEntity
from repository.guild_voice_setting_repository import GuildVoiceSettingRepository
from repository.voice_setting_repository import VoiceSettingRepository
from voice_model.softalk import Softalk
from voice_model.voiceroid import Voiceroid
from voice_model.voicevox import Voicevox


class VoiceSettingService:
    @classmethod
    async def set_voiceroid(
        cls,
        interaction: discord.Interaction,
        guild_id: int | None,
        user_id: int,
        key: int,
        speed: float,
        pitch: float,
    ) -> bool:
        """VOICEROID2のユーザー設定を入れる

        Parameters
        ----------
        interaction : discord.Interaction
            Discord interaction
        guild_id : int | None
            guild_id
        user_id : int
            ユーザーid
        key : int
            音声配列のキー
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

        if 0 < len(voice_list) < key:
            await interaction.followup.send("該当の声がありません", ephemeral=False)
            return False

        voice_name_key = voice_list[key]["id"]

        # DMなどで使用された場合は不要
        if guild_id is not None:
            guild_voice_setting_entity = GuildVoiceSettingEntity(
                guild_id=guild_id,
                user_id=user_id,
                voice_type="VOICEROID",
                voice_name_key=voice_name_key,
                speed=speed,
                pitch=pitch,
            )
            cls.__set_guild_voice_setting(guild_id, user_id, guild_voice_setting_entity)

        voice_setting_entity = VoiceSettingEntity(
            user_id=user_id,
            voice_type="VOICEROID",
            voice_name_key=voice_name_key,
            speed=speed,
            pitch=pitch,
        )
        cls.__set_voice_setting(user_id, voice_setting_entity)

        await interaction.followup.send(
            f"声を{voice_list[key]['name']} スピード:{speed} ピッチ:{pitch}で設定でしました",
            ephemeral=False,
        )
        return True

    @classmethod
    async def set_voicevox(
        cls,
        interaction: discord.Interaction,
        guild_id: int | None,
        user_id: int,
        key: int,
        speed: float,
        pitch: float,
    ) -> bool:
        """VOICEVOXのユーザー設定を入れる

        Parameters
        ----------
        interaction : discord.Interaction
            Discord interaction
        guild_id : int | None
            ギルドid
        user_id : int
            ユーザーid
        key : int
            音声配列のキー
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
        if 0 < len(voice_list) < key:
            await interaction.followup.send("該当の声がありません", ephemeral=False)
            return False

        voice_name_key = voice_list[key]["id"]

        # DMなどで使用された場合は不要
        if guild_id is not None:
            guild_voice_setting_entity = GuildVoiceSettingEntity(
                guild_id=guild_id,
                user_id=user_id,
                voice_type="VOICEVOX",
                voice_name_key=voice_name_key,
                speed=speed,
                pitch=pitch,
            )
            cls.__set_guild_voice_setting(guild_id, user_id, guild_voice_setting_entity)

        voice_setting_entity = VoiceSettingEntity(
            user_id=user_id,
            voice_type="VOICEVOX",
            voice_name_key=voice_name_key,
            speed=speed,
            pitch=pitch,
        )
        cls.__set_voice_setting(user_id, voice_setting_entity)

        await interaction.followup.send(
            f"声を{voice_list[key]['name']} スピード:{speed} ピッチ:{pitch}で設定でしました",
            ephemeral=False,
        )
        return True

    @classmethod
    async def set_softalk(
        cls,
        interaction: discord.Interaction,
        guild_id: int | None,
        user_id: int,
        key: int,
        speed: float,
        pitch: float,
    ) -> bool:
        """SofTalkのユーザー設定を入れる

        Parameters
        ----------
        interaction : discord.Interaction
            Discord interaction
        guild_id : int | None
            ギルドid
        user_id : int
            ユーザーid
        key : int
            音声配列のキー
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
        if 0 < len(voice_list) < key:
            await interaction.followup.send("該当の声がありません", ephemeral=False)
            return False

        voice_name_key = voice_list[key]["id"]

        # DMなどで使用された場合は不要
        if guild_id is not None:
            guild_voice_setting_entity = GuildVoiceSettingEntity(
                guild_id=guild_id,
                user_id=user_id,
                voice_type="Softalk",
                voice_name_key=voice_name_key,
                speed=speed,
                pitch=pitch,
            )
            cls.__set_guild_voice_setting(guild_id, user_id, guild_voice_setting_entity)

        voice_setting_entity = VoiceSettingEntity(
            user_id=user_id,
            voice_type="Softalk",
            voice_name_key=voice_name_key,
            speed=speed,
            pitch=pitch,
        )
        cls.__set_voice_setting(user_id, voice_setting_entity)

        await interaction.followup.send(
            f"声を{voice_list[key]['name']} スピード:{speed} ピッチ:{pitch}で設定でしました",
            ephemeral=False,
        )
        return True

    @classmethod
    async def set_guild_voiceroid(
        cls,
        interaction: discord.Interaction,
        guild_id: int,
        user_id: int,
        key: int,
        speed: float,
        pitch: float,
    ) -> bool:
        """VOICEROID2のサーバーユーザー設定を入れる

        Parameters
        ----------
        interaction : discord.Interaction
            Discord interaction
        guild_id : int
            ギルドid
        user_id : int
            ユーザーid
        key : int
            音声配列のキー
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
        if 0 < len(voice_list) < key:
            await interaction.followup.send("該当の声がありません", ephemeral=False)
            return False

        voice_name_key = voice_list[key]["id"]

        guild_voice_setting_entity = GuildVoiceSettingEntity(
            guild_id=guild_id,
            user_id=user_id,
            voice_type="VOICEROID",
            voice_name_key=voice_name_key,
            speed=speed,
            pitch=pitch,
        )
        cls.__set_guild_voice_setting(guild_id, user_id, guild_voice_setting_entity)

        await interaction.followup.send(
            f"声を{voice_list[key]['name']} スピード:{speed} ピッチ:{pitch}で設定でしました",
            ephemeral=False,
        )
        return True

    @classmethod
    async def set_guild_voicevox(
        cls,
        interaction: discord.Interaction,
        guild_id: int,
        user_id: int,
        key: int,
        speed: float,
        pitch: float,
    ) -> bool:
        """VOICEVOXのサーバーユーザー設定を入れる

        Parameters
        ----------
        interaction : discord.Interaction
            Discord interaction
        guild_id : int
            ギルドid
        user_id : int
            ユーザーid
        key : int
            音声配列のキー
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
        if 0 < len(voice_list) < key:
            await interaction.followup.send("該当の声がありません", ephemeral=False)
            return False

        voice_name_key = voice_list[key]["id"]

        guild_voice_setting_entity = GuildVoiceSettingEntity(
            guild_id=guild_id,
            user_id=user_id,
            voice_type="VOICEVOX",
            voice_name_key=voice_name_key,
            speed=speed,
            pitch=pitch,
        )
        cls.__set_guild_voice_setting(guild_id, user_id, guild_voice_setting_entity)

        await interaction.followup.send(
            f"声を{voice_list[key]['name']} スピード:{speed} ピッチ:{pitch}で設定でしました",
            ephemeral=False,
        )
        return True

    @classmethod
    async def set_guild_softalk(
        cls,
        interaction: discord.Interaction,
        guild_id: int,
        user_id: int,
        key: int,
        speed: float,
        pitch: float,
    ) -> bool:
        """SofTalkのサーバーユーザー設定を入れる

        Parameters
        ----------
        interaction : discord.Interaction
            Discord interaction
        guild_id : int
            ギルドid
        user_id : int
            ユーザーid
        key : int
            音声配列のキー
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
        if 0 < len(voice_list) < key:
            await interaction.followup.send("該当の声がありません", ephemeral=False)
            return False

        voice_name_key = voice_list[key]["id"]

        guild_voice_setting_entity = GuildVoiceSettingEntity(
            guild_id=guild_id,
            user_id=user_id,
            voice_type="Softalk",
            voice_name_key=voice_name_key,
            speed=speed,
            pitch=pitch,
        )
        cls.__set_guild_voice_setting(guild_id, user_id, guild_voice_setting_entity)

        await interaction.followup.send(
            f"声を{voice_list[key]['name']} スピード:{speed} ピッチ:{pitch}で設定でしました",
            ephemeral=False,
        )
        return True

    @classmethod
    def __set_guild_voice_setting(
        cls,
        guild_id: int,
        user_id: int,
        guild_voice_setting_entity: GuildVoiceSettingEntity,
    ):
        """_summary_

        Parameters
        ----------
        guild_id : int
            ギルドid
        user_id : int
            ユーザーid
        guild_voice_setting_entity : GuildVoiceSettingEntity
            サーバー読み上げ音声の設定
        """
        # 設定を登録
        voice_setting = GuildVoiceSettingRepository.get_by_user_id(
            guild_id=guild_id, user_id=user_id
        )
        if voice_setting is None:
            GuildVoiceSettingRepository.create(guild_voice_setting_entity)
        else:
            GuildVoiceSettingRepository.update(guild_voice_setting_entity)

    @classmethod
    def __set_voice_setting(
        cls, user_id: int, voice_setting_entity: VoiceSettingEntity
    ):
        """_summary_

        Parameters
        ----------
        user_id : int
            ユーザーid
        voice_setting_entity : VoiceSettingEntity
            個人読み上げ音声の設定
        """
        # 設定を登録
        voice_setting = VoiceSettingRepository.get_by_user_id(user_id)

        if voice_setting is None:
            VoiceSettingRepository.create(voice_setting_entity)
        else:
            VoiceSettingRepository.update(voice_setting_entity)
