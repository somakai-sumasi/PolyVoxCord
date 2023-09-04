import discord


class read_service:
    VOICE_TYPE = ["VOICEROID", "VOICEVOX", "SofTalk"]

    # 音声データ作成
    def read(message: discord.Message):
        # メッセージの送信者がbotだった場合は無視
        if message.author.bot:
            return
        # メッセージの送信したサーバーのボイスチャンネルに切断していない場合は無視
        if message.guild.voice_client is None:
            return

        # ユーザー情報を取得
        user_id = message.author.id

        # ユーザーからボイス設定を取得

        # ボイス設定から実際の音声モデルを作成する

        # 音声ファイルのパスを返す

    def read_txt():
        ...

    def read_file():
        ...
