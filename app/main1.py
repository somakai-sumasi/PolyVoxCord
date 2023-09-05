from data_model.read_limit import ReadLimit
from data_model.voice_setting_model import VoiceSettingModel
from common.csv import CSVHandler
from decimal import Decimal

voice_setting_model = VoiceSettingModel({"user_id": 100})
voice_setting_model.speed = Decimal("1")
