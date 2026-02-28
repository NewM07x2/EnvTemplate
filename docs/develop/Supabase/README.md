# Supabase 学習ガイド

> **対象者**: 開発初心者・新規参画者向けの Supabase 解説資料です。このドキュメントを読むことで、Supabase の基本概念と実装方法を理解できます。

---

## 📚 目次

1. [Supabase とは何か](#supabaseとは何か)
2. [主な機能](#主な機能)
3. [アーキテクチャ](#アーキテクチャ)
4. [料金体系](#料金体系)
5. [ユースケース](#ユースケース)
6. [Next-Python での利用](#next-pythonでの利用)
7. [学習ロードマップ](#学習ロードマップ)
8. [よくある質問](#よくある質問)

---

## Supabase とは何か

### 🎯 簡潔な説明

**Supabase** は、**Firebase の代替として設計された、オープンソースのバックエンド・サービス（BaaS: Backend as a Service）** です。

```
従来の開発：      フロントエンド  ←→  [自分で構築するバックエンド]
                                    （DB、認証、API等を自分で実装）

Supabase 利用：   フロントエンド  ←→  Supabase
                                    （DB、認証、API 等が既に用意されている）
```

### 📖 詳しい説明

Supabase は **PostgreSQL データベース** を中心に、以下のサービスを提供します：

| 機能 | 説明 | 従来の実装方法 |
|------|------|--------------|
| **PostgreSQL Database** | フルマネージド PostgreSQL | 自分で DB サーバーを構築・管理 |
| **Authentication** | ユーザー認証・認可 | JWT や OAuth を自分で実装 |
| **Auto-Generated REST API** | DB テーブルからの自動 REST API | API エンドポイントを手書き |
| **Real-time Subscriptions** | リアルタイムデータ同期 | WebSocket を自分で実装 |
| **Edge Functions** | サーバーレス関数 | Lambda や Cloud Functions 相当 |
| **Vector Database** | AI・機械学習用の埋め込みベクトル | Pinecone や Weaviate を利用 |

### 🔑 重要な特徴

| 特徴 | メリット |
|------|---------|
| **PostgreSQL 準拠** | SQL 標準準拠。MySQL や Oracle より強力で、多くの開発者に熟知されている |
| **オープンソース** | Google や AWS 等のベンダーロックインがない。自分でセルフホスト可能 |
| **REST + GraphQL** | 同一の DB から REST API と GraphQL API の両方を自動生成 |
| **Row Level Security (RLS)** | DB レベルでの権限管理。クライアント側の不正をサーバーで防止 |
| **無料プラン有** | 開発・学習用には無料で十分 |

---

## 主な機能

### 1️⃣ **Database（PostgreSQL）**

Supabase が提供するマネージド PostgreSQL です。

**できること:**
- テーブル作成・カラム定義
- SQL クエリの実行
- トリガーやストアドプロシージャの作成
- バックアップ・復元

**例:**
```sql
-- Supabase のダッシュボード上で実行可能
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR UNIQUE NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);
```

### 2️⃣ **Authentication（ユーザー認証）**

メールアドレス・パスワード、Google・GitHub 等の OAuth 認証をサポート。

**できること:**
- ユーザー登録・ログイン・ログアウト
- メール確認・パスワードリセット
- ソーシャルログイン（Google、GitHub、Discord 等）
- JWT トークン生成・検証

**実装例（JavaScript/TypeScript）:**
```typescript
import { createClient } from '@supabase/supabase-js'

const supabase = createClient(URL, ANON_KEY)

// ログイン
const { data, error } = await supabase.auth.signInWithPassword({
  email: 'user@example.com',
  password: 'password123'
})

// 現在のユーザーを取得
const { data: { user } } = await supabase.auth.getUser()
```

### 3️⃣ **Auto-Generated REST API**

DB テーブルから自動的に REST API が生成されます。**コードを書かずに API が利用可能** です。

**例：**
- テーブル名が `posts` の場合

| HTTP メソッド | エンドポイント | 動作 |
|-------------|--------------|------|
| `GET` | `/rest/v1/posts` | すべての行を取得 |
| `GET` | `/rest/v1/posts?id=eq.1` | ID=1 の行を取得 |
| `POST` | `/rest/v1/posts` | 新しい行を挿入 |
| `PATCH` | `/rest/v1/posts?id=eq.1` | ID=1 の行を更新 |
| `DELETE` | `/rest/v1/posts?id=eq.1` | ID=1 の行を削除 |

### 4️⃣ **Real-time Subscriptions**

DB の変更をリアルタイムでクライアント側に通知します。

**例：チャットアプリ**
```typescript
// メッセージテーブルの変更をリアルタイム監視
supabase
  .channel('messages')
  .on('postgres_changes', 
    { event: 'INSERT', schema: 'public', table: 'messages' },
    (payload) => {
      console.log('新しいメッセージ:', payload.new)
      // UI を更新
    }
  )
  .subscribe()
```

### 5️⃣ **Edge Functions（サーバーレス関数）**

カスタムロジックが必要な場合、TypeScript で Edge Functions を書きます。

**用途:**
- 複雑なビジネスロジック
- 外部 API 呼び出し
- 定時ジョブ・スケジューラ
- Webhook ハンドラー

**例：**
```typescript
// supabase/functions/send-email/index.ts
import { serve } from 'https://deno.land/std@0.168.0/http/server.ts'

serve(async (req) => {
  const { email, message } = await req.json()
  
  // メール送信処理
  // ...
  
  return new Response(JSON.stringify({ ok: true }))
})
```

---

## アーキテクチャ

### Supabase を使った Web アプリケーションの構成

```
┌──────────────────────────────────────────────────────┐
│  フロントエンド (Next.js / React / Flutter / etc)   │
│  - UI コンポーネント                                  │
│  - 状態管理（Redux / Zustand / Riverpod）           │
│  - フォーム処理                                      │
└─────────────────────┬────────────────────────────────┘
                      │
         ┌────────────┼────────────┐
         │            │            │
         ▼            ▼            ▼
    ┌─────────┐  ┌─────────┐  ┌──────────────┐
    │REST API │  │GraphQL  │  │Real-time Sub │
    │(自動生成)│  │(自動生成)│  │(WebSocket)   │
    └────┬────┘  └────┬────┘  └───────┬──────┘
         │             │               │
         └─────────────┼───────────────┘
                       │
         ┌─────────────▼──────────────┐
         │   Supabase Backend         │
         ├────────────────────────────┤
         │ PostgreSQL Database        │
         │ ├─ テーブル定義            │
         │ ├─ RLS ポリシー            │
         │ └─ トリガー・関数           │
         ├────────────────────────────┤
         │ Authentication             │
         │ ├─ ユーザー管理            │
         │ ├─ JWT トークン            │
         │ └─ ソーシャルログイン       │
         ├────────────────────────────┤
         │ Edge Functions             │
         │ └─ カスタムロジック        │
         └────────────────────────────┘
```

### セキュリティレイヤー

Supabase は **3 段階のセキュリティ** を提供します：

```
1. API キーレベル（すべてのリクエスト）
   ├─ ANON_KEY（公開可能・制限あり）
   └─ SERVICE_KEY（秘密キー・フルアクセス）

2. 認証レベル
   └─ JWT トークン（ログイン後のリクエストに含める）

3. データベースレベル（RLS = Row Level Security）
   ├─ テーブル単位のアクセス制御
   ├─ 行（レコード）単位のアクセス制御
   └─ ポリシーで条件指定
```

---

## Next-Python での利用

next-python プロジェクトでは、Supabase は以下のように構成されています：

### 📁 ディレクトリ構造

```
next-python/
├── supabase/                    # Supabase 管理ファイル
│   ├── migrations/              # DB マイグレーション
│   │   ├── 20260102000000_initial_schema.sql
│   │   ├── 20260120000000_create_backoffice_tables.sql
│   │   └── ...
│   └── config.toml              # Supabase 設定
│
├── api/                         # FastAPI バックエンド
│   ├── app/
│   │   ├── repositories/        # DB アクセス層
│   │   ├── services/            # ビジネスロジック
│   │   ├── schemas/             # リクエスト/レスポンス型
│   │   └── graphql/             # GraphQL スキーマ
│   └── main.py
│
└── web/                         # Next.js フロントエンド
    ├── src/
    │   ├── hooks/               # useQuery 等の Supabase 接続
    │   └── lib/                 # Supabase クライアント設定
    └── package.json
```

### 🔄 データフロー

```
1. フロントエンド (Next.js) がユーザーアクション検出
            ↓
2. Supabase クライアント経由で API/DB にアクセス
            ↓
3. Supabase のいずれかで処理
   ├─ REST API（自動生成）で直接 DB アクセス
   ├─ GraphQL で複雑なクエリ実行
   ├─ Edge Functions で複雑なロジック実行
   └─ FastAPI でビジネスロジック実行
            ↓
4. レスポンスがフロントエンドに返却
            ↓
5. UI が更新
```

---

## 学習ロードマップ

### レベル 1: 基礎（1〜2 日）

- [ ] Supabase アカウント作成・プロジェクト作成
- [ ] ダッシュボード（管理画面）の操作方法学習
- [ ] テーブル作成・カラム定義
- [ ] SQL クエリの実行
- [ ] 簡単な SELECT/INSERT/UPDATE/DELETE

**リソース:**
- [Supabase 公式チュートリアル](https://supabase.com/docs)
- [PostgreSQL 入門](https://www.postgresql.org/docs/)

### レベル 2: 認証・API（2〜3 日）

- [ ] Authentication の設定
- [ ] メールアドレス・パスワード認証の実装
- [ ] REST API を使ったデータ取得
- [ ] RLS ポリシーの基本理解
- [ ] ANON_KEY と SERVICE_KEY の使い分け

**リソース:**
- [Supabase Auth 公式ドキュメント](https://supabase.com/docs/guides/auth)
- [REST API リファレンス](https://supabase.com/docs/reference/javascript/introduction)

### レベル 3: 実装パターン（3〜5 日）

- [ ] Next.js / React での Supabase 統合
- [ ] カスタムフック（useQuery 等）の作成
- [ ] リアルタイムデータ同期（Subscriptions）
- [ ] GraphQL の基本
- [ ] Edge Functions でのカスタムロジック

**リソース:**
- [Supabase + Next.js の公式ガイド](https://supabase.com/docs/guides/getting-started/quickstarts/nextjs)
- [@supabase/supabase-js クライアント](https://github.com/supabase/supabase-js)

### レベル 4: 応用（5〜7 日）

- [ ] 複雑な RLS ポリシー設計
- [ ] トリガーとストアドプロシージャ
- [ ] マイグレーション管理（CI/CD 連携）
- [ ] パフォーマンスチューニング（インデックス等）
- [ ] エラーハンドリング・バリデーション

**リソース:**
- [PostgreSQL チュートリアル](https://www.postgresql.org/docs/current/tutorial.html)
- [Supabase RLS ガイド](https://supabase.com/docs/guides/auth/row-level-security)

---

## よくある質問

### Q1: Firebase との違いは？

| 特徴 | Supabase | Firebase |
|------|----------|----------|
| DB | PostgreSQL（SQL）| NoSQL（Firestore） |
| オープンソース | ✅ | ❌ |
| セルフホスト | ✅ | ❌ |
| 学習曲線 | 中程度（SQL 知識必要）| 緩い |
| ベンダーロック | なし | Google に依存 |

**結論:** SQL に詳しいなら Supabase、初心者なら Firebase がおすすめ。

### Q2: Supabase だけで十分？ FastAPI は不要？

**答え:** プロジェクトによる。

- **Supabase で足りる:** CRUD 中心のシンプルなアプリ
- **FastAPI 併用が必要:** 複雑なビジネスロジック、外部 API 連携、機械学習等

next-python は両方を使う：
- **シンプルなデータ取得** → Supabase REST API（ダイレクト）
- **複雑なロジック** → FastAPI Edge Functions（カスタム実装）

### Q3: 本番環境のセキュリティは大丈夫？

**答え:** Supabase は以下を実装しているため安全：

- ✅ Row Level Security（RLS）で行レベルのアクセス制御
- ✅ JWT トークン検証
- ✅ ANON_KEY と SERVICE_KEY の分離
- ✅ HTTPS 通信
- ✅ バックアップ・冗長性

ただし、**キーの管理は自分の責任**。環境変数で秘密キーを保護すること。

### Q4: コストはいくら？

詳細は「[料金体系](#料金体系)」セクションを参照してください。

---

## 料金体系

> 最新情報は [Supabase Pricing](https://supabase.com/pricing) を確認してください（価格は変動する場合があります）。

### プラン比較表

| プラン | 月額 | 主な用途 |
|--------|------|----------|
| **Free** | $0 | 個人開発・学習・PoC |
| **Pro** | $25 | 小〜中規模プロダクション |
| **Team** | $599 | チーム開発・SLA 保証 |
| **Enterprise** | 要問合せ | 大規模・セキュリティ要件あり |

### Free プラン（無料）

| リソース | 上限 |
|---------|------|
| **DB 容量** | 500 MB |
| **ストレージ** | 1 GB |
| **転送量** | 5 GB / 月 |
| **Edge Functions** | 50 万回 / 月 |
| **認証ユーザー数** | 無制限 |
| **Realtime メッセージ** | 200 万 / 月 |
| **プロジェクト数** | 2 件（アクティブ） |
| **バックアップ** | なし |
| **SLA** | なし |

> ⚠️ **重要**: Free プランのプロジェクトは **7 日間アクセスがないと一時停止**されます。本番運用には Pro 以上を推奨します。

### Pro プラン（$25 / 月）

| リソース | 上限 |
|---------|------|
| **DB 容量** | 8 GB（超過分 $0.125 / GB）|
| **ストレージ** | 100 GB（超過分 $0.021 / GB）|
| **転送量** | 250 GB / 月（超過分 $0.09 / GB）|
| **Edge Functions** | 500 万回 / 月 |
| **バックアップ** | 日次バックアップ（7 日間保持）|
| **プロジェクト数** | 無制限 |
| **SLA** | なし（Team プランから）|
| **自動一時停止** | なし |

### Team プラン（$599 / 月）

- Pro プランのすべての機能 ＋
- **99.9% SLA 保証**
- **14 日間のバックアップ保持**
- **SOC 2 Type II 準拠**
- **HIPAA 対応**（オプション）
- **優先サポート**

### コスト試算の目安

| フェーズ | 推奨プラン | 理由 |
|---------|-----------|------|
| 開発・学習 | Free | コスト 0。制限内で十分 |
| MVP・PoC | Free → Pro | ユーザーが増えたら移行 |
| 小規模プロダクション | Pro | 自動停止なし・バックアップあり |
| チーム開発・SLA 必要 | Team | SLA・セキュリティ要件を満たす |
| 大企業・規制業界 | Enterprise | カスタム契約・専任サポート |

### セルフホスト（無料）

Supabase はオープンソースのため、**自前のサーバーに無料で構築**することも可能です。

```bash
# Docker Compose でセルフホスト
git clone https://github.com/supabase/supabase
cd supabase/docker
cp .env.example .env
docker compose up -d
```

- **メリット**: コストゼロ、データを完全に自社管理
- **デメリット**: インフラ管理・セキュリティ対応が自己責任

---

## ユースケース

### 📱 Supabase が「向いている」ケース

#### 1. SaaS・Web アプリのバックエンド

```
構成例: Next.js + Supabase

フロントエンド (Next.js)
  │
  ├─ ユーザー認証     → Supabase Auth
  ├─ データ取得・更新  → Supabase REST API (RLS で保護)
  ├─ リアルタイム通知  → Supabase Realtime
  └─ ファイルアップロード → Supabase Storage
```

**具体例:**
- タスク管理アプリ（Notion 風）
- ブログ・CMS
- EC サイト（小〜中規模）
- ダッシュボード・分析ツール

#### 2. モバイルアプリのバックエンド

```
構成例: React Native / Flutter + Supabase

モバイルアプリ
  │
  ├─ ログイン / SNS 認証  → Supabase Auth
  ├─ プロフィール画像      → Supabase Storage
  ├─ チャット機能          → Supabase Realtime
  └─ ユーザーデータ        → Supabase DB + RLS
```

**具体例:**
- チャットアプリ
- SNS・コミュニティアプリ
- フィットネス記録アプリ

#### 3. AI・機械学習アプリ

```
構成例: Next.js + Supabase Vector + OpenAI

ユーザー入力
  → OpenAI で埋め込みベクトル生成
  → Supabase pgvector で類似検索
  → 関連ドキュメントを返す（RAG）
```

**具体例:**
- AI チャットボット（社内知識検索）
- 類似商品推薦システム
- ドキュメント Q&A ツール

#### 4. リアルタイムアプリ

```
構成例: Supabase Realtime Subscriptions

ユーザー A が投稿
  → DB に INSERT
  → Supabase が変更を検知
  → 購読中の全クライアントに即時通知
```

**具体例:**
- チャット・メッセージングアプリ
- コラボレーションツール（Google Docs 風）
- ライブスコア・通知システム
- オンラインゲームのリーダーボード

---

### ⚠️ Supabase が「向いていない」ケース

| ケース | 理由 | 代替手段 |
|--------|------|----------|
| 超大規模トランザクション（数億件 / 日） | マネージド PostgreSQL のスケール上限 | AWS Aurora、PlanetScale |
| NoSQL 形式のデータが中心 | Supabase は PostgreSQL（リレーショナル）| MongoDB、Firebase |
| 複雑な ML パイプライン | Edge Functions は軽量処理向け | AWS SageMaker、Google Vertex AI |
| 完全にオフライン動作するアプリ | クラウド依存 | SQLite + Drift（ローカル DB）|
| 金融・医療など高度な規制対応 | Free/Pro では SLA・コンプライアンス不十分 | Team/Enterprise プランまたは AWS |

---

### 🏗️ アーキテクチャパターン別の選択指針

```
[シンプルな CRUD アプリ]
フロントエンド → Supabase のみ
└─ ロジックが少なく、CRUD 中心のアプリに最適

[中規模アプリ（ビジネスロジックあり）]
フロントエンド → Supabase (Auth + DB + RLS)
                ↕
              Edge Functions（軽量なカスタムロジック）

[大規模アプリ（複雑なロジック）]
フロントエンド → API サーバー (FastAPI / NestJS 等)
                ↕
              Supabase（DB + Auth + Storage のみ活用）
└─ ビジネスロジックは API サーバーに集約
```

---

## 次のステップ

### レベル 1-2（基礎）
1. [Supabase クイックスタート](01_クイックスタート.md) → アカウント作成～最初のテーブル作成
2. [Authentication ガイド](02_認証ガイド.md) → ユーザー認証の実装
3. [REST API ガイド](03_REST_APIガイド.md) → フロントエンドからのデータ取得
4. [RLS（Row Level Security）ガイド](04_RLSガイド.md) → セキュアなデータアクセス

### レベル 3（実装パターン）
5. [Next.js 統合ガイド](05_Next.js統合ガイド.md) → Next.js / React での実践的な統合
6. [Edge Functions ガイド](06_EdgeFunctionsガイド.md) → サーバーレス関数によるカスタムロジック

### レベル 4（応用）
7. [マイグレーション管理](07_マイグレーション管理.md) → CI/CD 連携・スキーマ変更の安全な運用

### レベル 5（機能別詳細）
8. [PostgreSQL 機能ガイド](08_PostgreSQL機能ガイド.md) → インデックス・トリガー・JSONB・全文検索
9. [Storage ガイド](09_Storageガイド.md) → ファイルアップロード・画像変換・ストレージポリシー
10. [Realtime 詳細ガイド](10_Realtime詳細ガイド.md) → リアルタイム同期・チャット・Presence
11. [Vector / AI 機能ガイド](11_Vector_AI機能ガイド.md) → pgvector・RAG・AI 検索

### レベル 6（品質・運用）
12. [テストガイド](12_テストガイド.md) → pgTAP・RLS テスト・Vitest・E2E テスト
13. [デプロイ・CI/CD ガイド](13_デプロイ・CI/CDガイド.md) → GitHub Actions・環境分離・ロールバック
14. [パフォーマンスガイド](14_パフォーマンスガイド.md) → インデックス戦略・N+1 解消・キャッシュ・モニタリング

---

**Supabase での開発を楽しんでください！不明な点があれば、公式ドキュメントを参照するか、チーム内で相談してください。**
