from common.db_setting import Base
from sqlalchemy import Column, Float, Integer, Text


class ReadLimit(Base):
    """読み上げ数の管理

    Parameters
    ----------
    Base : any
    """

    __tablename__ = "read_limit"

    guild_id = Column(Integer, primary_key=True)
    """ギルドid
    """
    upper_limit = Column(Integer)
    """読み上げ上限数
    """
