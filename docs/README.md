# 開発ドキュメント

このリポジトリに含まれる開発者向け学習資料のインデックスです。

---

## 📂 ドキュメント一覧

### BaaS（Backend as a Service）

| カテゴリ | ドキュメント | 概要 |
|---------|------------|------|
| **Supabase** | [学習ガイド](develop/Supabase/README.md) | PostgreSQL ベースのオープンソース BaaS |
| **Firebase** | [学習ガイド](Firebase/README.md) | Google が提供する BaaS |
| **比較** | [Firebase vs Supabase](比較/Firebase_vs_Supabase.md) | 技術選定の判断基準 |

---

### 開発ツール・インフラ

| カテゴリ | ドキュメント | 概要 |
|---------|------------|------|
| **Docker** | [入門ガイド](develop/Docker/README.md) | コンテナ化・docker-compose 実践 |
| **Prisma** | [ORM ガイド](develop/Prisma/README.md) | 型安全な DB アクセス・マイグレーション |
| **GitHub Actions** | [CI/CD ガイド](develop/GitHubActions/README.md) | 自動テスト・デプロイ |
| **テスト** | [Vitest / Jest ガイド](develop/テスト/README.md) | フロントエンド・モバイルテスト |

---

### バックエンド・フレームワーク

| カテゴリ | ドキュメント | 概要 |
|---------|------------|------|
| **Go + Echo** | [API ガイド](develop/Go/README.md) | Go の REST API 開発 |
| **FastAPI** | [Python API ガイド](develop/FastAPI/README.md) | Python の高速 API 開発 |
| **Hono** | [Cloudflare Workers ガイド](develop/Hono/README.md) | エッジ API・サーバーレス開発 |
| **Flutter** | [入門ガイド](develop/Flutter/README.md) | クロスプラットフォームアプリ開発 |

---

### 比較・技術選定

| カテゴリ | ドキュメント | 概要 |
|---------|------------|------|
| **フロントエンド** | [フレームワーク比較](比較/フロントエンドフレームワーク比較.md) | 11テンプレートのフレームワーク選定ガイド |
| **BaaS** | [Firebase vs Supabase](比較/Firebase_vs_Supabase.md) | 機能・料金・ユースケース別比較 |

---

### Supabase シリーズ

```
docs/develop/Supabase/
├── README.md                  ← 概要・料金体系・ユースケース
├── 01_クイックスタート.md      ← セットアップ（15分）
├── 02_認証ガイド.md           ← Auth 実装（30分）
├── 03_REST_APIガイド.md       ← データ操作（40分）
├── 04_RLSガイド.md            ← セキュリティ（50分）
├── 05_Next.js統合ガイド.md    ← App Router 統合（60分）
├── 06_EdgeFunctionsガイド.md  ← サーバーレス関数（50分）
├── 07_マイグレーション管理.md  ← CI/CD・スキーマ管理（60分）
├── 08_PostgreSQL活用ガイド.md ← 高度な SQL・全文検索（60分）
├── 09_Storageガイド.md        ← ファイルアップロード（40分）
├── 10_Realtimeガイド.md       ← リアルタイム通信（50分）
└── 11_Vector_AIガイド.md      ← ベクトル検索・AI 連携（60分）
```

### Firebase シリーズ

```
docs/Firebase/
├── README.md                        ← シリーズインデックス
├── 01_Firebaseとは.md               ← 概要・主な機能・比較（15分）
├── 02_クイックスタート.md            ← セットアップ（20分）
├── 03_認証ガイド.md                 ← Auth 実装（30分）
├── 04_Firestoreガイド.md            ← データ操作・セキュリティ（40分）
├── 05_CloudFunctionsガイド.md       ← サーバーレス関数（50分）
├── 06_StorageAndHostingガイド.md    ← ファイル管理・ホスティング（40分）
└── 07_FCMAndAnalyticsガイド.md      ← プッシュ通知・分析（40分）
```

---

## 🗺️ 学習ロードマップ

### 初めてこのリポジトリを使う場合

```
1. 使用するフレームワークを決める
   → 比較/フロントエンドフレームワーク比較.md

2. Docker で環境を起動する
   → develop/Docker/README.md

3. DB アクセスを実装する（Prisma 使用テンプレートの場合）
   → develop/Prisma/README.md

4. BaaS を選んで連携する
   ├── SQL / Next.js 中心 → develop/Supabase/ シリーズ
   └── モバイル / NoSQL   → Firebase/ シリーズ

5. テストを書く
   → develop/テスト/README.md

6. CI/CD を設定する
   → develop/GitHubActions/README.md
```

### テンプレート別の推奨ガイド

| テンプレート | 推奨ガイド |
|------------|----------|
| `next/` `nuxt/` `remix/` `sveltekit/` | Docker → Prisma → Supabase → テスト → GitHub Actions |
| `react/` `vue/` `astro/` | Docker → テスト → GitHub Actions |
| `go/echo-app/` `next-go/` | Docker → Go + Echo → GitHub Actions |
| `python/FastAPI/` `next-python/` | Docker → FastAPI → GitHub Actions |
| `hono-cloudflare/` | Hono → GitHub Actions |
| `flutter/` | Flutter → Firebase |
| `react-native/` | テスト（Jest） → Firebase |
| `next-fastapi-supabase/` | Docker → FastAPI → Supabase → GitHub Actions |

---

## 📁 ディレクトリ構造

```
docs/
├── README.md              ← このファイル（インデックス）
├── develop/
│   ├── Supabase/          ← Supabase シリーズ（01〜11）
│   ├── Docker/            ← Docker・docker-compose 入門
│   ├── Prisma/            ← Prisma ORM ガイド
│   ├── GitHubActions/     ← CI/CD ガイド
│   ├── Flutter/           ← Flutter 入門ガイド
│   ├── Go/                ← Go + Echo API ガイド
│   ├── FastAPI/           ← FastAPI ガイド
│   ├── Hono/              ← Hono + Cloudflare Workers ガイド
│   └── テスト/            ← Vitest / Jest テストガイド
├── Firebase/              ← Firebase シリーズ（01〜07）
└── 比較/
    ├── Firebase_vs_Supabase.md
    └── フロントエンドフレームワーク比較.md
```

---

## 📝 ドキュメントの追加方法

新しい技術の学習資料を追加する場合は以下のディレクトリに配置してください：

```
docs/
├── develop/     ← 技術別の詳細ガイド（複数ファイルのシリーズ）
├── 比較/        ← 技術比較・選定ガイド
└── Firebase/    ← Firebase シリーズ（既存）
```

**命名規則**: `{連番}_{内容}.md`（例: `01_クイックスタート.md`）
