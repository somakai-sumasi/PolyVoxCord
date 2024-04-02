from dataclasses import dataclass


@dataclass
class VoiceSettingEntity:
    """個人読み上げ音声の設定"""

    user_id: int
    """ユーザーid
    """
    voice_type: str
    """音声のタイプ
    """
    voice_name_key: str
    """ボイスキー
    """
    speed: float
    """スピード
    """
    pitch: float
    """ピッチ
    """
