from typing import List
from dataclasses import asdict
from common.db_setting import session
from common.model_entity_converter import (
    model_to_entity,
    models_to_entities,
    entity_to_model,
    entities_to_models,
)
from model.reading_dict import ReadingDict
from entity.reading_dict_entity import ReadingDictEntity


class ReadingDictRepository:
    @classmethod
    def get_by_id(cls, id: int) -> ReadingDict | None:
        voice_setting_model: ReadingDict = (
            session.query(ReadingDict).filter_by(id=id).first()
        )

        if voice_setting_model == None:
            return None

        return model_to_entity(voice_setting_model, ReadingDictEntity)

    @classmethod
    def get_by_character(cls, guild_id: int, character: str) -> ReadingDict | None:
        voice_setting_model: ReadingDict = (
            session.query(ReadingDict)
            .filter_by(guild_id=guild_id, character=character)
            .first()
        )

        if voice_setting_model == None:
            return None

        return model_to_entity(voice_setting_model, ReadingDictEntity)

    @classmethod
    def get_by_guild_id(cls, guild_id: int) -> List[ReadingDictEntity]:
        voice_setting_models: List[ReadingDictEntity] = session.query(
            ReadingDict
        ).filter_by(guild_id=guild_id)

        return models_to_entities(voice_setting_models, ReadingDictEntity)

    @classmethod
    def create(cls, reading_dict_entity: ReadingDictEntity) -> ReadingDictEntity:
        voice_setting = entity_to_model(reading_dict_entity, ReadingDict)

        session.add(voice_setting)
        session.commit()

        return cls.get_by_guild_id(reading_dict_entity.guild_id)

    @classmethod
    def update(cls, reading_dict_entity: ReadingDictEntity) -> ReadingDictEntity:
        session.query(ReadingDict).filter_by(id=reading_dict_entity.id).update(
            asdict(reading_dict_entity)
        )
        session.commit()
        return cls.get_by_id(reading_dict_entity.id)

    @classmethod
    def delete(cls, id: int) -> ReadingDictEntity:
        session.query(ReadingDict).filter_by(id=id).delete()
        session.commit()

        return cls.get_by_id(id)
