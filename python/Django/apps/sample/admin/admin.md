# 管理画面の概要

Django 管理画面でのモデルの表示方法をカスタマイズするための設定について説明します。

このドキュメントでは、管理画面で実施するべき内容や目的、使用用途を整理します。

## 管理画面の目的

- モデルデータを簡単に管理・操作できるインターフェースを提供する
- データの作成、更新、削除を効率的に行う
- データの検索やフィルタリングを容易にする
- データの整合性を保ちながら、管理者が操作できるようにする

## 使用用途

- モデルデータの一覧表示、詳細表示、編集、削除
- フィルタリングや検索機能を活用して特定のデータを素早く見つける
- データの入力補助 (例: `prepopulated_fields` を使用して自動生成)
- 読み取り専用フィールドを設定して重要なデータを保護する
- カスタムアクションを追加して特定の操作を簡略化する

## 各管理クラスの役割

### CategoryAdmin

- **対象モデル**: `Category`
- **主な機能**:
  - 一覧画面に `name`, `slug`, `created_at` を表示
  - `created_at` フィールドでフィルタリング可能
  - `name`, `slug`, `description` で検索可能
  - `name` フィールドから `slug` を自動生成
  - デフォルトの並び順を `name` に設定

### PostAdmin

- **対象モデル**: `Post`
- **主な機能**:
  - 一覧画面に `title`, `author`, `category`, `is_published`, `published_at`, `views_count`, `created_at` を表示
  - `is_published`, `category`, `created_at`, `published_at` でフィルタリング可能
  - `title`, `content`, `excerpt` で検索可能
  - `title` フィールドから `slug` を自動生成
  - デフォルトの並び順を `-created_at` に設定
  - 日付ベースのナビゲーションを `created_at` に設定
  - 詳細画面で以下のフィールドセットを定義:
    - 基本情報: `title`, `slug`, `author`, `category`
    - コンテンツ: `content`, `excerpt`
    - 公開設定: `is_published`, `published_at`
    - 統計情報: `views_count`, `likes_count` (折りたたみ可能)
    - タイムスタンプ: `created_at`, `updated_at` (折りたたみ可能)
  - 読み取り専用フィールド: `created_at`, `updated_at`, `views_count`, `likes_count`

## よく使用する設定例

### 一覧画面のカスタマイズ

```python
list_display = ['name', 'slug', 'created_at']
list_filter = ['created_at']
search_fields = ['name', 'slug', 'description']
```

### 詳細画面のフィールドセット

```python
fieldsets = (
    ('基本情報', {
        'fields': ('title', 'slug', 'author', 'category')
    }),
    ('コンテンツ', {
        'fields': ('content', 'excerpt')
    }),
    ('公開設定', {
        'fields': ('is_published', 'published_at')
    }),
)
```

### 読み取り専用フィールド

```python
readonly_fields = ['created_at', 'updated_at']
```

---

このドキュメントは、Django 管理画面の設定を理解しやすくするためのガイドです。

必要に応じて更新してください。

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Categoryモデルの管理画面設定。

    表示フィールド、検索フィールド、フィルタリングオプションなどを定義します。
    """
    
    list_display = ['name', 'slug', 'created_at']  # 一覧画面に表示するフィールド
    list_filter = ['created_at']  # サイドバーでのフィルタリングオプション
    search_fields = ['name', 'slug', 'description']  # 検索可能なフィールド
    prepopulated_fields = {'slug': ('name',)}  # nameフィールドからslugを自動生成
    ordering = ['name']  # デフォルトの並び順


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """
    Postモデルの管理画面設定。

    表示フィールド、検索フィールド、フィルタリングオプション、
    および詳細画面のフィールドセットを定義します。
    """
    
    list_display = [
        'title', 'author', 'category', 'is_published',
        'published_at', 'views_count', 'created_at'
    ]  # 一覧画面に表示するフィールド
    list_filter = ['is_published', 'category', 'created_at', 'published_at']  # フィルタリングオプション
    search_fields = ['title', 'content', 'excerpt']  # 検索可能なフィールド
    prepopulated_fields = {'slug': ('title',)}  # titleフィールドからslugを自動生成
    ordering = ['-created_at']  # デフォルトの並び順
    date_hierarchy = 'created_at'  # 日付ベースのナビゲーション
    
    fieldsets = (
        ('基本情報', {
            'fields': ('title', 'slug', 'author', 'category')
        }),
        ('コンテンツ', {
            'fields': ('content', 'excerpt')
        }),
        ('公開設定', {
            'fields': ('is_published', 'published_at')
        }),
        ('統計情報', {
            'fields': ('views_count', 'likes_count'),
            'classes': ('collapse',)  # 折りたたみ可能
        }),
        ('タイムスタンプ', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)  # 折りたたみ可能
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at', 'views_count', 'likes_count']  # 読み取り専用フィールド
