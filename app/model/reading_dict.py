from sqlalchemy import Column, Integer, Text, Float
from common.setting import Base


class ReadingDict(Base):
    __tablename__ = "reading_dict"

    id = Column(Integer, primary_key=True)
    guild_id = Column(Integer)
    character = Column(Text)
    reading = Column(Text)
