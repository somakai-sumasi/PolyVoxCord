import platform
import wave

# Windowsでのみ使用可能なモジュールを条件付きでインポート
if platform.system() == "Windows":
    import pyvcroid2

from entity.voice_setting_entity import VoiceSettingEntity
from voice_model.meta_voice_model import MetaVoiceModel

voice_dict = {
    "yukari_emo_44": "結月ゆかり",
    "akane_west_emo_44": "琴葉 茜",
    "aoi_emo_44": "琴葉 葵",
    "akari_44": "紲星あかり",
    "sora_44": "桜乃そら",
    "itako_44": "東北イタコ",
    "tsuina_44": "ついなちゃん(標準)",
    "tsuina_west_44": "ついなちゃん(関西)",
    "yukari_44": "結月ゆかり(v1)",
    "tamiyasu_44": "民安ともえ(v1)",
    "zunko_44": "東北ずん子(v1)",
    "akane_west_44": "琴葉 茜(v1)",
    "aoi_44": "琴葉 葵(v1)",
    "kiritan_44": "東北きりたん(v1)",
    "kou_44": "水奈瀬コウ(v1)",
    "seika_44": "京町セイカ(v1)",
    "yoshidakun_44": "鷹の爪 吉田くん(v1)",
    "shouta_44": "月読ショウタ(v1)",
    "ai_44": "月読アイ(v1)",
}


class Voiceroid(MetaVoiceModel):
    @classmethod
    def create_voice(cls, voice_setting: VoiceSettingEntity, text: str) -> str:
        """読み上げ音声を作成する

        Parameters
        ----------
        voice_setting : VoiceSettingEntity
            ボイスの設定
        text : str
            読み上げするテキスト

        Returns
        -------
        str
            音声ファイルのパス
        """

        # Windows以外での動作の場合、エラー
        if platform.system() != "Windows":
            raise NotImplementedError("Voiceroid is only available on Windows.")

        vc = pyvcroid2.VcRoid2()

        # 琴葉茜の場合は関西弁にする
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

        wf = wave.open("./tmp/wav/" + cls.create_filename(__class__.__name__), "wb")
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(44100)
        wf.writeframes(speech)
        wf.close()

        path = "./wav/" + cls.create_filename(__class__.__name__)
        with open(path, mode="wb") as f:
            f.write(speech)

        return path

    @classmethod
    def voice_list(cls) -> dict[str, str]:
        """自身が持っているボイス名を返す

        Returns
        -------
        dict[str, str]
            ボイス名のリスト
        """

        # Windows以外での動作の場合、何も返さない
        if platform.system() != "Windows":
            return {}

        vc = pyvcroid2.VcRoid2()
        voice_list = vc.listVoices()

        filtered_dict = {k: v for k, v in voice_dict.items() if k in voice_list}

        return filtered_dict
