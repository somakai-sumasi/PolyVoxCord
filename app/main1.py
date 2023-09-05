from data_model.read_limit import ReadLimit
from data_model.voice_model import VoiceModel
from common.csv import CSVHandler
from decimal import Decimal

voice_model = VoiceModel({"user_id": 100})
voice_model.speed = Decimal("1")
