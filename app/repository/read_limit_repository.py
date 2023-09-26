from dataclasses import asdict

from common.db_setting import session
from common.model_entity_converter import entity_to_model, model_to_entity
from entity.read_limit_entity import ReadLimitEntity
from model.read_limit import ReadLimit


class ReadLimitRepository:
    @classmethod
    def get_by_guild_id(cls, guild_id: int) -> ReadLimitEntity | None:
        voice_setting_model: ReadLimit = (
            session.query(ReadLimit).filter_by(guild_id=guild_id).first()
        )

        if voice_setting_model == None:
            return None

        return model_to_entity(voice_setting_model, ReadLimitEntity)

    @classmethod
    def create(cls, read_limit_entity: ReadLimitEntity) -> ReadLimitEntity:
        voice_setting = entity_to_model(read_limit_entity, ReadLimit)

        session.add(voice_setting)
        session.commit()

        return cls.get_by_guild_id(read_limit_entity.guild_id)

    @classmethod
    def update(cls, read_limit_entity: ReadLimitEntity) -> ReadLimitEntity:
        session.query(ReadLimit).filter_by(guild_id=read_limit_entity.guild_id).update(
            asdict(read_limit_entity)
        )
        session.commit()

        return cls.get_by_guild_id(read_limit_entity.guild_id)

    @classmethod
    def delete(cls, guild_id: int) -> ReadLimitEntity:
        session.query(ReadLimit).filter_by(user_id=guild_id).delete()
        session.commit()

        return cls.get_by_guild_id(guild_id)
