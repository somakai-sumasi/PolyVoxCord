import asyncio
import platform

import discord
from config.voice import OPUS_PATH
from discord.ext import commands
from service.presence_service import PresenceService


class BaseBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()
        super().__init__(command_prefix="!", intents=intents, help_command=None)

        self.async_event_handlers = {}
        self.queue_map: dict[
            int, asyncio.Queue[tuple[int, asyncio.Future[list[str]]]]
        ] = {}
        self.text_channel_list: dict[int, list[int]] = {}

    def get_cogs(self) -> list[str]:
        """読み込むcogのリストを返す

        Returns
        -------
        list[str]
            読み込むcogのリスト
        """
        return [
            "cogs.guide",
            "cogs.ops",
            "cogs.read",
            "cogs.connection",
            "cogs.user_setting",
            "cogs.guild_setting",
            "cogs.task",
        ]

    async def setup_hook(self):
        for cog in self.get_cogs():
            await self.load_extension(cog)

    async def on_ready(self):
        print(f"Logged in as {self.user} (ID: {self.user.id})")

        # Windows以外のプラットフォームでは、Opusライブラリをロード
        if platform.system() != "Windows":
            discord.opus.load_opus(OPUS_PATH)

        await PresenceService.set_presence(self)

    def add_text_channel(self, guild_id: int, channel_id: int):
        """指定されたguild_idにchannel_idを追加する。

        Parameters
        ----------
        guild_id : int
            ギルドid
        channel_id : int
            チャンネルid
        """

        if guild_id not in self.text_channel_list:
            self.text_channel_list[guild_id] = []

        if channel_id not in self.text_channel_list[guild_id]:
            self.text_channel_list[guild_id].append(channel_id)

    def has_channel(self, guild_id: int, channel_id: int) -> bool:
        """指定されたguild_idにchannel_idが存在するかを確認する。

        Parameters
        ----------
        guild_id : int
            ギルドid
        channel_id : int
            チャンネルid

        Returns
        -------
        bool
            存在する場合True
        """
        return (
            guild_id in self.text_channel_list
            and channel_id in self.text_channel_list[guild_id]
        )

    def remove_guild(self, guild_id: int) -> None:
        """指定されたguild_id（と紐づくchannel_id）を削除する。

        Parameters
        ----------
        guild_id : int
            ギルドid
        """
        if guild_id in self.text_channel_list:
            del self.text_channel_list[guild_id]

        # キューも削除してメモリリークを防ぐ
        if guild_id in self.queue_map:
            # キュー内の残りのFutureをキャンセル
            queue = self.queue_map[guild_id]
            while not queue.empty():
                try:
                    _, future = queue.get_nowait()
                    if not future.done():
                        future.cancel()
                except asyncio.QueueEmpty:
                    break

            del self.queue_map[guild_id]

    async def add_to_read_queue(
        self, guild_id: int, message_id: int, voice_future: asyncio.Future[list[str]]
    ):
        """読み上げキューにメッセージを追加して処理する

        Parameters
        ----------
        guild_id : int
            ギルドID
        message_id : int
            メッセージID
        voice_future : asyncio.Future
            音声ファイルパスのFuture
        """
        # ギルドごとのキューが存在しない場合は作成
        if guild_id not in self.queue_map:
            self.queue_map[guild_id] = asyncio.Queue()

        # メッセージIDとFutureをキューに追加
        await self.queue_map[guild_id].put((message_id, voice_future))

        # キューから取り出して処理
        while True:
            next_message_id, next_future = await self.queue_map[guild_id].get()
            if next_message_id == message_id:
                # 自分の番の場合、音声ファイルの作成を待機して再生
                try:
                    paths = await asyncio.wait_for(next_future, timeout=30.0)
                    guild = self.get_guild(guild_id)
                    if guild and guild.voice_client and paths:
                        for path in paths:
                            await self.play_audio(guild.voice_client, path)
                except asyncio.TimeoutError:
                    print(f"Voice generation timeout for message {message_id}")
                    if not next_future.done():
                        next_future.cancel()
                except asyncio.CancelledError:
                    print(f"Voice generation cancelled for message {message_id}")
                except Exception as e:
                    print(f"Error processing voice for message {message_id}: {e}")
                break
            else:
                # 自分の番でない場合、キューを戻す
                await self.queue_map[guild_id].put((next_message_id, next_future))

    async def play_audio(self, voice_client: discord.VoiceClient, path: str):
        """音声を再生する

        Parameters
        ----------
        voice_client : discord.VoiceClient
            音声クライアント
        path : str
            音声ファイルパス
        """
        try:
            while voice_client.is_playing():
                await asyncio.sleep(0.5)

            voice_client.stop()
            voice_client.play(discord.FFmpegPCMAudio(path))
        except Exception as e:
            print(f"Error in play_audio: {e}")


bot = BaseBot()
