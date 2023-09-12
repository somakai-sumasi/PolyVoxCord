# main.py

from data_model.database import engine, Session, Base  # database.pyからengineとSessionをインポート
from data_model.test import User  # models.pyからUserをインポート

# セッションを作成
session = Session()

users = session.query(User).all()

print(users)
for user in users:
    print(user.id)