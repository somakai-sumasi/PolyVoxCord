from dataclasses import dataclass, asdict


@dataclass
class VoiceSettingEntity:
    user_id: int
    voice_type: str
    voice_name_key: str
    speed: float
    pitch: float
