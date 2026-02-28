# Hono + Cloudflare Workers ガイド

> **対象者**: Cloudflare Workers・Hono を初めて使う開発者  
> **関連テンプレート**: `hono-cloudflare/`  
> **所要時間**: 約 40 分

---

## 📚 目次

1. [Hono と Cloudflare Workers とは](#1-hono-と-cloudflare-workers-とは)
2. [環境構築](#2-環境構築)
3. [テンプレートの構造](#3-テンプレートの構造)
4. [ルーティングとハンドラー](#4-ルーティングとハンドラー)
5. [ミドルウェア](#5-ミドルウェア)
6. [Cloudflare バインディング](#6-cloudflare-バインディング)
7. [環境変数（wrangler.toml）](#7-環境変数wranglertoml)
8. [デプロイ](#8-デプロイ)
9. [よく使うコマンド](#9-よく使うコマンド)

---

## 1. Hono と Cloudflare Workers とは

### Hono

**Hono**（炎）は超軽量・超高速な TypeScript Web フレームワークです。

```
特徴:
  ✅ バンドルサイズが極小（5KB 以下）
  ✅ Edge 環境（Cloudflare Workers / Deno Deploy）で動く
  ✅ Express に近い直感的な API
  ✅ TypeScript ファースト
  ✅ バリデーション・JWT 等のミドルウェアが充実
```

### Cloudflare Workers

**Cloudflare Workers** は Cloudflare の CDN エッジ上で動く**サーバーレス実行環境**です。

```
特徴:
  ✅ 世界 200+ 拠点のエッジで実行 → 超低レイテンシ
  ✅ コールドスタートなし（起動が瞬時）
  ✅ 無料枠: 10 万リクエスト / 日
  ✅ KV（キーバリューストア）・D1（SQLite）・R2（オブジェクトストレージ）が使える
```

### 従来のサーバーとの違い

```
従来のサーバー（EC2 / ECS 等）:
  リクエスト → [サーバー（東京）] → レスポンス
  距離が遠いとレイテンシが高い

Cloudflare Workers:
  リクエスト → [最寄りのエッジ（200+ 拠点）] → レスポンス
  常にユーザーの近くで実行されるため超高速
```

---

## 2. 環境構築

```bash
# Node.js 18 以上が必要
node --version

# 依存関係をインストール
cd hono-cloudflare
npm install

# Cloudflare CLI（wrangler）をグローバルインストール
npm install -g wrangler

# Cloudflare にログイン（デプロイ時に必要）
wrangler login
```

---

## 3. テンプレートの構造

```
hono-cloudflare/
├── src/
│   ├── index.ts          ← エントリポイント・ミドルウェア設定
│   ├── routes/
│   │   ├── api.ts        ← API ルートのまとめ
│   │   ├── users.ts      ← ユーザー関連のルート
│   │   └── posts.ts      ← 投稿関連のルート
│   ├── middleware/
│   │   └── errorHandler.ts ← グローバルエラーハンドラー
│   └── test/             ← テストコード
├── wrangler.toml         ← Cloudflare Workers の設定ファイル
├── tsconfig.json
├── vitest.config.ts
└── package.json
```

---

## 4. ルーティングとハンドラー

### 基本的なルーティング

```typescript
import { Hono } from 'hono'

const app = new Hono()

// GET
app.get('/users', (c) => {
  return c.json({ users: [] })
})

// POST
app.post('/users', async (c) => {
  const body = await c.req.json()
  return c.json({ created: body }, 201)
})

// パスパラメータ
app.get('/users/:id', (c) => {
  const id = c.req.param('id')
  return c.json({ id })
})

// クエリパラメータ
app.get('/search', (c) => {
  const q = c.req.query('q')
  const page = Number(c.req.query('page') ?? '1')
  return c.json({ q, page })
})
```

### サブルートでの構成（このテンプレートの書き方）

```typescript
// src/routes/users.ts
import { Hono } from 'hono'

const users = new Hono()

users.get('/', (c) => c.json({ users: [] }))
users.get('/:id', (c) => c.json({ id: c.req.param('id') }))
users.post('/', async (c) => {
  const body = await c.req.json()
  return c.json(body, 201)
})

export default users


// src/routes/api.ts
import { Hono } from 'hono'
import usersRoutes from './users'
import postsRoutes from './posts'

const api = new Hono()
api.route('/users', usersRoutes)   // → /api/users
api.route('/posts', postsRoutes)   // → /api/posts

export default api


// src/index.ts
import { Hono } from 'hono'
import apiRoutes from './routes/api'

const app = new Hono()
app.route('/api', apiRoutes)       // → /api/users, /api/posts

export default app
```

### レスポンスの種類

```typescript
// JSON レスポンス
return c.json({ message: 'OK' })
return c.json({ error: 'Not Found' }, 404)

// テキスト
return c.text('Hello World')

// リダイレクト
return c.redirect('https://example.com')

// カスタムヘッダー
return new Response('OK', {
  status: 200,
  headers: { 'X-Custom-Header': 'value' },
})
```

---

## 5. ミドルウェア

```typescript
import { Hono } from 'hono'
import { cors } from 'hono/cors'
import { logger } from 'hono/logger'
import { prettyJSON } from 'hono/pretty-json'
import { jwt } from 'hono/jwt'
import { rateLimiter } from 'hono/rate-limiter'

const app = new Hono()

// ログ出力
app.use('*', logger())

// JSON を整形して出力（開発用）
app.use('*', prettyJSON())

// CORS 設定
app.use('*', cors({
  origin: ['http://localhost:3000', 'https://example.com'],
  allowMethods: ['GET', 'POST', 'PUT', 'DELETE'],
}))

// JWT 認証（特定ルートのみ）
app.use('/api/protected/*', jwt({ secret: 'my-secret-key' }))

// カスタムミドルウェア（リクエストログ）
app.use('*', async (c, next) => {
  console.log(`${c.req.method} ${c.req.url}`)
  await next()
})

// グローバルエラーハンドラー
app.onError((err, c) => {
  console.error(err)
  return c.json({ error: err.message }, 500)
})
```

### Zod でのバリデーション

```typescript
import { zValidator } from '@hono/zod-validator'
import { z } from 'zod'

const createUserSchema = z.object({
  email: z.string().email(),
  username: z.string().min(1).max(50),
  password: z.string().min(8),
})

app.post(
  '/users',
  zValidator('json', createUserSchema),  // バリデーション失敗時は 400 を返す
  async (c) => {
    const body = c.req.valid('json')     // 型安全なボディ
    // body.email, body.username, body.password が型推論される
    return c.json({ created: body }, 201)
  }
)
```

---

## 6. Cloudflare バインディング

### KV（キーバリューストア）

```typescript
type Bindings = {
  MY_KV: KVNamespace
}

const app = new Hono<{ Bindings: Bindings }>()

app.get('/cache/:key', async (c) => {
  const value = await c.env.MY_KV.get(c.req.param('key'))
  if (!value) return c.json({ error: 'Not Found' }, 404)
  return c.json({ value })
})

app.put('/cache/:key', async (c) => {
  const { value } = await c.req.json()
  await c.env.MY_KV.put(c.req.param('key'), value, {
    expirationTtl: 3600,  // 1 時間で有効期限切れ
  })
  return c.json({ ok: true })
})
```

### D1（SQLite データベース）

```typescript
type Bindings = {
  DB: D1Database
}

const app = new Hono<{ Bindings: Bindings }>()

app.get('/users', async (c) => {
  const { results } = await c.env.DB.prepare(
    'SELECT id, email, username FROM users LIMIT 100'
  ).all()
  return c.json({ users: results })
})

app.post('/users', async (c) => {
  const { email, username } = await c.req.json()
  const result = await c.env.DB.prepare(
    'INSERT INTO users (id, email, username) VALUES (?, ?, ?)'
  ).bind(crypto.randomUUID(), email, username).run()
  return c.json({ success: result.success }, 201)
})
```

### R2（オブジェクトストレージ）

```typescript
type Bindings = {
  MY_BUCKET: R2Bucket
}

app.post('/upload', async (c) => {
  const formData = await c.req.formData()
  const file = formData.get('file') as File
  
  await c.env.MY_BUCKET.put(file.name, file.stream(), {
    httpMetadata: { contentType: file.type },
  })
  
  return c.json({ filename: file.name })
})
```

---

## 7. 環境変数（wrangler.toml）

```toml
# wrangler.toml
name = "hono-cloudflare-workers"
main = "src/index.ts"
compatibility_date = "2024-12-01"

# 静的な環境変数（コードで c.env.ENVIRONMENT として参照）
[vars]
ENVIRONMENT = "development"
APP_NAME = "My API"

# KV バインディング（Cloudflare ダッシュボードで作成後に ID を設定）
[[kv_namespaces]]
binding = "MY_KV"
id = "your-kv-namespace-id"

# D1 データベース
[[d1_databases]]
binding = "DB"
database_name = "my-database"
database_id = "your-database-id"

# 本番環境の設定
[env.production.vars]
ENVIRONMENT = "production"
```

**シークレット（機密情報）は `wrangler secret` で登録：**

```bash
# シークレットを登録（対話型で値を入力）
wrangler secret put JWT_SECRET

# シークレットの一覧
wrangler secret list
```

---

## 8. デプロイ

```bash
# ローカルで開発サーバー起動
npm run dev
# → http://localhost:8787

# Cloudflare Workers にデプロイ
npm run deploy
# = wrangler deploy

# プレビュー（本番デプロイ前の確認）
wrangler deploy --dry-run

# デプロイ済みのログを確認
wrangler tail
```

---

## 9. よく使うコマンド

```bash
# 開発サーバー起動（ホットリロード付き）
npm run dev

# テスト実行
npm test

# 型チェック
npx tsc --noEmit

# デプロイ
npm run deploy

# シークレット管理
wrangler secret put SECRET_NAME    # 追加
wrangler secret list               # 一覧
wrangler secret delete SECRET_NAME # 削除

# KV を操作（ローカル）
wrangler kv key put --binding MY_KV "key" "value"
wrangler kv key get --binding MY_KV "key"

# D1 を操作
wrangler d1 execute DB --local --command "SELECT * FROM users"
```

---

## 📌 まとめ

| 概念 | Hono | Express |
|------|------|---------|
| インスタンス作成 | `new Hono()` | `express()` |
| ルーティング | `app.get('/path', handler)` | `app.get('/path', handler)` |
| JSON レスポンス | `c.json(data)` | `res.json(data)` |
| パスパラメータ | `c.req.param('id')` | `req.params.id` |
| クエリパラメータ | `c.req.query('q')` | `req.query.q` |
| リクエストボディ | `await c.req.json()` | `req.body` |
| 環境変数 | `c.env.MY_VAR` | `process.env.MY_VAR` |

**Hono + Cloudflare Workers が向いているケース：**
- グローバルに低レイテンシな API が必要
- サーバーレスでスケーリングをゼロコストにしたい
- BFF（Backend for Frontend）として Next.js と組み合わせる
