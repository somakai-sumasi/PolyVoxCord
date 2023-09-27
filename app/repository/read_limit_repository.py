from dataclasses import asdict

from common.db_setting import session
from common.model_entity_converter import entity_to_model, model_to_entity
from entity.read_limit_entity import ReadLimitEntity
from model.read_limit import ReadLimit


class ReadLimitRepository:
    @classmethod
    def get_by_guild_id(cls, guild_id: int) -> ReadLimitEntity | None:
        """サーバーの読み上げ上限数を検索

        Parameters
        ----------
        guild_id : int
            guild_id

        Returns
        -------
        ReadLimitEntity | None
            検索結果
        """
        voice_setting_model: ReadLimit = (
            session.query(ReadLimit).filter_by(guild_id=guild_id).first()
        )

        if voice_setting_model == None:
            return None

        return model_to_entity(voice_setting_model, ReadLimitEntity)

    @classmethod
    def create(cls, read_limit_entity: ReadLimitEntity) -> ReadLimitEntity:
        """作成

        Parameters
        ----------
        read_limit_entity : ReadLimitEntity
            作成情報

        Returns
        -------
        ReadLimitEntity
            作成後の情報
        """
        voice_setting = entity_to_model(read_limit_entity, ReadLimit)

        session.add(voice_setting)
        session.commit()

        return cls.get_by_guild_id(read_limit_entity.guild_id)

    @classmethod
    def update(cls, read_limit_entity: ReadLimitEntity) -> ReadLimitEntity:
        """更新

        Parameters
        ----------
        read_limit_entity : ReadLimitEntity
            更新情報

        Returns
        -------
        ReadLimitEntity
            更新後の情報
        """
        session.query(ReadLimit).filter_by(guild_id=read_limit_entity.guild_id).update(
            asdict(read_limit_entity)
        )
        session.commit()

        return cls.get_by_guild_id(read_limit_entity.guild_id)

    @classmethod
    def delete(cls, guild_id: int) -> ReadLimitEntity:
        """削除

        Parameters
        ----------
        guild_id : int
            guild_id

        Returns
        -------
        ReadLimitEntity
            削除後の情報
        """
        session.query(ReadLimit).filter_by(user_id=guild_id).delete()
        session.commit()

        return cls.get_by_guild_id(guild_id)
