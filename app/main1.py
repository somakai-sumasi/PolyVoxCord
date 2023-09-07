from dotenv import load_dotenv
import sqlite3

load_dotenv()
# TEST.dbを作成する
# すでに存在していれば、それにアスセスする。
dbname = "DB/TEST.db"
conn = sqlite3.connect(dbname)

# データベースへのコネクションを閉じる。(必須)
conn.close()
