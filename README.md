# PolyVoxCord
[![LICENSE](http://img.shields.io/badge/license-MIT-blue.svg?style=flat)](LICENSE)
![Discord bot](https://img.shields.io/static/v1?logo=discord&label=&message=Discord%20bot&labelColor=f5f5f5&color=5865F2&logoColor=5865F2)
![Python3.11.0](https://img.shields.io/static/v1?logo=python&label=&message=Python3.11.0&labelColor=f5f5f5&color=3776AB&logoColor=3776AB)
![SQLite](https://img.shields.io/static/v1?logo=SQLite&label=&message=SQLite&labelColor=f5f5f5&color=003B57&logoColor=003B57)
[![VSCode](https://img.shields.io/static/v1?logo=visualstudiocode&label=&message=Open%20in%20Visual%20Studio%20Code&labelColor=2c2c32&color=007acc&logoColor=007acc)](https://open.vscode.dev/somakai-sumasi/PolyVoxCord)

## これはなに
Discordの読み上げbot
VOICEROID2,VOICEVOX,SofTalkを使用し、音声を作成し、読み上げをしてくれる

## 機能,仕様
- VOICEROID2,VOICEVOX,SofTalkを使用したDiscord上のテキストを読み上げを行う
- txtファイル読み上げ
- ユーザー,サーバー事のボイスモデルを設定
- ユーザー独自のサーバー事の辞書
- サーバー事読み上げ文字数制限
- URLはそのまま読み上げせず置き換える
- MeCabによる単語の読みを推測(お好きなコーパスを指定出来ます。)

## コマンド

| コマンド名                    | 説明                                  |
| ------------------------ | ----------------------------------- |
| help                     | ヘルプコマンド                             |
| read_start               | 読み上げ開始                              |
| read_end                 | 読み上げ終了                              |
| softalk_list             | Softalkの声の一覧を見る                     |
| voiceroid_list           | VOICEROIDの声の一覧を見る                   |
| voicevox_list            | VOICEVOXの声の一覧を見る                    |
| set_softalk              | SofTalkの声を設定する                      |
| set_voiceroid            | VOICEROIDの声を設定する                    |
| set_voicevox             | VOICEVOXの声を設定する                     |
| set_other_user_softalk   | 他のユーザーのSofTalkの声を設定する(管理者権限が必要です)   |
| set_other_user_voiceroid | 他のユーザーのVOICEROIDの声を設定する(管理者権限が必要です) |
| set_other_user_voicevox  | 他のユーザーのVOICEVOXの声を設定する(管理者権限が必要です)  |
| set_limit                | 読み上げ上限数を設定                          |
| add_dict                 | 辞書を追加                               |


## 環境変数
envファイルについて

| 変数名             | 役割                     | デフォルト値         |
| --------------- | ---------------------- | -------------- |
| TOKEN           | Discordのトークン           |                |
| DB_NAME         | SQLiteデータベース名          | PolyVoxCord.db |
| SOFTALK         | SofTalkのインストールパス       |                |
| VOICEVOX_HOST   | VOICEVOXを動かしているホスト     | localhost      |
| VOICEVOX_PORT   | VOICEVOXを動かしているホストのポート | 50021          |
| MECAB_USER_DICT | MeCabのコーパスのパス          |                |

## 初期設定,実行
1. VOICEVOXを起動する
2. `poetry install`を行いpoetryで仮想環境を作成
3. `.env.sample`ファイルを`.env`にリネーム
4. `.env`ファイルのTOKENなどを埋める
5. `poetry shell`で仮想環境に入る
6. `python app/init_db.py`を実行し、dbフォルダにdbファイルが作成される事を確認する
7. `python app/main.py`を実行する

## 動かない時試す事
- VOICEROID2を64bitに上げる
- VOICEVOXを起動する

## 改修時にする事
フォーマッターを実行する
1. `isort .`
2. `black .`
