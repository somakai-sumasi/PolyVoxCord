from common.db_setting import Base
from sqlalchemy import Column, Float, Integer, Text


class ReadingDict(Base):
    __tablename__ = "reading_dict"

    id = Column(Integer, primary_key=True)
    guild_id = Column(Integer)
    character = Column(Text)
    reading = Column(Text)
