# リポジトリ層に関するドキュメント

## 概要

リポジトリ層は、データベース操作を抽象化し、サービス層や他のアプリケーションロジックから直接的なデータベース操作を分離する役割を担います。
これにより、コードの再利用性が向上し、テストが容易になります。

---

## 目的

- **データアクセスの抽象化**: データベース操作をリポジトリ層に集約し、他の層から直接的なデータベース操作を排除します。

- **コードの再利用性向上**: 共通のデータ操作ロジックをリポジトリ層に集約することで、コードの重複を削減します。

- **テストの容易化**: データベース操作をモック化しやすくすることで、ユニットテストの実施を容易にします。

- **役割分担の明確化**: 他の層（サービス層、ビュー層）との責務を分離し、コードの可読性を向上させます。

---

## 使用用途

1. **データの取得**

   - すべてのデータを取得するメソッド。
   - 特定の条件に基づいてデータをフィルタリングするメソッド。

2. **データの作成**

   - 新しいデータをデータベースに挿入するメソッド。

3. **データの更新**

   - 既存のデータを更新するメソッド。

4. **データの削除**

   - 特定のデータを削除するメソッド。

5. **カスタムクエリ**

   - 特定のビジネスロジックに基づいたカスタムクエリを実行するメソッド。

---

## 実施すべき内容

1. **リポジトリクラスの設計**

   - 各モデルに対応するリポジトリクラスを作成します。
   - 例: `CategoryRepository`, `SampleRepository`。

2. **静的メソッドの活用**

   - インスタンス化を必要としないメソッドには `@staticmethod` を使用します。

3. **トランザクション管理**

   - 複数のデータベース操作が必要な場合は、`@transaction.atomic` を使用してトランザクションを管理します。

4. **キャッシュの活用**

   - 計算コストの高いプロパティには `@cached_property` を使用します。

5. **エラーハンドリング**

   - データが存在しない場合やクエリが失敗した場合のエラーハンドリングを実装します。

---

## 具体例


### CategoryRepository の例

```python
from django.db.models import QuerySet
from .models import Category

class CategoryRepository:
    @staticmethod
    def get_all() -> QuerySet:
        return Category.objects.all()

    @staticmethod
    def get_by_id(category_id: int) -> Category:
        return Category.objects.filter(id=category_id).first()
```


### SampleRepository の例

```python
from django.db.models import QuerySet
from .models import Sample

class SampleRepository:
    @staticmethod
    def create_sample(author_id: int, **kwargs) -> Sample:
        return Sample.objects.create(author_id=author_id, **kwargs)

    @staticmethod
    def search(query: str) -> QuerySet:
        return Sample.objects.filter(title__icontains=query)
```

---

## 注意点

- **依存性の注入**: リポジトリ層をサービス層に注入することで、依存性を明確にします。

- **パフォーマンスの最適化**: 必要に応じてクエリの最適化やキャッシュを利用します。

- **セキュリティ**: ユーザー入力を直接クエリに使用しないようにし、SQLインジェクションを防ぎます。

---

## 参考

- [Django ドキュメント](https://docs.djangoproject.com/)

- [Django REST Framework ドキュメント](https://www.django-rest-framework.org/)