from dataclasses import dataclass


@dataclass
class ReadLimitEntity:
    guild_id: int
    upper_limit: int
