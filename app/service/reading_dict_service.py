from entity.reading_dict_entity import ReadingDictEntity
from repository.reading_dict_repository import ReadingDictRepository


class ReadingDictService:
    @classmethod
    def add_dict(cls, guild_id: int, character: str, reading: str) -> ReadingDictEntity:
        """辞書に読み書きを追加する

        Parameters
        ----------
        guild_id : int
            guild_id
        character : str
            書き
        reading : str
            読みかた

        Returns
        -------
        ReadingDictEntity
            ReadingDictEntity
        """

        reading_dict = ReadingDictRepository.get_by_character(
            guild_id, character=character
        )
        if reading_dict == None:
            reading_dict = ReadingDictEntity(
                id=None, guild_id=guild_id, character=character, reading=reading
            )
            return ReadingDictRepository.create(reading_dict)
        else:
            reading_dict.reading = reading
            return ReadingDictRepository.update(reading_dict)
