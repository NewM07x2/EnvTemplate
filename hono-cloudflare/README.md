# Hono + Cloudflare Workers エッジコンピューティングテンプレート

超高速・軽量な Hono フレームワークと Cloudflare Workers を組み合わせた、エッジコンピューティング対応の API テンプレートです。

## 📋 目次

- [概要](#概要)
- [技術スタック](#技術スタック)
- [プロジェクト構成](#プロジェクト構成)
- [セットアップ](#セットアップ)
- [開発](#開発)
- [テスト](#テスト)
- [デプロイ](#デプロイ)
- [Cloudflare サービス統合](#cloudflareサービス統合)
- [パフォーマンス](#パフォーマンス)
- [トラブルシューティング](#トラブルシューティング)

## 概要

### 主な特徴

- **⚡ 超高速**: Hono は他のフレームワークより最大 3 倍高速
- **🌍 グローバルエッジ**: Cloudflare Workers で世界中にデプロイ
- **🪶 超軽量**: バンドルサイズが非常に小さい
- **🔄 マルチランタイム**: Cloudflare/Deno/Bun/Node.js 対応
- **🛡️ 型安全**: TypeScript ファースト設計
- **🔧 充実のミドルウェア**: CORS、ロガー、認証など標準装備

### ユースケース

- REST API
- サーバーレスバックエンド
- エッジ関数
- Webhook ハンドラー
- リバースプロキシ
- API ゲートウェイ

## 技術スタック

- **Hono 4**: 超高速 Web フレームワーク
- **Cloudflare Workers**: エッジコンピューティングプラットフォーム
- **Wrangler 3**: Cloudflare 公式開発ツール
- **Vitest 2**: 高速テストランナー (Workers Pool 対応)
- **TypeScript 5**: 完全型安全

### Cloudflare 統合可能サービス

- **KV**: Key-Value ストレージ
- **D1**: SQLite データベース
- **R2**: オブジェクトストレージ (S3 互換)
- **Durable Objects**: ステートフル処理
- **Queues**: メッセージキュー
- **Pages**: 静的サイトホスティング

## プロジェクト構成

```
hono-cloudflare/
├── wrangler.toml              # Wrangler設定ファイル
├── package.json               # 依存関係
├── tsconfig.json              # TypeScript設定
├── vitest.config.ts           # テスト設定
├── .node-version              # Node.js 22
└── src/
    ├── index.ts               # エントリーポイント
    ├── routes/
    │   ├── api.ts             # APIルートのルート
    │   ├── users.ts           # ユーザーAPI
    │   └── posts.ts           # 投稿API
    ├── middleware/
    │   └── errorHandler.ts    # エラーハンドリング
    └── test/
        └── index.test.ts      # APIテスト
```

## セットアップ

### 前提条件

- Node.js 22 以上
- Cloudflare アカウント (デプロイ時)
- Wrangler CLI

### 初回セットアップ

1. **依存関係のインストール**

```powershell
cd hono-cloudflare
npm install
```

2. **Wrangler にログイン** (デプロイ時のみ)

```powershell
npx wrangler login
```

3. **開発サーバー起動**

```powershell
npm run dev
```

ブラウザで http://localhost:8787 にアクセス

## 開発

### ローカル開発

```powershell
# 開発サーバー起動 (ホットリロード対応)
npm run dev

# 型定義生成
npm run cf-typegen
```

### API エンドポイント

#### ルート

- `GET /` - Welcome メッセージ
- `GET /health` - ヘルスチェック
- `GET /api` - API 情報

#### ユーザー API

- `GET /api/users` - 全ユーザー取得
- `GET /api/users/:id` - 特定ユーザー取得
- `POST /api/users` - ユーザー作成
- `PUT /api/users/:id` - ユーザー更新
- `DELETE /api/users/:id` - ユーザー削除

#### 投稿 API

- `GET /api/posts` - 全投稿取得 (クエリ: `?published=true`)
- `GET /api/posts/:id` - 特定投稿取得
- `POST /api/posts` - 投稿作成

### リクエスト例

```powershell
# 全ユーザー取得
curl http://localhost:8787/api/users

# ユーザー作成
curl -X POST http://localhost:8787/api/users `
  -H "Content-Type: application/json" `
  -d '{"name":"John Doe","email":"john@example.com"}'

# 公開済み投稿のみ取得
curl http://localhost:8787/api/posts?published=true
```

## テスト

### Vitest + Cloudflare Workers Pool

```powershell
# テスト実行
npm test

# UIモード
npm run test:ui

# カバレッジ
npm run test:coverage
```

### テスト例

```typescript
import { describe, it, expect } from 'vitest'
import app from '../index'

describe('API Tests', () => {
  it('should return users', async () => {
    const res = await app.request('/api/users')
    expect(res.status).toBe(200)

    const data = await res.json()
    expect(data.users).toBeInstanceOf(Array)
  })
})
```

## デプロイ

### Cloudflare Workers へのデプロイ

```powershell
# 本番デプロイ
npm run deploy

# プレビューデプロイ
npx wrangler deploy --dry-run
```

デプロイ後の URL 例: `https://hono-cloudflare-workers.<your-subdomain>.workers.dev`

### デプロイ設定

`wrangler.toml` で設定を調整:

```toml
name = "your-app-name"
main = "src/index.ts"
compatibility_date = "2024-12-01"

[vars]
ENVIRONMENT = "production"
```

### カスタムドメイン設定

Cloudflare ダッシュボードから:

1. Workers & Pages → あなたの Worker
2. Settings → Triggers → Custom Domains
3. ドメインを追加

## Cloudflare サービス統合

### KV (Key-Value ストレージ)

```powershell
# KV Namespace作成
npx wrangler kv:namespace create "MY_KV"
```

`wrangler.toml`:

```toml
[[kv_namespaces]]
binding = "MY_KV"
id = "your-kv-namespace-id"
```

使用例:

```typescript
app.get('/kv-test', async (c) => {
  await c.env.MY_KV.put('key', 'value')
  const value = await c.env.MY_KV.get('key')
  return c.json({ value })
})
```

### D1 (SQLite データベース)

```powershell
# D1データベース作成
npx wrangler d1 create my-database
```

`wrangler.toml`:

```toml
[[d1_databases]]
binding = "DB"
database_name = "my-database"
database_id = "your-database-id"
```

使用例:

```typescript
app.get('/db-test', async (c) => {
  const result = await c.env.DB.prepare('SELECT * FROM users').all()
  return c.json(result)
})
```

### R2 (オブジェクトストレージ)

```powershell
# R2バケット作成
npx wrangler r2 bucket create my-bucket
```

`wrangler.toml`:

```toml
[[r2_buckets]]
binding = "MY_BUCKET"
bucket_name = "my-bucket"
```

使用例:

```typescript
app.post('/upload', async (c) => {
  const body = await c.req.arrayBuffer()
  await c.env.MY_BUCKET.put('file.txt', body)
  return c.json({ message: 'Uploaded' })
})
```

### Durable Objects (ステートフル処理)

WebSocket やリアルタイム処理に最適:

```typescript
export class Counter {
  state: DurableObjectState
  value = 0

  constructor(state: DurableObjectState) {
    this.state = state
  }

  async fetch(request: Request) {
    this.value++
    return new Response(String(this.value))
  }
}
```

## パフォーマンス

### ベンチマーク結果

Hono は以下のフレームワークより高速:

| フレームワーク | リクエスト/秒 | 相対速度 |
| -------------- | ------------- | -------- |
| Hono           | 38,000        | 1.0x     |
| Express        | 12,000        | 0.32x    |
| Fastify        | 25,000        | 0.66x    |

### 最適化ヒント

1. **ミドルウェアの最小化**: 必要なものだけ使用
2. **KV/D1 の活用**: インメモリストレージの代わりに永続化
3. **キャッシュ戦略**: Cache API を活用
4. **圧縮**: レスポンス圧縮を有効化

```typescript
import { compress } from 'hono/compress'
app.use('*', compress())
```

## トラブルシューティング

### ローカル開発でポート競合

```powershell
# ポート変更
npx wrangler dev --port 8788
```

### バインディングが見つからない

```powershell
# 型定義を再生成
npm run cf-typegen
```

### デプロイエラー

```powershell
# Wranglerを最新版に更新
npm install wrangler@latest

# ログイン状態を確認
npx wrangler whoami
```

### CORS エラー

```typescript
// より詳細なCORS設定
app.use(
  '*',
  cors({
    origin: ['https://yourdomain.com'],
    allowMethods: ['GET', 'POST', 'PUT', 'DELETE'],
    credentials: true
  })
)
```

### Workers Bundle Size 制限

- 無料プラン: 1MB
- 有料プラン: 10MB

大きなライブラリは避け、必要最小限の依存関係に:

```powershell
# バンドルサイズ確認
npx wrangler deploy --dry-run --outdir=dist
```

## マイグレーションガイド

### Express から移行

```typescript
// Express
app.get('/users/:id', (req, res) => {
  res.json({ id: req.params.id })
})

// Hono
app.get('/users/:id', (c) => {
  return c.json({ id: c.req.param('id') })
})
```

### Fastify から移行

```typescript
// Fastify
fastify.get('/users', async (request, reply) => {
  return { users: [] }
})

// Hono
app.get('/users', (c) => {
  return c.json({ users: [] })
})
```

## 参考リンク

- [Hono 公式ドキュメント](https://hono.dev/)
- [Cloudflare Workers 公式](https://developers.cloudflare.com/workers/)
- [Wrangler CLI](https://developers.cloudflare.com/workers/wrangler/)
- [Cloudflare D1](https://developers.cloudflare.com/d1/)
- [Cloudflare KV](https://developers.cloudflare.com/kv/)
- [Cloudflare R2](https://developers.cloudflare.com/r2/)

## ライセンス

MIT
