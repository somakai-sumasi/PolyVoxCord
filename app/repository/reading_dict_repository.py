from dataclasses import asdict
from typing import List

from common.db_setting import session
from common.model_entity_converter import (
    entities_to_models,
    entity_to_model,
    model_to_entity,
    models_to_entities,
)
from entity.reading_dict_entity import ReadingDictEntity
from model.reading_dict import ReadingDict


class ReadingDictRepository:
    @classmethod
    def get_by_id(cls, id: int) -> ReadingDict | None:
        """idで辞書を検索

        Parameters
        ----------
        id : int
            id

        Returns
        -------
        ReadingDict | None
            検索結果
        """
        voice_setting_model: ReadingDict = (
            session.query(ReadingDict).filter_by(id=id).first()
        )

        if voice_setting_model == None:
            return None

        return model_to_entity(voice_setting_model, ReadingDictEntity)

    @classmethod
    def get_by_character(cls, guild_id: int, character: str) -> ReadingDict | None:
        """サーバーごとの書きの検索

        Parameters
        ----------
        guild_id : int
            guild_id
        character : str
            書き

        Returns
        -------
        ReadingDict | None
            検索結果
        """
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
        """サーバー全体の辞書の検索

        Parameters
        ----------
        guild_id : int
            guild_id

        Returns
        -------
        List[ReadingDictEntity]
            検索結果
        """
        voice_setting_models: List[ReadingDictEntity] = session.query(
            ReadingDict
        ).filter_by(guild_id=guild_id)

        return models_to_entities(voice_setting_models, ReadingDictEntity)

    @classmethod
    def create(cls, reading_dict_entity: ReadingDictEntity) -> ReadingDictEntity:
        """作成

        Parameters
        ----------
        reading_dict_entity : ReadingDictEntity
            作成情報

        Returns
        -------
        ReadingDictEntity
            作成後の情報
        """
        voice_setting = entity_to_model(reading_dict_entity, ReadingDict)

        session.add(voice_setting)
        session.commit()

        return cls.get_by_guild_id(reading_dict_entity.guild_id)

    @classmethod
    def update(cls, reading_dict_entity: ReadingDictEntity) -> ReadingDictEntity:
        """更新

        Parameters
        ----------
        reading_dict_entity : ReadingDictEntity
            更新情報

        Returns
        -------
        ReadingDictEntity
            更新後の情報
        """
        session.query(ReadingDict).filter_by(id=reading_dict_entity.id).update(
            asdict(reading_dict_entity)
        )
        session.commit()
        return cls.get_by_id(reading_dict_entity.id)

    @classmethod
    def delete(cls, id: int) -> ReadingDictEntity:
        """削除

        Parameters
        ----------
        id : int
            id

        Returns
        -------
        ReadingDictEntity
            削除後の情報
        """
        session.query(ReadingDict).filter_by(id=id).delete()
        session.commit()

        return cls.get_by_id(id)
