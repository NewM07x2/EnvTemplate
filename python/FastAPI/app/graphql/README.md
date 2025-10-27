# GraphQL フォルダ

## 目的
このフォルダには、アプリケーションの GraphQL スキーマ、リゾルバ、および関連するロジックが含まれています。

## 使用方法
- GraphQL スキーマを `schema.py` に定義します。
- 特定のクエリやミューテーションのリゾルバ関数を個別のファイルに実装します。

## コードサンプル
```python
from graphene import ObjectType, String, Schema

class Query(ObjectType):
    hello = String(description="シンプルな GraphQL クエリ")

    def resolve_hello(root, info):
        return "こんにちは、GraphQL！"

schema = Schema(query=Query)
```

## コードの追い方
1. `schema.py` から始めて、GraphQL API の構造を理解します。
2. 特定のクエリやミューテーションの実装についてはリゾルバファイルを確認します。

## フォルダ構成

以下は、このフォルダ内の主なファイルとディレクトリの説明です。

- `schema/`
  - GraphQL スキーマを機能ごとに分割して管理するフォルダ。
  - `strawberry_schema.py`: Strawberry を使用したスキーマ定義。
  - `graphene_schema.py`: Graphene を使用したスキーマ定義。

- `resolvers/`
  - GraphQL のリゾルバを機能ごとに分割して管理するフォルダ。
  - `post/`: 投稿に関連するクエリとミューテーション。
  - `sample/`: サンプルデータに関連するクエリとミューテーション。
  - `user/`: ユーザーに関連するクエリとミューテーション。

- `types.py`
  - GraphQL の型定義を含むファイル。
  - 例: `User` 型や `Post` 型。

- `sample_schema.py`
  - Graphene を使用した簡易的なサンプルスキーマ。

- `schema.py`
  - 旧スキーマ定義ファイル。現在は `schema/` フォルダに分割されています。

## 注意事項

- 各スキーマやリゾルバは、機能ごとに適切に分割されています。
- 必要に応じて新しいスキーマやリゾルバを追加する際は、既存の構造に従ってください。
- `types.py` に新しい型を追加する場合は、関連するリゾルバやスキーマも更新してください。