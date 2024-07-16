from common.db_setting import Base
from sqlalchemy import Column, Integer, Text


class ReadingDict(Base):
    """読み上げ時の辞書の管理

    Parameters
    ----------
    Base : any
    """

    __tablename__ = "reading_dict"

    id = Column(Integer, primary_key=True)
    """id
    """
    guild_id = Column(Integer)
    """ギルドid
    """
    character = Column(Text)
    """書き
    """
    reading = Column(Text)
    """読み
    """
