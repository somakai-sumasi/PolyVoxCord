# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## プロジェクト概要
PolyVoxCordは、複数の日本語TTS（テキスト読み上げ）エンジン（VOICEROID2、VOICEVOX、SofTalk）をサポートするDiscordボットです。

## 開発コマンド

### セットアップ
```bash
# 依存関係のインストール
poetry install

# 仮想環境の有効化
poetry shell

# データベースの初期化
python app/init_db.py

# ボットの実行
python app/main.py
```

### コード品質管理
```bash
# インポートの整形
isort .

# コードの整形
black .

# Lintの実行
flake8
```

## アーキテクチャ概要

レイヤードアーキテクチャを採用：

1. **Botレイヤー** (`app/base/bot.py`): discord.pyのcommands.Botを拡張したコアクラス
   - ギルドごとの読み上げキューを管理（メッセージ順序を保証）
   - ボイスチャンネル接続と音声再生を制御
   - 切断時のリソースクリーンアップを実装
2. **Cogs** (`app/cogs/`): Discordスラッシュコマンドを実装するコマンドグループ
   - 各cogは機能ドメインを表現（read、connection、settingsなど）
3. **サービスレイヤー** (`app/service/`): ビジネスロジックとオーケストレーション
   - 複雑な処理を実行し、リポジトリ間を調整
   - `read_service.py`: Future基盤の非同期音声ファイル作成を管理
4. **リポジトリレイヤー** (`app/repository/`): SQLAlchemyを使用したデータベースアクセス
   - 各リポジトリは特定エンティティのCRUD操作を担当
5. **音声モデル** (`app/voice_model/`): TTSエンジンの統合
   - 各音声モデルは異なるTTSエンジン用の基本インターフェースを実装

## 主要な実装パターン

### 新規コマンドの追加
新しいコマンドは適切なcogクラスに`@discord.app_commands.command()`デコレータを使用してメソッドとして追加します。

### データベース操作
- すべてのデータベース操作にはリポジトリクラスを使用
- セッションはサービスレイヤーでコンテキストマネージャーを通じて管理
- モデルは`app/model/`でSQLAlchemy declarative baseを使用して定義

### 音声処理フロー
1. メッセージ受信 → Futureと共に即座にキューイング（`read_service.py`）
2. 非同期音声作成:
   - テキスト入力 → 辞書置換（`reading_dict_service.py`）
   - テキスト処理 → 必要に応じてMeCab解析
   - 音声生成 → 選択されたTTSエンジン（`voice_model/`）
3. キュー処理 → メッセージIDに基づいて順番待ち
4. 音声出力 → 適切な順序でDiscordボイスチャンネルに出力

### キュー管理パターン
- `asyncio.Queue[tuple[int, asyncio.Future[list[str]]]]`を使用したギルドごとのキュー
- メッセージIDチェックによるメッセージ順序の保証
- 順番外のメッセージは再キューイングして順序を維持
- ギルド切断時のFutureキャンセルを含む適切なクリーンアップ

### エラーハンドリング
- サービスレイヤーのメソッドはResultオブジェクトを返すか特定の例外を発生
- Cogsは例外を処理し、適切なDiscord埋め込みレスポンスを送信
- 一貫したエラーフォーマットのために`ErrorContext`を使用
- 音声生成は適切なFuture処理を伴う30秒のタイムアウト

## 環境設定
必要な環境変数（.envファイル）:
- `TOKEN`: Discordボットトークン
- `DB_NAME`: データベースファイル名（デフォルト: PolyVoxCord.db）
- `SOFTALK_PATH`: SofTalk実行ファイルへのパス
- `VOICEVOX_HOST`: VOICEVOX APIホスト
- `VOICEVOX_PORT`: VOICEVOX APIポート
- `USER_DICT_CSV_PATH`: MeCabユーザー辞書へのパス

## 重要な考慮事項
- すべてのテキスト処理は日本語入力を前提
- 音声モデルには異なる利用可能性と要件がある
- 接続管理はギルドごとの音声接続を追跡
- ユーザー設定はサーバー間で永続化
- ギルド設定はサーバー固有
- 音声ファイル作成はFutureベースの非同期パターンでノンブロッキング
- 非同期音声生成でもメッセージ順序は厳密に保持