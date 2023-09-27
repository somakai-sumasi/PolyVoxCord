from common.db_setting import Base
from sqlalchemy import Column, Float, Integer, Text


class VoiceSetting(Base):
    """読み上げ音声の設定

    Parameters
    ----------
    Base : any
    """

    __tablename__ = "voice_setting"

    user_id = Column(Integer, primary_key=True)
    """ユーザーid
    """
    voice_type = Column(Text)
    """音声のタイプ
    """
    voice_name_key = Column(Text)
    """ボイスキー
    """
    speed = Column(Float)
    """スピード
    """
    pitch = Column(Float)
    """ピッチ
    """
