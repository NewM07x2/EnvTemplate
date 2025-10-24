# Django 開発ガイド（初学者向け）

このドキュメントは、テンプレートプロジェクト `python/Django` 全体を通して、初心者が効率よくコードを追い、  
処理の流れを理解し、デバッグやローカル開発を行えるように作成しました。

目次

- はじめに

- プロジェクト構成の把握

- 開発時の基本作業フロー

- コードの追い方（実践）

- よくある処理の流れ（リクエスト → レスポンス）

- マイグレーションとデータベース

- Docker を使った開発

- Celery / バックグラウンドワーカー

- テストの書き方と実行

- デバッグの基本テクニック

- トラブルシューティングのヒント

- 参考資料

## はじめに

このテンプレートは、Django 5.0 を用いた REST API + GraphQL のハイブリッド構成を採用しています。  
コードはレイヤードアーキテクチャ（models → repositories → services → serializers → views）に分かれており、  
各層の役割を分離して理解することが大切です。

## プロジェクト構成の把握

主なトップレベルディレクトリ:

- `apps/` - 各ドメインアプリ（`users`, `posts` など）。ここがビジネスロジックの本体です。

- `config/` - プロジェクト設定（`settings.py`, `urls.py`, `wsgi.py`, `asgi.py`, `celery.py`）

- `core/` - 共通のユーティリティやヘルスチェック

- `docker/` - Dockerfile 等

- `tests/` - pytest 用テスト

各アプリの典型的な構成（例: `apps/users`）:

- `models.py` - Django モデル定義

- `repositories.py` - DB 操作をまとめた層

- `services.py` - ビジネスロジック

- `serializers.py` - DRF シリアライザー

- `views.py` - ViewSet / API のエンドポイント

- `schema.py` - GraphQL スキーマ


## 開発時の基本作業フロー

1. ブランチを作成する
2. 依存関係をインストール（ローカル）
3. マイグレーションを作る/適用
4. サーバーを起動して動作確認
5. テストを実行
6. PR を作成

## コードの追い方（実践）

以下は API リクエストが来てから DB に保存されるまでを追う具体的な方法です。

1. ルーティングを探す
   - `config/urls.py` と各アプリの `urls.py` を確認してエンドポイント（例: `/api/users/`）の割当を探す。
2. view を開く
   - `apps/<app>/views.py` の ViewSet または APIView を特定。どの serializer、service を使っているかを見る。
3. serializer を確認
   - `serializers.py` で入力バリデーション、create/update の処理が書かれているか確認。
4. service/repository を追う
   - ビジネスロジックは `services.py` にあり、DB 操作は `repositories.py` に集約されていることが多い。
5. model を確認
   - `models.py` を見て DB のカラムやリレーションを把握する。
6. 実行時のログを参照
   - サーバーの標準出力や `docker-compose logs` を見て、SQL や例外のスタックトレースを追う。

Tips:

- まずユニットテストを読むとその機能の期待仕様がわかりやすい。

- `grep` / VSCode の「参照」機能で関数名やクラス名を横断検索する。


## よくある処理の流れ（例: ユーザー作成 API）

1. `POST /api/users/` が来る
2. `apps/users/views.py` の `UserViewSet.create`（または generic ViewSet の `create`）が呼ばれる
3. `serializers.UserSerializer` でデータ検証
4. `services.UserService.create_user(...)` が呼ばれ、必要であれば `repositories.UserRepository` が DB に保存
5. レスポンスを返す


## マイグレーションとデータベース

- マイグレーションファイルは `apps/<app>/migrations/` にあります。
- 開発では `python manage.py makemigrations` と `python manage.py migrate` を使います。
- Docker 環境では `docker-compose exec app python manage.py migrate` を実行します。
- 問題があれば、`docker-compose down -v` でボリュームを消してクリーンに再構築できます（データは失われます）。


## Docker を使った開発

- `docker-compose up -d --build` で起動。
- `docker-compose logs -f app` でログを追う。
- 依存サービス（Postgres, Redis）は `docker-compose.yml` で定義されています。
- entrypoint がマイグレーションを行う設定になっている場合、環境変数 `AUTO_MIGRATE=false` で無効化できます。


## Celery / バックグラウンドワーカー

- Celery は `config/celery.py` で定義されています。
- ワーカー起動: `celery -A config worker -l info`（Docker: `docker-compose exec celery_worker celery -A config worker -l info`）
- ビート起動: `celery -A config beat -l info`（スケジューラ）
- Celery が起動しない場合は、`config.celery`（ファイル）と `CELERY_BROKER_URL` が正しく設定されているか確認。


## テストの書き方と実行

- pytest を使用しています。
- すべてのテストを実行する: `pytest`
- Docker 内で実行: `docker-compose exec app pytest`
- テスト時は DB の状態を fixture で制御する（`tests/conftest.py` を参照）。


## デバッグの基本テクニック

1. ログを読む
   - Django のエラースタックトレースは詳細を示します。`docker-compose logs -f app` で確認。
2. ローカルで落ちる箇所を再現
   - 該当のリクエストを curl/Postman で作成し、エラーメッセージとスタックトレースを取得する。
3. print / logging を一時的に入れる
   - 小さいプロジェクトでは `print()` で確認することも OK。ただし本番では `logging` を使う。
4. Django shell を使う
   - `docker-compose exec app python manage.py shell` でモデルやサービスの動作を対話的に確認。
5. breakpoints (VSCode と debugpy)
   - `pip install debugpy` して、`python -m debugpy --listen 0.0.0.0:5678 --wait-for-client manage.py runserver` のように起動してデバッガからアタッチ。


## トラブルシューティングのヒント

- マイグレーションの競合: 複数コンテナが同時に migrate を実行している場合は、`AUTO_MIGRATE=false` にして一つのジョブで migrate を行う。
- Celery が起動しない: `config.celery` の存在、`CELERY_BROKER_URL`（redis）を確認。ログの `Module 'config' has no attribute 'celery'` は `config/__init__.py` に `from .celery import app as celery_app` を追加すれば解決。
- 静的ファイルの警告: `STATICFILES_DIRS` を確認し、`static/` ディレクトリを作成。


## 参考資料

- Django 公式ドキュメント: [https://docs.djangoproject.com/](https://docs.djangoproject.com/)

- Django REST framework: [https://www.django-rest-framework.org/](https://www.django-rest-framework.org/)

- Celery 公式: [https://docs.celeryq.dev/](https://docs.celeryq.dev/)


---

このドキュメントは初学者がプロジェクトを読み、素早く動かせることを目的にしています。必要であれば追加で『API 開発ガイド』や『テストガイド』等の分割したドキュメントも作成します。
