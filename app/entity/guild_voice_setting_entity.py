from dataclasses import dataclass


@dataclass
class GuildVoiceSettingEntity:
    """読み上げ音声の設定"""

    guild_id: int
    """ギルドid
    """
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
