from common.db_setting import Base
from sqlalchemy import Column, Float, Integer, Text


class VoiceSetting(Base):
    __tablename__ = "voice_setting"

    user_id = Column(Integer, primary_key=True)
    voice_type = Column(Text)
    voice_name_key = Column(Text)
    speed = Column(Float)
    pitch = Column(Float)
