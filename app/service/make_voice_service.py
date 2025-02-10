import asyncio
import os

from common.assign_kana import get_pronunciation
from common.text_format import conv_discord_object, omit_url
from entity.read_limit_entity import ReadLimitEntity
from entity.voice_setting_entity import VoiceSettingEntity
from repository.guild_voice_setting_repository import GuildVoiceSettingRepository
from repository.read_limit_repository import ReadLimitRepository
from repository.reading_dict_repository import ReadingDictRepository
from repository.voice_setting_repository import VoiceSettingRepository
from voice_model.meta_voice_model import MetaVoiceModel
from voice_model.softalk import Softalk
from voice_model.voiceroid import Voiceroid
from voice_model.voicevox import Voicevox


class MakeVoiceService:
    def __init__(self, guild_id: int, user_id: int):
        self.guild_id = guild_id
        self.user_id = user_id
        self.voice_setting = self.__fetch_voice_setting(guild_id, user_id)

    def __fetch_voice_setting(self, guild_id: int, user_id: int) -> VoiceSettingEntity:
        """音声設定を取得

        Parameters
        ----------
        guild_id : int
            guild_id
        user_id : int
            guild_id

        Returns
        -------
        VoiceSettingEntity
            VoiceSettingEntity
        """

        voice_setting = GuildVoiceSettingRepository.get_by_user_id(guild_id, user_id)
        # サーバー別の設定がない場合はこちらを使う
        if voice_setting is None:
            voice_setting = VoiceSettingRepository.get_by_user_id(user_id)

        # 登録されていない場合はデフォルト設定で読み上げ
        if voice_setting is None:
            voice_setting = VoiceSettingEntity(
                user_id=user_id,
                voice_type="Softalk",
                voice_name_key="/T:7/U:0",
                speed=120,
                pitch=100,
            )

        return voice_setting

    async def make_voice(self, text: str, is_omit_url=True, is_read_limit=True) -> str:
        """音声を作成

        Parameters
        ----------
        text : str
            読み上げる文字
        is_omit_url : bool, optional
            URLを省略するかどうか, by default True
        is_read_limit : bool, optional
            読み上げ文字数に制限をかけるかどうか, by default True

        Returns
        -------
        str
            作成した音声のパス
        """

        text = self.__conv_text(text, is_omit_url, is_read_limit)
        voice_type = self.voice_setting.voice_type

        voice_model: MetaVoiceModel = None
        if voice_type == "VOICEROID":
            voice_model = Voiceroid()

        if voice_type == "VOICEVOX":
            voice_model = Voicevox()

        if voice_type == "Softalk":
            voice_model = Softalk()
        path = voice_model.create_voice(self.voice_setting, text)

        # ファイルが出来るまで待つ
        while not (os.access(path, os.W_OK)):
            await asyncio.sleep(0.1)

        return path

    def __conv_text(self, text, is_omit_url=True, is_read_limit=True) -> str:
        """テキストを読み上げる形に変換

        Parameters
        ----------
        text : str
            読み上げる文字
        is_omit_url : bool, optional
            URLを省略するかどうか, by default True
        is_read_limit : bool, optional
            読み上げ文字数に制限をかけるかどうか, by default True

        Returns
        -------
        str
            読み上げる文字
        """

        text = conv_discord_object(text)
        if is_omit_url:
            text = omit_url(text)

        text = self.__match_with_dictionary(text)

        if is_read_limit:
            text = self.__limit_length(text)

        text = get_pronunciation(text)

        return text

    def __limit_length(self, text: str) -> str:
        """最大文字数を超える場合カット

        Parameters
        ----------
        text : str
            変換する文字

        Returns
        -------
        str
            変換後の文字
        """
        read_limit = ReadLimitRepository.get_by_guild_id(self.guild_id)
        if read_limit is None:
            read_limit = ReadLimitEntity(guild_id=self.guild_id, upper_limit=250)
        upper_limit = read_limit.upper_limit

        if len(text) > upper_limit:
            text = text[:upper_limit] + "\n以下略\n"
        return text

    def __match_with_dictionary(self, text: str) -> str:
        """読みを反映した、読み上げ文字にする

        Parameters
        ----------
        guild_id : int
            guild_id
        text : str
            変換する文字

        Returns
        -------
        str
            変換後の文字
        """

        reading_dicts = ReadingDictRepository.get_by_guild_id(self.guild_id)
        result_text = text

        read_list = []  # あとでまとめて変換するときの読み仮名リスト
        for i, reading_dict in enumerate(reading_dicts):
            result_text = result_text.replace(
                reading_dict.character, "{" + str(i) + "}"
            )
            read_list.append(reading_dict.reading)  # 変換が発生した順に読みがなリストに追加

        result_text = result_text.format(*read_list)  # 読み仮名リストを引数にとる

        return result_text
