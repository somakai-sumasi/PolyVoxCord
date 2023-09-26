from common.db_setting import Base
from sqlalchemy import Column, Float, Integer, Text


class ReadLimit(Base):
    __tablename__ = "read_limit"

    guild_id = Column(Integer, primary_key=True)
    upper_limit = Column(Integer)
