import discord
from discord import app_commands
from discord.ext import commands
from service.guide_service import GuideService


class Guide(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: commands.Bot = bot

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
        await GuideService.softalk_list(interaction)

    @app_commands.command(name="voiceroid_list", description="VOICEROIDの声の一覧を見る")
    async def voiceroid_list(self, interaction: discord.Interaction):
        """VOICEROIDの声の一覧を見る

        Parameters
        ----------
        interaction : discord.Interaction
            discord.Interaction
        """
        await GuideService.voiceroid_list(interaction)

    @app_commands.command(name="voicevox_list", description="VOICEVOXの声の一覧を見る")
    async def voicevox_list(self, interaction: discord.Interaction):
        """VOICEVOXの声の一覧を見る

        Parameters
        ----------
        interaction : discord.Interaction
            discord.Interaction
        """
        await GuideService.voicevox_list(interaction)


async def setup(bot: commands.Bot):
    await bot.add_cog(Guide(bot))
