from entity.reading_dict_entity import ReadingDictEntity
from repository.reading_dict_repository import ReadingDictRepository


class ReadingDictService:
    @classmethod
    def add_dict(cls, guild_id: int, character: str, reading: str):
        reading_dict = ReadingDictRepository.get_by_character(
            guild_id, character=character
        )
        if reading_dict == None:
            reading_dict = ReadingDictEntity(
                id=None, guild_id=guild_id, character=character, reading=reading
            )
            return cls.create(reading_dict)
        else:
            reading_dict.reading = reading
            return cls.update(reading_dict)

    @classmethod
    def create(cls, reading_dict_entity: ReadingDictEntity):
        return ReadingDictRepository.create(reading_dict_entity)

    @classmethod
    def update(cls, reading_dict_entity: ReadingDictEntity):
        return ReadingDictRepository.update(reading_dict_entity)
