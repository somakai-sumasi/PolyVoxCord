from dotenv import load_dotenv
import sqlite3
import os

load_dotenv()
DB_NAME = os.getenv("DB_NAME")
conn = sqlite3.connect("./DB/" + DB_NAME)

cur = conn.cursor()

# 音声設定
cur.execute(
    """
    CREATE TABLE voice_setting(
        user_id INTEGER PRIMARY KEY ,
        voice_type TEXT ,
        voice_name_key TEXT,
        speed REAL,
        pitch REAL
    )
"""
)

# 読み上げ上限
cur.execute(
    """
    CREATE TABLE read_limit(
        guild_id INTEGER PRIMARY KEY ,
        upper_limit INTEGER 
    )
"""
)

# 辞書
cur.execute(
    """
    CREATE TABLE reading_dict(
        id INTEGER PRIMARY KEY ,
        guild_id INTEGER  ,
        character TEXT ,
        reading TEXT
    )
"""
)

conn.close()
