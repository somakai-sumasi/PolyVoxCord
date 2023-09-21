from voice_model.meta_voice_model import MetaVoiceModel
from entity.voice_setting_entity import VoiceSettingEntity
import pyvcroid2
import winsound
import wave


class Voiceroid(MetaVoiceModel):
    @classmethod
    def create_voice(cls, voice_setting: VoiceSettingEntity, text: str) -> str:
        """読み上げ音声を作成する

        Parameters
        ----------
        text : str
            読み上げするテキスト

        Returns
        -------
        str
            音声ファイルのパス
        """
        vc = pyvcroid2.VcRoid2()

        language = "standard"
        if voice_setting.voice_name_key == "akane_west_emo_44":
            language = "standard_kansai"

        vc.loadLanguage(language)
        vc.loadVoice(voice_setting.voice_name_key)

        vc.param.volume = 1
        vc.param.speed = voice_setting.speed
        vc.param.pitch = voice_setting.pitch
        vc.param.emphasis = 1
        vc.param.pauseMiddle = 150
        vc.param.pauseLong = 370
        vc.param.pauseSentence = 800
        vc.param.masterVolume = 1

        speech = vc.textToSpeech(text)[0]

        wf = wave.open("./wav/" + cls.create_filename(__class__.__name__), "wb")
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(44100)
        wf.writeframes(speech)
        wf.close()

        path = "./wav/" + cls.create_filename(__class__.__name__)
        with open(path, mode="wb") as f:
            f.write(speech)

    @classmethod
    def voice_list() -> list[str]:
        """自身が持っているボイス名を返す

        Returns
        -------
        list[str]
            ボイス名のリスト
        """
        vc = pyvcroid2.VcRoid2()
        voice_list = vc.listVoices()

        pass
