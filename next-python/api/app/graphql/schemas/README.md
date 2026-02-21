# schemas ディレクトリの役割と構成

このディレクトリは、GraphQL の型やスキーマ定義をドメインごとに整理・管理するための場所です。

## 目的

- 各ドメイン（例：post, user, sample）ごとに GraphQL の型やリゾルバ、スキーマ定義を分割・整理し、可読性・保守性を高める。

## 主なファイル

- `post_schema.py`：Post（記事）に関する GraphQL 型やクエリ・ミューテーションを定義
- `user_schema.py`：User（ユーザー）に関する GraphQL 型やクエリ・ミューテーションを定義
- `sample_schema.py`：サンプル用の型やクエリ・ミューテーションを定義
- `schema.py`：各スキーマ（post, user, sample など）を統合し、アプリ全体の GraphQL スキーマ（`graphql_schema`）としてエクスポートする役割

## 使い方のイメージ

1. 各スキーマファイル（例：`post_schema.py`）で型やリゾルバを定義
2. `schema.py`でそれらをまとめて、FastAPI の GraphQL エンドポイントに渡すスキーマを生成
3. `main.py`や`__init__.py`からは `from app.graphql.schemas.schema import graphql_schema` のようにインポートして利用

## 追加・更新の方法と注意点

- **新しいドメインや型を追加する場合**
  - 例：`comment_schema.py`のように新規ファイルを作成し、型やリゾルバを定義します。
  - `schema.py`で新しいスキーマをインポートし、統合してください。
- **既存スキーマの更新時の注意点**
  - 型やフィールド名を変更する場合、フロントエンドや他のAPI利用者への影響を考慮してください。
  - 依存関係のある他ファイルの修正やテストの追加も忘れずに行いましょう。
- **不要になったスキーマの削除**
  - `schema.py`からのインポート・統合も削除し、関連するテストやドキュメントも整理してください。
- **バージョン管理**
  - スキーマの大きな変更時は、Gitのブランチを切って作業し、レビュー・テストを経てマージするのが安全です。

## 使用している主なライブラリ

- [Strawberry GraphQL](https://strawberry.rocks/)：Python製の型安全なGraphQLサーバーライブラリ。FastAPIと連携してGraphQLエンドポイントを構築。
- [Graphene](https://graphene-python.org/)：Python用のGraphQLライブラリ。主にサンプルや比較用として利用可能。
- [FastAPI](https://fastapi.tiangolo.com/)：Pythonの高速Web APIフレームワーク。GraphQLエンドポイントのルーティングやAPI全体の管理に使用。

## GraphQLスキーマの使い分けについて

- `graphene_schema`：Graphene（別のGraphQLライブラリ）用のスキーマです。  
GrapheneはDjangoなど他のPythonフレームワークとも親和性が高く、従来型のGraphQL実装や比較・サンプル用途で利用できます。
    - **用途例**：GrapheneのAPIやツールと連携したい場合、既存のGraphene資産を活用したい場合。
    - **使用するケース**：
        - 既存のGrapheneベースのプロジェクトやDjangoプロジェクトから移行・統合する場合
        - Graphene特有の機能やエコシステム（Django連携、Relay対応など）を活用したい場合
        - Strawberryとの比較検証や、GraphQL実装の学習・サンプル用途
    - **注意点**：本プロジェクトでは主にサンプル・比較用として保持しており、API本番運用ではStrawberryを推奨しています。

- `strawberry_schema`/`graphql_schema`：Strawberry用（FastAPIで主に利用）  
    - **用途例**：FastAPIと組み合わせて型安全なGraphQL APIを構築したい場合。
    - **特徴**：Pythonの型ヒントを活かした宣言的なスキーマ定義ができ、開発体験や保守性が高いです。
    - **推奨**：**本プロジェクトではStrawberry（`graphql_schema`）を基本として使用します。FastAPIでGraphQLエンドポイントを提供する場合は`graphql_schema`（=Strawberryスキーマ）を利用してください。**

---

何か追加で知りたい点や、具体的な設計例が必要であればご相談ください。
