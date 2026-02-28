# Structure — 正式アーキテクチャ定義（Authoritative）

本ドキュメントは、本リポジトリの不変アーキテクチャ構造を定義する。

本ルールは交渉不可である。
リファクタリングや最適化よりも、安定性と予測可能性を最優先とする。

---

# 1. プロジェクト構成

本リポジトリは以下の構成となる：

- **フロントエンド:** Flutter/Dart (`app/lib/`)
- **バックエンド API:** FastAPI + GraphQL (`api/`)
- **データベース（クラウド）:** Supabase PostgreSQL (`supabase/migrations/`)
- **ローカルDB:** Drift SQLite (`app/lib/data/local/`)

---

# 2. Flutter アーキテクチャ（クリーンアーキテクチャ）

層構造は必ず以下とする：

Presentation Layer（UI/State Management）
        ↓
Business Logic Layer（Providers/UseCase）
        ↓
Data Layer（Repository/DataSource）
        ↓
FastAPI / Supabase / Local Database

逸脱は一切許可しない。

---

# 3. ディレクトリ構造（正式定義）

## 3.1 フロントエンド（`app/lib/`）

```
lib/
├── core/              # 横断的な共有ロジック
│   ├── services/      # Supabase/API/DB接続サービス
│   ├── theme/         # テーマ・スタイル定義
│   └── widgets/       # 再利用可能な共有Widget
│
├── data/              # Data層（リポジトリ・データソース）
│   ├── local/         # Drift SQLite実装
│   ├── models/        # データモデル（Drift Entity等）
│   ├── repositories/  # Repository実装
│   ├── services/      # API/DB接続ロジック
│   └── providers.dart # 共有Provider定義
│
├── features/          # Presentation + Business Logic層
│   ├── analysis/      # 分析機能
│   ├── backoffice/    # 管理画面
│   ├── character/     # キャラクター機能
│   ├── contact/       # お問い合わせ
│   ├── home/          # ホーム画面
│   ├── notifications/ # 通知機能
│   ├── poop_log/      # 排便記録機能
│   ├── settings/      # 設定
│   └── terms/         # 利用規約等
│       ├── data/            # 機能別データソース
│       ├── domain/          # ビジネスロジック・UseCase
│       └── presentation/    # UI・State Management
│           ├── pages/       # スクリーン
│           ├── widgets/     # 機能別Widget
│           └── providers/   # Riverpod provider
│
├── l10n/              # 国際化（多言語対応）
└── main.dart          # エントリーポイント
```

## 3.2 バックエンド API（`api/`）

```
api/
├── app/
│   ├── api/           # RESTful エンドポイント
│   ├── core/          # 設定・セキュリティ・DB接続
│   ├── graphql/       # GraphQL スキーマ・リゾルバー
│   │   ├── schemas/   # GraphQL型定義
│   │   └── resolvers/ # クエリ・ミューテーション実装
│   ├── middleware/    # ロギング・タイミング計測等
│   ├── models/        # データモデル
│   ├── repositories/  # DB アクセス層
│   ├── schemas/       # Pydantic スキーマ
│   ├── services/      # ビジネスロジック
│   └── utils/         # ヘルパー関数
├── prisma/            # Prisma スキーマ（ORM定義）
├── tests/             # テストコード
├── main.py            # エントリーポイント
├── docker-compose.yml # Docker設定
└── pyproject.toml     # Python依存管理
```

## 3.3 データベース（`supabase/`）

```
supabase/
├── migrations/        # PostgreSQL マイグレーション
│   ├── 20260102000000_initial_schema.sql
│   ├── 20260120000000_create_backoffice_tables.sql
│   └── ...（順序付き）
└── config.toml        # Supabase設定
```

---

# 4. 層ごとの責務

## 4.1 Presentation Layer（Flutter）

位置: `features/[feature]/presentation/`

責務:
- UI描画のみ
- ユーザー入力の受け取り
- 状態管理（Riverpod provider）
- ビジネスロジックの呼び出し

禁止事項:
- 直接DB・API呼び出し
- 複雑な業務ロジック
- APIクライアント実装

## 4.2 Business Logic Layer（Flutter）

位置: `features/[feature]/domain/` + `providers/`

責務:
- UseCase（ビジネスルール）実装
- Riverpod Provider定義
- ユースケースの組み合わせ

禁止事項:
- UIフレームワーク依存
- 直接DB・API呼び出し
- UI描画

## 4.3 Data Layer（Flutter）

位置: `data/datasources/`, `data/repositories/`, `data/models/`, `data/local/`

責務:
- Supabase / FastAPI との通信
- Drift SQLite アクセス
- データ取得・永続化
- Entity ⇄ Model の変換

禁止事項:
- ビジネスロジック
- UI描画
- Presentation層への直接参照

## 4.4 Backend API Layer（FastAPI）

位置: `api/app/`

責務:
- RESTful / GraphQL エンドポイント実装
- リクエスト・レスポンス処理
- ビジネスロジック実装（Service層）
- データベースアクセス（Repository層）

禁止事項:
- UI処理
- 認証・認可はmiddleware層で実装

### 4.4.1 API層の構成

- **api/** — RESTful エンドポイント
- **graphql/** — GraphQL スキーマ・リゾルバー
- **services/** — ビジネスロジック
- **repositories/** — PostgreSQL アクセス
- **schemas/** — リクエスト・レスポンス型定義
- **models/** — データモデル
- **middleware/** — ロギング・タイミング・認証
- **core/** — 設定・DB接続・セキュリティ

## 4.5 Database Layer

### 4.5.1 Supabase PostgreSQL（クラウド）

位置: `supabase/migrations/`

責務:
- スキーマ定義
- RLS（Row Level Security）ポリシー
- ストアドプロシージャ（必要最小限）

### 4.5.2 Drift SQLite（ローカル）

位置: `app/lib/data/local/`, `app/lib/data/models/`

責務:
- ローカルキャッシュ
- オフライン対応
- 高速アクセス

---

# 5. 依存関係制約（厳格）

## 5.1 Flutter側の依存方向

許可される依存方向:
```
Presentation → Business Logic → Data → FastAPI / Supabase / Drift
```

禁止される逆方向参照:
- ✗ Data層がPresentation層を参照
- ✗ Data層がBusiness Logic層を参照
- ✗ Business Logic層がPresentation層を参照
- ✗ Presentation層がData層を直接参照

## 5.2 FastAPI側の依存方向

許可される依存方向:
```
API Endpoint → Service → Repository → Database
```

禁止事項:
- ✗ Repository がService を参照
- ✗ Endpoint が Repository を直接参照
- ✗ 層をスキップした呼び出し

---

# 6. State Management（Riverpod）

必ず以下のルールに従う:

- Provider定義は `presentation/providers/` または `domain/` に配置
- StateNotifier/StateNotifierProvider を使用
- UI層は Provider 経由でのみアクセス
- ローカルキャッシュが必要な場合は Drift を使用
- Provider間の依存関係を明示的に定義する

---

# 7. Database設計

## 7.1 Supabase PostgreSQL（クラウド）

マイグレーション: `supabase/migrations/`

ルール:
- スキーマ定義のみ
- ストアドプロシージャは最小限
- RLS（Row Level Security）ポリシー定義
- 実行順序で順番付け（`20260102000000_initial_schema.sql` など）

## 7.2 Drift SQLite（ローカル）

位置: `app/lib/data/local/`, `app/lib/data/models/`

ルール:
- Supabase スキーマとの同期
- オフライン対応用キャッシュ
- ローカル専用データ（キャッシュ等）の保存
- Entity定義と Supabase スキーマの整合性を確認

## 7.3 FastAPI + PostgreSQL（Prisma ORM）

位置: `api/prisma/schema.prisma`

ルール:
- Prisma ORM で PostgreSQL スキーマを定義
- Supabase マイグレーション と一致させる
- リレーションシップを明示的に定義

---

# 8. パッケージ命名規約

## 8.1 Flutter側

**機能単位の場合:**
```
features.{feature_name}.presentation.pages
features.{feature_name}.presentation.widgets
features.{feature_name}.presentation.providers
features.{feature_name}.domain
features.{feature_name}.data
```

**共有コンポーネント:**
```
core.services
core.theme
core.widgets
```

**データ層:**
```
data.datasources
data.repositories
data.models
data.local
```

## 8.2 FastAPI側（Python）

**API層:**
```
app.api                  # RESTful エンドポイント
app.graphql.schemas     # GraphQL型定義
app.graphql.resolvers   # GraphQL クエリ・ミューテーション
```

**ビジネスロジック:**
```
app.services            # ビジネスロジック実装
app.repositories        # DB アクセス層
```

**その他:**
```
app.core                # 設定・セキュリティ
app.schemas             # Pydantic スキーマ
app.models              # データモデル
app.middleware          # ミドルウェア
```

---

# 9. 変更時の修正順序（厳守）

### DB変更を伴う機能追加（フロント＋バックエンド）:

1. `supabase/migrations/` で PostgreSQL スキーマ修正
2. `api/prisma/schema.prisma` で Prisma スキーマ更新
3. `api/app/repositories/` で Repository 実装
4. `api/app/services/` で ビジネスロジック実装
5. `api/app/graphql/` または `api/app/api/` で エンドポイント実装
6. `app/lib/data/models/` で Drift Entity 更新
7. `app/lib/data/repositories/` で Repository 実装
8. `features/[feature]/domain/` で UseCase 更新
9. `features/[feature]/presentation/` で UI 更新

### DB変更を伴う修正（フロントエンドのみ）:

1. `supabase/migrations/` で PostgreSQL スキーマ修正
2. `app/lib/data/models/` で Drift Entity 更新
3. `app/lib/data/repositories/` で Repository 更新
4. `features/[feature]/domain/` で UseCase 更新
5. `features/[feature]/presentation/` で UI 更新

### API側のみのビジネスロジック変更:

1. `api/app/services/` で ビジネスロジック修正
2. `api/app/graphql/` または `api/app/api/` で エンドポイント修正

### 業務ロジックのみ変更（フロントエンド）:

1. `features/[feature]/domain/` で UseCase 更新
2. `features/[feature]/presentation/providers/` で Provider 更新
3. `features/[feature]/presentation/` で UI 更新

必ずこの順序を守ること。

---

# 10. 設計思想

- 優雅さより安定性
- 賢さより明示性
- 改善より一貫性
- 大規模変更より最小差分

迷った場合:

同一ディレクトリ内の既存実装に従うこと。
アーキテクチャ改善を試みてはならない。
