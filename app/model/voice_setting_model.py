from sqlalchemy import Column, Integer, Text, Float
from common.setting import Base


class VoiceSettingModel(Base):
    __tablename__ = "voice_setting"

    id = Column(Integer, primary_key=True)
    voice_type = Column(Text)
    voice_name_key = Column(Text)
    speed = Column(Float)
    pitch = Column(Float)
