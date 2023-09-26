from dataclasses import asdict

from common.db_setting import session
from common.model_entity_converter import entity_to_model, model_to_entity
from entity.voice_setting_entity import VoiceSettingEntity
from model.voice_setting import VoiceSetting


class VoiceSettingRepository:
    @classmethod
    def get_by_user_id(cls, user_id: int) -> VoiceSettingEntity | None:
        voice_setting_model: VoiceSetting = (
            session.query(VoiceSetting).filter_by(user_id=user_id).first()
        )

        if voice_setting_model == None:
            return None

        return model_to_entity(voice_setting_model, VoiceSettingEntity)

    @classmethod
    def create(cls, voice_setting_entity: VoiceSettingEntity) -> VoiceSettingEntity:
        voice_setting = entity_to_model(voice_setting_entity, VoiceSetting)

        session.add(voice_setting)
        session.commit()
        return cls.get_by_user_id(voice_setting_entity.user_id)

    @classmethod
    def update(cls, voice_setting_entity: VoiceSettingEntity) -> VoiceSettingEntity:
        session.query(VoiceSetting).filter_by(
            user_id=voice_setting_entity.user_id
        ).update(asdict(voice_setting_entity))
        session.commit()

        return cls.get_by_user_id(voice_setting_entity.user_id)

    @classmethod
    def delete(cls, user_id: int) -> VoiceSettingEntity:
        session.query(VoiceSetting).filter_by(user_id=user_id).delete()
        session.commit()

        return cls.get_by_user_id(user_id)
