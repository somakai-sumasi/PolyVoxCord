from dataclasses import dataclass


@dataclass
class ReadingDictEntity:
    id: int | None
    guild_id: int
    character: str
    reading: str
