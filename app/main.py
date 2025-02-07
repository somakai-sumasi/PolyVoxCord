import logging

from base.bot import BaseBot
from config.discord import TOKEN

bot = BaseBot()
handler = logging.FileHandler(filename="./logs/discord.log", encoding="utf-8", mode="a")
bot.run(TOKEN, log_handler=handler)
