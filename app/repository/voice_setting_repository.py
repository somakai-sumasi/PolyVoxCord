from dataclasses import asdict
from common.db_setting import session
from common.model_entity_converter import model_to_entity, entity_to_model
from model.voice_setting import VoiceSetting
from entity.voice_setting_entity import VoiceSettingEntity


class VoiceSettingRepository:
    @classmethod
    def get_by_user_id(cls, user_id: int) -> VoiceSettingEntity:
        voice_setting_model: VoiceSetting = (
            session.query(VoiceSetting).filter_by(user_id=user_id).first()
        )

        if voice_setting_model == None:
            return None

        return model_to_entity(voice_setting_model, VoiceSettingEntity)

    @classmethod
    def create(cls, voice_setting_entity: VoiceSettingEntity) -> VoiceSettingEntity:
        voice_setting = entity_to_model(voice_setting_entity, VoiceSetting)

        with session.begin():
            session.add(voice_setting)

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
