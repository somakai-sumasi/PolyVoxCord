from sqlalchemy import Column, Integer, Text, Float
from common.setting import Base


class ReadLimit(Base):
    __tablename__ = "read_limit"

    guild_id = Column(Integer, primary_key=True)
    upper_limit = Column(Integer)
