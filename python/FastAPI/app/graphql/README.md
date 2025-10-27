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

## 注意事項
- スキーマ設計のベストプラクティスに従ってください。
- リゾルバがエラーを適切に処理することを確認してください。