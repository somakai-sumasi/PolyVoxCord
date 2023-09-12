# models.py

from sqlalchemy import Column, Integer, String
from data_model.database import Base  # database.pyからBaseをインポート

# Userテーブル（モデル）を定義
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
