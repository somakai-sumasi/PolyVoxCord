from sqlalchemy import Column, Integer, Text, Float
from common.db_setting import Base


class VoiceSetting(Base):
    __tablename__ = "voice_setting"

    user_id = Column(Integer, primary_key=True)
    voice_type = Column(Text)
    voice_name_key = Column(Text)
    speed = Column(Float)
    pitch = Column(Float)
