from dataclasses import asdict

from common.db_setting import session
from common.model_entity_converter import entity_to_model, model_to_entity
from entity.guild_voice_setting_entity import GuildVoiceSettingEntity
from model.guild_voice_setting import GuildVoiceSetting


class GuildVoiceSettingRepository:
    @classmethod
    def get_by_user_id(cls, guild_id:int, user_id: int) -> GuildVoiceSettingEntity | None:
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
        voice_setting_model: GuildVoiceSetting = (
            session.query(GuildVoiceSetting).filter_by(guild_id=guild_id,user_id=user_id).first()
        )

        if voice_setting_model == None:
            return None

        return model_to_entity(voice_setting_model, GuildVoiceSettingEntity)

    @classmethod
    def create(cls, voice_setting_entity: GuildVoiceSettingEntity) -> GuildVoiceSettingEntity:
        """作成

        Parameters
        ----------
        voice_setting_entity : VoiceSettingEntity
            作成情報

        Returns
        -------
        VoiceSettingEntity
            作成後の情報
        """
        voice_setting = entity_to_model(voice_setting_entity, GuildVoiceSetting)

        session.add(voice_setting)
        session.commit()
        return cls.get_by_user_id(voice_setting_entity.guild_id, voice_setting_entity.user_id)

    @classmethod
    def update(cls, voice_setting_entity: GuildVoiceSettingEntity) -> GuildVoiceSettingEntity:
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
            guild_id=voice_setting_entity.guild_id,
            user_id=voice_setting_entity.user_id
        ).update(asdict(voice_setting_entity))
        session.commit()

        return cls.get_by_user_id(voice_setting_entity.guild_id, voice_setting_entity.user_id)

    @classmethod
    def delete(cls,guild_id:int,  user_id: int) -> GuildVoiceSettingEntity:
        """削除

        Parameters
        ----------
        guild_id : int
            guild_id
        user_id : int
            user_id

        Returns
        -------
        GuildVoiceSettingEntity
            削除後の情報
        """
        session.query(GuildVoiceSetting).filter_by(guild_id=guild_id,user_id=user_id).delete()
        session.commit()

        return cls.get_by_user_id(user_id)
