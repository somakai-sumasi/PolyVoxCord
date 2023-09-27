# PolyVoxCord

## 初期設定,実行
1. `poetry install`を行いpoetryで仮想環境を作成
2. `.env.sample`ファイルを`.env`にリネーム
3. `.env`ファイルのTOKENなどを埋める
4. `python app/init.py`を実行し、dbフォルダにdbファイルが作成される事を確認する

## 実行方法
`python app/main.py`を実行し、dbフォルダにdbファイルが作成される事を確認する

## 動かない時試す事
- VOICEROIDを64bitに上げる

## 改修時にする事
フォーマッターを実行する
1. `isort .`
2. `black .`
