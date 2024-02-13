# PolyVoxCord
[![MIT License](http://img.shields.io/badge/license-MIT-blue.svg?style=flat)](LICENSE)
[![Open in Visual Studio Code](https://img.shields.io/static/v1?logo=visualstudiocode&label=&message=Open%20in%20Visual%20Studio%20Code&labelColor=2c2c32&color=007acc&logoColor=007acc)](https://open.vscode.dev/somakai-sumasi/PolyVoxCord)

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

## 初期設定,実行
1. `poetry install`を行いpoetryで仮想環境を作成
2. `.env.sample`ファイルを`.env`にリネーム
3. `.env`ファイルのTOKENなどを埋める
4. `python app/init.py`を実行し、dbフォルダにdbファイルが作成される事を確認する

## 実行方法
1. `poetry shell`で仮想環境に入る
2. `python app/main.py`を実行する

## 動かない時試す事
- VOICEROID2を64bitに上げる
- VOICEVOXを起動する

## 改修時にする事
フォーマッターを実行する
1. `isort .`
2. `black .`
