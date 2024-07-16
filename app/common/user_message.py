from enum import IntEnum

# import discord


class MessageType(IntEnum):
    INFO = 0xAAAAAA
    SUCCESS = 0x00CF00
    NOTICE = 0x005FAF
    WARNING = 0xFFCF00
    ERROR = 0xAF0000


# class UserMessage:
#     def embed(message_type: MessageType = MessageType.INFO):
#         return discord.Embed(
#             title="Hi!!", description="I got a color!", color=message_type
#         )
