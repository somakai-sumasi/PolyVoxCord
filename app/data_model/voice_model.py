from data_model.base_model import BaseModel
from decimal import Decimal


class VoiceModel(BaseModel):
    def __init__(self, index_value):
        FILE = "app/data/VoiceModel.csv"
        INDEX_COLUMNS = {"user_id": int}
        NON_INDEX_COLUMNS = {
            "voice_type": str,
            "voice_name_key": str,
            "speed": Decimal,
            "pitch": Decimal,
        }

        super().__init__(FILE, index_value, INDEX_COLUMNS, NON_INDEX_COLUMNS)

    @property
    def voice_type(self) -> str:
        return self.data.get("voice_type", None)

    @voice_type.setter
    def voice_type(self, value: str):
        self.data["voice_type"] = value
        self.save()

    @property
    def voice_name_key(self) -> str:
        return self.data.get("voice_name_key", None)

    @voice_name_key.setter
    def voice_name_key(self, value: str):
        self.data["voice_name_key"] = value
        self.save()

    @property
    def speed(self) -> Decimal:
        return self.data.get("speed", None)

    @speed.setter
    def speed(self, value: Decimal):
        self.data["speed"] = value
        self.save()

    @property
    def pitch(self) -> Decimal:
        return self.data.get("pitch", None)

    @pitch.setter
    def pitch(self, value: Decimal):
        self.data["pitch"] = value
        self.save()
