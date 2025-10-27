# サービス層の概要

ビジネスロジックを実装するためのサービス層について説明します。この層は、リポジトリを使用してデータベース操作を行い、アプリケーションのルールや制約を実装します。

## サービス層の目的

- ビジネスロジックを集約し、ビューやコントローラーから分離する。
- データベース操作をリポジトリに委譲し、コードの再利用性を向上させる。
- アプリケーションのルールや制約を実装する。

## 使用用途

- データの取得、作成、更新、削除などの操作を一元管理する。
- 入力データの検証や、関連するデータの整合性を確保する。
- 複数のリポジトリや外部サービスを統合して処理を行う。
- ビジネスルールに基づいたエラーハンドリングを実装する。
- データの状態に応じた追加処理（例: 公開日時の自動設定、閲覧数のインクリメント）を行う。

## サービス層のクラス

### SampleService

サンプルデータに関するビジネスロジックを管理します。

#### 主なメソッド

- `get_samples(skip: int, limit: int, published_only: bool) -> List[Sample]`
  - ページネーションを使用してサンプルを取得します。
- `create_sample(author_id: int, **kwargs) -> Sample`
  - 新しいサンプルを作成します。
- `update_sample(sample_id: int, user_id: int, is_staff: bool, **kwargs) -> Sample`
  - 既存のサンプルを更新します。
- `delete_sample(sample_id: int, user_id: int, is_staff: bool) -> bool`
  - サンプルを削除します。

### CategoryService

カテゴリデータに関するビジネスロジックを管理します。

#### 主なメソッド

- `get_categories() -> List[Category]`
  - すべてのカテゴリを取得します。
- `get_category(category_id: int) -> Category`
  - IDでカテゴリを取得します。

## よく使用する書き方

### サービスの初期化

```python
from .services import SampleService, CategoryService

sample_service = SampleService()
category_service = CategoryService()
```

### サンプルデータの取得

```python
samples = sample_service.get_samples(skip=0, limit=10, published_only=True)
for sample in samples:
    print(sample.title)
```

### サンプルデータの作成

```python
new_sample = sample_service.create_sample(
    author_id=1,
    title="新しいサンプル",
    content="サンプルの内容",
    is_published=True
)
print(new_sample.id)
```

### サンプルデータの更新

```python
updated_sample = sample_service.update_sample(
    sample_id=1,
    user_id=1,
    title="更新されたタイトル"
)
print(updated_sample.title)
```

### サンプルデータの削除

```python
is_deleted = sample_service.delete_sample(sample_id=1, user_id=1)
if is_deleted:
    print("削除成功")
```

---

このドキュメントは、サービス層の使用方法を理解しやすくするためのガイドです。必要に応じて更新してください。
