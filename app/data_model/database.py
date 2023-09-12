# database.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()
# Base クラスの生成
Base = declarative_base()
DB_NAME = os.getenv("DB_NAME")
# データベースエンジンを作成
engine = create_engine('sqlite:///./db/'+ DB_NAME, echo=False)

# セッションファクトリを作成
Session = sessionmaker(bind=engine)
