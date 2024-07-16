import discord
from voice_model.softalk import Softalk
from voice_model.voiceroid import Voiceroid
from voice_model.voicevox import Voicevox
from common.user_message import MessageType


class GuideService:
    @classmethod
    async def softalk_list(cls, interaction: discord.Interaction):
        """Softalkの声の一覧を見る

        Parameters
        ----------
        interaction : discord.Interaction
            discord.Interaction
        """
        await interaction.response.defer()

        list = Softalk.voice_list()
        text = ""

        for index, voice in enumerate(list):
            text += f"`{index}`   {voice['name']}\n"
        embed = discord.Embed(
            title="Softalkの声の一覧", description=text, color=MessageType.INFO
        )
        await interaction.followup.send(embed=embed, ephemeral=False)

    @classmethod
    async def voiceroid_list(cls, interaction: discord.Interaction):
        """VOICEROIDの声の一覧を見る

        Parameters
        ----------
        interaction : discord.Interaction
            discord.Interaction
        """
        await interaction.response.defer()

        list = Voiceroid.voice_list()
        text = ""

        for index, voice in enumerate(list):
            text += f"`{index}`   {voice['name']}\n"
        embed = discord.Embed(
            title="VOICEROIDの声の一覧", description=text, color=MessageType.INFO
        )
        await interaction.followup.send(embed=embed, ephemeral=False)

    @classmethod
    async def voicevox_list(cls, interaction: discord.Interaction):
        """VOICEVOXの声の一覧を見る

        Parameters
        ----------
        interaction : discord.Interaction
            discord.Interaction
        """
        await interaction.response.defer()

        list = Voicevox.voice_list()
        text = ""

        for index, voice in enumerate(list):
            text += f"`{index}`   {voice['name']}\n"
        embed = discord.Embed(
            title="VOICEVOXの声の一覧", description=text, color=MessageType.INFO
        )
        await interaction.followup.send(embed=embed, ephemeral=False)
