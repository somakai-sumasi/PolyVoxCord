import discord
from cogs.base_cog import BaseCog
from common.user_message import MessageType
from config.discord import MANAGEMENT_GUILD_ID
from discord.ext import commands
from voice_model.softalk import Softalk
from voice_model.voiceroid import Voiceroid
from voice_model.voicevox import Voicevox


class GuideService:
    @classmethod
    async def help(cls, bot: commands.Bot, interaction: discord.Interaction):
        """_summary_

        Parameters
        ----------
        bot : commands.Bot
            discord.ext.commands.Bot
        interaction : discord.Interaction
            discord.Interaction
        """

        await interaction.response.defer()

        is_management_guild = interaction.guild_id == MANAGEMENT_GUILD_ID

        commands = {}
        for cmd in bot.tree.walk_commands():
            commands[cmd.name] = cmd.description

        cogs = bot.cogs
        for _, cog in cogs.items():
            cog: BaseCog
            if cog.is_ops and not is_management_guild:
                continue

            for cmd in cog.walk_app_commands():
                commands[cmd.name] = cmd.description

        embed = discord.Embed(
            title="コマンド一覧",
            color=MessageType.INFO,
        )
        for name, description in commands.items():
            embed.add_field(name=name, value=description, inline=False)

        await interaction.followup.send(
            embed=embed,
            ephemeral=False,
        )

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

        await interaction.followup.send(
            embed=discord.Embed(
                title="Softalkの声の一覧", description=text, color=MessageType.INFO
            ),
            ephemeral=False,
        )

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

        await interaction.followup.send(
            embed=discord.Embed(
                title="VOICEROIDの声の一覧", description=text, color=MessageType.INFO
            ),
            ephemeral=False,
        )

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

        await interaction.followup.send(
            embed=discord.Embed(
                title="VOICEVOXの声の一覧", description=text, color=MessageType.INFO
            ),
            ephemeral=False,
        )
