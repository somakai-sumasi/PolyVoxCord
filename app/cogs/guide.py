import os
import discord
from discord import app_commands
from discord.ext import commands
from voice_model.voicevox import Voicevox

GUILD = int(os.getenv("GUILD"))


class Guide(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("loaded :" + self.__class__.__name__)
        await self.bot.tree.sync(guild=discord.Object(GUILD))
        print("sync:" + self.__class__.__name__)

    @app_commands.command(name="voicevox_list", description="VOICEVOXの声の一覧を見る")
    @app_commands.guilds(GUILD)
    async def voicevox_list(self, interaction: discord.Interaction):
        """VOICEVOXの声の一覧を見る"""

        list = Voicevox.voice_list()
        text = ""
        for key, val in list.items():
            text += f"`{key}`   {val}\n"
        embed = discord.Embed(title="VOICEVOXの声の一覧", description=text)
        await interaction.response.send_message(embed=embed, ephemeral=False)


async def setup(bot: commands.Bot):
    await bot.add_cog(Guide(bot))
