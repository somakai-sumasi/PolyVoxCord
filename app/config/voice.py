"""音声関連の設定"""
import os

# 音声エンジン設定
SOFTALK = str(os.getenv("SOFTALK"))
VOICEVOX_HOST = os.getenv("VOICEVOX_HOST")
VOICEVOX_PORT = os.getenv("VOICEVOX_PORT")

# 音声ファイル出力設定
BASE_DIR = os.getcwd()
VOICE_OUTPUT_DIR = os.path.join(BASE_DIR, "tmp", "wav")

# Opusライブラリのパス
OPUS_PATH = os.getenv("OPUS_PATH")
