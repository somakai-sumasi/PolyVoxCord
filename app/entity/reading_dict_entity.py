from dataclasses import dataclass


@dataclass
class ReadingDictEntity:
    """読み上げ時の辞書の管理"""

    id: int | None
    """id
    """
    guild_id: int
    """ギルドid
    """
    character: str
    """書き
    """
    reading: str
    """読み
    """
