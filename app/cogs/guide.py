import discord
from discord import app_commands
from discord.ext import commands
from voice_model.softalk import Softalk
from voice_model.voiceroid import Voiceroid
from voice_model.voicevox import Voicevox


class Guide(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("loaded :" + self.__class__.__name__)
        await self.bot.tree.sync(guild=None)
        print("sync:" + self.__class__.__name__)

    @app_commands.command(name="softalk_list", description="Softalkの声の一覧を見る")
    async def softalk_list(self, interaction: discord.Interaction):
        """Softalkの声の一覧を見る

        Parameters
        ----------
        interaction : discord.Interaction
            discord.Interaction
        """
        await interaction.response.defer()

        list = Softalk.voice_list()
        text = ""
        for key, val in list.items():
            text += f"`{key}`   {val}\n"
        embed = discord.Embed(title="Softalkの声の一覧", description=text)
        await interaction.followup.send(embed=embed, ephemeral=False)

    @app_commands.command(name="voiceroid_list", description="VOICEROIDの声の一覧を見る")
    async def voiceroid_list(self, interaction: discord.Interaction):
        """VOICEROIDの声の一覧を見る

        Parameters
        ----------
        interaction : discord.Interaction
            discord.Interaction
        """
        await interaction.response.defer()

        list = Voiceroid.voice_list()
        text = ""
        for key, val in list.items():
            text += f"`{key}`   {val}\n"
        embed = discord.Embed(title="VOICEROIDの声の一覧", description=text)
        await interaction.followup.send(embed=embed, ephemeral=False)

    @app_commands.command(name="voicevox_list", description="VOICEVOXの声の一覧を見る")
    async def voicevox_list(self, interaction: discord.Interaction):
        """VOICEVOXの声の一覧を見る

        Parameters
        ----------
        interaction : discord.Interaction
            discord.Interaction
        """
        await interaction.response.defer()

        list = Voicevox.voice_list()
        text = ""
        for key, val in list.items():
            text += f"`{key}`   {val}\n"
        embed = discord.Embed(title="VOICEVOXの声の一覧", description=text)
        await interaction.followup.send(embed=embed, ephemeral=False)


async def setup(bot: commands.Bot):
    await bot.add_cog(Guide(bot))
