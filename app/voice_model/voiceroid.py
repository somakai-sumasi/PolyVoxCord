from voice_model.meta_voice_model import MetaVoiceModel
from model.voice_setting_model import VoiceSettingModel


class Voiceroid(MetaVoiceModel):
    def create_voice(self, voice_setting: VoiceSettingModel, text: str) -> str:
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
        pass

    def voice_list(self) -> list[str]:
        """自身が持っているボイス名を返す

        Returns
        -------
        list[str]
            ボイス名のリスト
        """
        pass
