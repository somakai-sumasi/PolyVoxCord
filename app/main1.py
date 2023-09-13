from model.voice_setting_model import VoiceSettingModel
from common.setting import session

from voice_model.sof_talk import SofTalk

voice_setting_model: VoiceSettingModel = (
    session.query(VoiceSettingModel).filter_by(id=1).first()
)

SofTalk.create_voice(voice_setting_model, "aaaa")
