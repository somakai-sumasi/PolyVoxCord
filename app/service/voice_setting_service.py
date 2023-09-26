import discord
from entity.voice_setting_entity import VoiceSettingEntity
from repository.voice_setting_repository import VoiceSettingRepository
from voice_model.softalk import Softalk
from voice_model.voiceroid import Voiceroid
from voice_model.voicevox import Voicevox


class VoiceSettingService:
    @classmethod
    async def set_voiceroid(
        cls,
        interaction: discord.Interaction,
        user_id: int,
        voice_name_key: str,
        speed: float,
        pitch: float,
    ):
        await interaction.response.defer()
        
        voice_list = Voiceroid.voice_list()
        if not (voice_name_key in voice_list):
            await interaction.followup.send(f"該当の声がありません", ephemeral=False)
            return False

        # 設定を登録
        voice_setting = VoiceSettingRepository.get_by_user_id(user_id=user_id)
        entity = VoiceSettingEntity(
            user_id=user_id,
            voice_type="VOICEROID",
            voice_name_key=voice_name_key,
            speed=speed,
            pitch=pitch,
        )
        if voice_setting == None:
            VoiceSettingRepository.create(entity)
        else:
            VoiceSettingRepository.update(entity)

        await interaction.followup.send(
            f"声を{voice_list[voice_name_key]} スピード:{speed} ピッチ:{pitch}で設定でしました",
            ephemeral=False,
        )
        return True

    @classmethod
    async def set_voicevox(
        cls,
        interaction: discord.Interaction,
        user_id: int,
        voice_name_key: str,
        speed: float,
        pitch: float,
    ) -> bool:
        await interaction.response.defer()

        voice_list = Voicevox.voice_list()
        if not (voice_name_key in voice_list):
            await interaction.followup.send(f"該当の声がありません", ephemeral=False)
            return False

        # 設定を登録
        voice_setting = VoiceSettingRepository.get_by_user_id(user_id=user_id)
        entity = VoiceSettingEntity(
            user_id=user_id,
            voice_type="VOICEVOX",
            voice_name_key=voice_name_key,
            speed=speed,
            pitch=pitch,
        )
        if voice_setting == None:
            VoiceSettingRepository.create(entity)
        else:
            VoiceSettingRepository.update(entity)

        await interaction.followup.send(
            f"声を{voice_list[voice_name_key]} スピード:{speed} ピッチ:{pitch}で設定でしました",
            ephemeral=False,
        )
        return True

    @classmethod
    async def set_softalk(
        cls,
        interaction: discord.Interaction,
        user_id: int,
        voice_name_key: str,
        speed: float,
        pitch: float,
    ):
        await interaction.response.defer()

        voice_list = Softalk.voice_list()
        if not (voice_name_key in voice_list):
            await interaction.followup.send(f"該当の声がありません", ephemeral=False)
            return False

        # 設定を登録
        voice_setting = VoiceSettingRepository.get_by_user_id(user_id=user_id)
        entity = VoiceSettingEntity(
            user_id=user_id,
            voice_type="Softalk",
            voice_name_key=voice_name_key,
            speed=speed,
            pitch=pitch,
        )
        if voice_setting == None:
            VoiceSettingRepository.create(entity)
        else:
            VoiceSettingRepository.update(entity)

        await interaction.followup.send(
            f"声を{voice_list[voice_name_key]} スピード:{speed} ピッチ:{pitch}で設定でしました",
            ephemeral=False,
        )
        return True
