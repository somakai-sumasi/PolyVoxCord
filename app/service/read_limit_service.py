from entity.read_limit_entity import ReadLimitEntity
from repository.read_limit_repository import ReadLimitRepository


class ReadLimitService:
    @classmethod
    def set_limit(cls, guild_id: int, upper_limit: int):
        read_limit = ReadLimitRepository.get_by_guild_id(guild_id)
        if read_limit == None:
            read_limit = ReadLimitEntity(guild_id=guild_id, upper_limit=upper_limit)
            return cls.create(read_limit)
        else:
            read_limit.upper_limit = upper_limit
            return cls.update(read_limit)

    @classmethod
    def create(cls, read_limit_entity: ReadLimitEntity):
        return ReadLimitRepository.create(read_limit_entity)

    @classmethod
    def update(cls, read_limit_entity: ReadLimitEntity):
        return ReadLimitRepository.update(read_limit_entity)
