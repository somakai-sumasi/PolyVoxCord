from repository.voice_setting_repository import VoiceSettingRepository
from entity.voice_setting_entity import VoiceSettingEntity


class VoiceSettingService:
    @classmethod
    def set_voiceroid(
        cls, user_id: int, voice_name_key: str, speed: float, pitch: float
    ):
        ...

    @classmethod
    def set_voicevox(
        cls, user_id: int, voice_name_key: str, speed: float, pitch: float
    ):
        voice_setting = VoiceSettingRepository.get_by_user_id(user_id=user_id)
        if voice_setting == None:
            VoiceSettingRepository.create(
                VoiceSettingEntity(
                    user_id=user_id,
                    voice_type="VOICEVOX",
                    voice_name_key=voice_name_key,
                    speed=speed,
                    pitch=pitch,
                )
            )
        else:
            VoiceSettingRepository.update(
                VoiceSettingEntity(
                    user_id=user_id,
                    voice_type="VOICEVOX",
                    voice_name_key=voice_name_key,
                    speed=speed,
                    pitch=pitch,
                )
            )
        ...

    @classmethod
    def set_softalk(cls, user_id: int, voice_name_key: str, speed: float, pitch: float):
        ...
