from entity.read_limit_entity import ReadLimitEntity
from repository.read_limit_repository import ReadLimitRepository


class ReadLimitService:
    @classmethod
    def set_limit(cls, guild_id: int, upper_limit: int) -> ReadLimitEntity:
        """読上げ上限文字数を設定

        Parameters
        ----------
        guild_id : int
            guild_id
        upper_limit : int
            読上げ上限文字数

        Returns
        -------
        ReadLimitEntity
            ReadLimitEntity
        """

        read_limit = ReadLimitRepository.get_by_guild_id(guild_id)
        if read_limit == None:
            read_limit = ReadLimitEntity(guild_id=guild_id, upper_limit=upper_limit)
            return ReadLimitRepository.create(read_limit)
        else:
            read_limit.upper_limit = upper_limit
            return ReadLimitRepository.update(read_limit)
