# from model.voice_setting import VoiceSetting
# from entity.voice_setting_entity import VoiceSettingEntity
# from common.db_setting import session
# from typing import TypeVar, Type, Dict, Any
# from dataclasses import dataclass, asdict
# from voice_model.sof_talk import SofTalk
#
## 抽象化した変換メソッド
# T = TypeVar("T")
# U = TypeVar("U")
#
#
# def model_to_entity(model: T, entity_cls: Type[U]) -> U:
#    model_dict = {c.name: getattr(model, c.name) for c in model.__table__.columns}
#    return entity_cls(**model_dict)
#
#
# def entity_to_model(entity: U, model_cls: Type[T]) -> T:
#    entity_dict = asdict(entity)
#    return model_cls(**entity_dict)
#
#
# voice_setting_model: VoiceSetting = session.query(VoiceSetting).filter_by(id=1).first()
# voice_setting_entity: VoiceSettingEntity = model_to_entity(
#    voice_setting_model, VoiceSettingEntity
# )
# user_model = entity_to_model(voice_setting_entity, VoiceSetting)
#
# print(user_model)


# from repository.voice_setting_repository import VoiceSettingRepository
# from entity.voice_setting_entity import VoiceSettingEntity
#
##
# a = VoiceSettingRepository.get_voice_setting_by_id(2)
#
# print(a)

# voice_setting_entity = VoiceSettingEntity(
#    id=3, voice_type="test", voice_name_key="bbb", speed=120, pitch=1000
# )
# VoiceSettingRepository.delete(voice_setting_entity)

from voice_model.voicevox import Voicevox
from entity.voice_setting_entity import VoiceSettingEntity

Voicevox.voice_list()

voice_setting_entity = VoiceSettingEntity(
   user_id=3, voice_type="test", voice_name_key="2", speed=120, pitch=1000
)
Voicevox.create_voice(voice_setting_entity, 'テストです')