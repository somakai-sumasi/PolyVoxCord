from dataclasses import dataclass


@dataclass
class ReadLimitEntity:
    """読み上げ上限数の管理"""

    guild_id: int
    """ギルドid
    """
    upper_limit: int
    """読み上げ上限数
    """
