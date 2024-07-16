from dataclasses import asdict

from common.db_setting import session
from common.model_entity_converter import entity_to_model, model_to_entity
from entity.guild_voice_setting_entity import GuildVoiceSettingEntity
from model.guild_voice_setting import GuildVoiceSetting


class GuildVoiceSettingRepository:
    @classmethod
    def get_by_user_id(
        cls, guild_id: int, user_id: int
    ) -> GuildVoiceSettingEntity | None:
        """ユーザーの読み上げ上限数を検索

        Parameters
        ----------
        guild_id : int
            guild_id
        user_id : int
            user_id

        Returns
        -------
        GuildVoiceSettingEntity | None
            検索結果
        """
        guild_voice_setting: GuildVoiceSetting = (
            session.query(GuildVoiceSetting)
            .filter_by(guild_id=guild_id, user_id=user_id)
            .first()
        )

        if guild_voice_setting is None:
            return None

        return model_to_entity(guild_voice_setting, GuildVoiceSettingEntity)

    @classmethod
    def create(
        cls, guild_voice_setting: GuildVoiceSettingEntity
    ) -> GuildVoiceSettingEntity:
        """作成

        Parameters
        ----------
        guild_voice_setting : GuildVoiceSettingEntity
            作成情報

        Returns
        -------
        GuildVoiceSettingEntity
            作成後の情報
        """
        voice_setting = entity_to_model(guild_voice_setting, GuildVoiceSetting)

        session.add(voice_setting)
        session.commit()
        return cls.get_by_user_id(
            guild_voice_setting.guild_id, guild_voice_setting.user_id
        )

    @classmethod
    def update(
        cls, guild_voice_setting: GuildVoiceSettingEntity
    ) -> GuildVoiceSettingEntity:
        """更新

        Parameters
        ----------
        voice_setting_entity : GuildVoiceSettingEntity
            更新情報

        Returns
        -------
        GuildVoiceSettingEntity
            更新後の情報
        """
        session.query(GuildVoiceSetting).filter_by(
            guild_id=guild_voice_setting.guild_id, user_id=guild_voice_setting.user_id
        ).update(asdict(guild_voice_setting))
        session.commit()

        return cls.get_by_user_id(
            guild_voice_setting.guild_id, guild_voice_setting.user_id
        )

    @classmethod
    def delete(cls, guild_id: int, user_id: int) -> None:
        """削除

        Parameters
        ----------
        guild_id : int
            guild_id
        user_id : int
            user_id
        """
        session.query(GuildVoiceSetting).filter_by(
            guild_id=guild_id, user_id=user_id
        ).delete()
        session.commit()

        return
