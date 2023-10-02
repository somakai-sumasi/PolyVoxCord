import discord
from discord.ext import commands


class PresenceService:
    @classmethod
    async def set_presence(cls, bot: commands.Bot):
        await bot.change_presence(
            activity=discord.Game(
                name=f"{len(bot.guilds)}サーバー | {len(bot.voice_clients)}ボイスチャンネル | {len(bot.users)}ユーザー"
            )
        )
