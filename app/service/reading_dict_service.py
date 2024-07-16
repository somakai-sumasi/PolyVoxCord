import discord
from common.user_message import MessageType
from entity.reading_dict_entity import ReadingDictEntity
from repository.reading_dict_repository import ReadingDictRepository


class ReadingDictService:
    @classmethod
    async def add_dict(
        cls,
        interaction: discord.Interaction,
        guild_id: int,
        character: str,
        reading: str,
    ) -> None:
        """辞書に読み書きを追加する

        Parameters
        ----------
        interaction : discord.Interaction
            discord.Interaction
        guild_id : int
            guild_id
        character : str
            書き
        reading : str
            読みかた
        """
        await interaction.response.defer()

        reading_dict = ReadingDictRepository.get_by_character(
            guild_id, character=character
        )
        if reading_dict is None:
            reading_dict = ReadingDictEntity(
                id=None, guild_id=guild_id, character=character, reading=reading
            )
            ReadingDictRepository.create(reading_dict)
        else:
            reading_dict.reading = reading
            ReadingDictRepository.update(reading_dict)

        await interaction.followup.send(
            embed=discord.Embed(
                title="辞書に読みを追加しました",
                description=f"書き: {character} => {reading}",
                color=MessageType.SUCCESS,
            ),
            ephemeral=False,
        )

    @classmethod
    async def del_dict(
        cls, interaction: discord.Interaction, guild_id: int, character: str
    ) -> None:
        """辞書に書きを削除

        Parameters
        ----------
        interaction : discord.Interaction
            discord.Interaction
        guild_id : int
            guild_id
        character : str
            書き
        """
        await interaction.response.defer()

        reading_dict = ReadingDictRepository.get_by_character(
            guild_id, character=character
        )

        if reading_dict is None:
            await interaction.followup.send(
                embed=discord.Embed(
                    title="辞書に登録されていません",
                    description=f"{character}",
                    color=MessageType.WARNING,
                ),
                ephemeral=False,
            )
            return

        ReadingDictRepository.delete(reading_dict.id)

        await interaction.followup.send(
            embed=discord.Embed(
                title="辞書から読みを削除しました",
                description=f"{character}",
                color=MessageType.SUCCESS,
            ),
            ephemeral=False,
        )
