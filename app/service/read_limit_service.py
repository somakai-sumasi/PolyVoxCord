import discord
from common.user_message import MessageType
from entity.read_limit_entity import ReadLimitEntity
from repository.read_limit_repository import ReadLimitRepository


class ReadLimitService:
    @classmethod
    async def set_limit(
        cls, interaction: discord.Interaction, guild_id: int, upper_limit: int
    ) -> None:
        """_summary_

        Parameters
        ----------
        interaction : discord.Interaction
           discord.Interaction
        guild_id : int
            guild_id
        upper_limit : int
            読上げ上限文字数
        """

        await interaction.response.defer()

        read_limit = ReadLimitRepository.get_by_guild_id(guild_id)
        if read_limit is None:
            read_limit = ReadLimitEntity(guild_id=guild_id, upper_limit=upper_limit)
            ReadLimitRepository.create(read_limit)
        else:
            read_limit.upper_limit = upper_limit
            ReadLimitRepository.update(read_limit)

        await interaction.followup.send(
            embed=discord.Embed(
                title=f"読み上げ上限を{upper_limit}文字に変更しました", color=MessageType.SUCCESS
            ),
            ephemeral=False,
        )
