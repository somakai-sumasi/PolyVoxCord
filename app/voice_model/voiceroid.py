import platform
import wave

# Windowsでのみ使用可能なモジュールを条件付きでインポート
if platform.system() == "Windows":
    import pyvcroid2

from entity.voice_setting_entity import VoiceSettingEntity
from voice_model.meta_voice_model import MetaVoiceModel

voice_dicts = [
    {
        "id": "yukari_emo_44",
        "name": "結月ゆかり",
    },
    {
        "id": "akane_west_emo_44",
        "name": "琴葉 茜",
    },
    {
        "id": "aoi_emo_44",
        "name": "琴葉 葵",
    },
    {
        "id": "akari_44",
        "name": "紲星あかり",
    },
    {
        "id": "sora_44",
        "name": "桜乃そら",
    },
    {
        "id": "itako_44",
        "name": "東北イタコ",
    },
    {
        "id": "tsuina_44",
        "name": "ついなちゃん(標準)",
    },
    {
        "id": "tsuina_west_44",
        "name": "ついなちゃん(関西)",
    },
    {
        "id": "yukari_44",
        "name": "結月ゆかり(v1)",
    },
    {
        "id": "tamiyasu_44",
        "name": "民安ともえ(v1)",
    },
    {
        "id": "zunko_44",
        "name": "東北ずん子(v1)",
    },
    {
        "id": "akane_west_44",
        "name": "琴葉 茜(v1)",
    },
    {
        "id": "aoi_44",
        "name": "琴葉 葵(v1)",
    },
    {
        "id": "kiritan_44",
        "name": "東北きりたん(v1)",
    },
    {
        "id": "kou_44",
        "name": "水奈瀬コウ(v1)",
    },
    {
        "id": "seika_44",
        "name": "京町セイカ(v1)",
    },
    {
        "id": "yoshidakun_44",
        "name": "鷹の爪 吉田くん(v1)",
    },
    {
        "id": "shouta_44",
        "name": "月読ショウタ(v1)",
    },
    {
        "id": "ai_44",
        "name": "月読アイ(v1)",
    },
]


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
        path = cls.file_path(__class__.__name__)
        wf = wave.open(path, "wb")
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(44100)
        wf.writeframes(speech)
        wf.close()

        return path

    @classmethod
    def voice_list(cls) -> list[dict[str, str]]:
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

        filtered_dicts = [d for d in voice_dicts if d["id"] in voice_list]

        return filtered_dicts
