# Hono + Cloudflare Workers ディレクトリ構造

```
hono-cloudflare/
├── wrangler.toml              # Wrangler設定 (Workers環境、バインディング設定)
├── package.json               # 依存関係・スクリプト定義
├── tsconfig.json              # TypeScript設定 (ESNext、Workers types)
├── vitest.config.ts           # Vitest設定 (Workers Pool使用)
├── .gitignore                 # Git除外ファイル (.wrangler, dist等)
├── .node-version              # Node.js 22
├── .dev.vars                  # ローカル環境変数 (Gitにコミットしない)
├── README.md                  # プロジェクト説明書
└── src/
    ├── index.ts               # アプリケーションエントリーポイント
    │                          # - Honoインスタンス作成
    │                          # - ミドルウェア設定 (cors, logger, prettyJSON)
    │                          # - ルート定義 (/, /health, /api)
    │                          # - エラーハンドリング
    │
    ├── routes/                # ルート定義ディレクトリ
    │   ├── api.ts             # APIルートのルート (/api)
    │   │                      # - サブルートの集約 (users, posts)
    │   │
    │   ├── users.ts           # ユーザーAPI (/api/users)
    │   │                      # - GET /api/users (全ユーザー取得)
    │   │                      # - GET /api/users/:id (特定ユーザー取得)
    │   │                      # - POST /api/users (ユーザー作成)
    │   │                      # - PUT /api/users/:id (ユーザー更新)
    │   │                      # - DELETE /api/users/:id (ユーザー削除)
    │   │                      # ※現在はインメモリ、本番ではKV/D1使用推奨
    │   │
    │   └── posts.ts           # 投稿API (/api/posts)
    │                          # - GET /api/posts (全投稿取得、published絞り込み可)
    │                          # - GET /api/posts/:id (特定投稿取得)
    │                          # - POST /api/posts (投稿作成)
    │
    ├── middleware/            # カスタムミドルウェア
    │   └── errorHandler.ts    # グローバルエラーハンドリング
    │                          # - 404, 401, 403, 500エラーの統一処理
    │
    └── test/                  # テストファイル
        └── index.test.ts      # APIテスト (Vitest + Workers Pool)
                               # - ルートテスト (/health等)
                               # - ユーザーAPIテスト (CRUD)
                               # - 投稿APIテスト (CRUD、フィルタリング)
```

## ファイルの役割

### 設定ファイル

- **wrangler.toml**: Cloudflare Workers の設定ファイル

  - `name`: Worker 名 (デプロイ時の URL 決定)
  - `main`: エントリーポイント指定
  - `compatibility_date`: Workers API バージョン
  - `vars`: 環境変数定義
  - バインディング設定 (KV, D1, R2, Durable Objects 等)

- **tsconfig.json**: TypeScript 設定

  - `target: ES2022`: 最新 JavaScript 機能使用
  - `types`: Cloudflare Workers 型定義
  - `jsxImportSource: "hono/jsx"`: Hono の JSX 使用

- **vitest.config.ts**: テスト設定
  - `@cloudflare/vitest-pool-workers`: Workers 環境でテスト実行
  - `wrangler.toml`と連携してバインディングをモック

### ソースコード

- **src/index.ts**: アプリケーションのエントリーポイント

  - Hono インスタンス作成 (型付き Bindings)
  - ミドルウェアチェーン設定
  - ルーティング定義
  - エラーハンドリング

- **src/routes/**: ルート定義 (モジュール分割)

  - 各ルートが独立した Hono インスタンスを持つ
  - `app.route('/path', routeModule)` でマウント
  - RESTful API 設計

- **src/middleware/**: カスタムミドルウェア
  - エラーハンドリング
  - 認証・認可 (将来追加)
  - レート制限 (将来追加)

## アーキテクチャ特徴

### エッジコンピューティング

Cloudflare Workers はユーザーに最も近いエッジロケーションで実行されるため:

- **低レイテンシ**: 世界中どこからでも 50ms 以下
- **高スループット**: 自動スケーリング
- **コールドスタート 0ms**: 常時起動状態

### Hono の利点

1. **超軽量**: バンドルサイズが小さく、Workers 制限内に収まる
2. **マルチランタイム**: Cloudflare/Deno/Bun/Node.js 対応
3. **高速**: ルーティングが最適化されている
4. **DX**: Express ライクな直感的 API

### データストレージ戦略

現在のテンプレートはインメモリストレージですが、本番では以下を使用:

| ユースケース       | 推奨サービス              |
| ------------------ | ------------------------- |
| Key-Value          | KV (グローバルキャッシュ) |
| リレーショナル DB  | D1 (SQLite)               |
| ファイルストレージ | R2 (S3 互換)              |
| ステートフル処理   | Durable Objects           |
| メッセージキュー   | Queues                    |

### ミドルウェアチェーン

Hono のミドルウェアは順番に実行される:

```typescript
app.use('*', logger()) // 1. リクエストログ
app.use('*', prettyJSON()) // 2. JSONフォーマット
app.use('*', cors()) // 3. CORS設定
// ... ルート処理 ...
app.onError(errorHandler) // 4. エラーハンドリング
```

### ルーティング階層

```
/                    → Welcome メッセージ
/health              → ヘルスチェック
/api                 → API情報
  /users             → ユーザーAPI
    /               → 全ユーザー (GET)
    /:id            → 特定ユーザー (GET/PUT/DELETE)
  /posts            → 投稿API
    /               → 全投稿 (GET/POST)
    /:id            → 特定投稿 (GET)
```

## 開発フロー

1. **ローカル開発**: `npm run dev` で Wrangler Dev Server 起動
2. **テスト**: `npm test` で Vitest + Workers Pool 実行
3. **型チェック**: `tsc --noEmit` で TypeScript エラー確認
4. **デプロイ**: `npm run deploy` で Cloudflare にデプロイ

## Cloudflare バインディング拡張例

### KV Namespace 追加

```toml
# wrangler.toml
[[kv_namespaces]]
binding = "MY_KV"
id = "your-kv-namespace-id"
```

```typescript
// src/index.ts (型定義)
type Bindings = {
  MY_KV: KVNamespace
}

// 使用例
app.get('/cache', async (c) => {
  await c.env.MY_KV.put('key', 'value')
  const value = await c.env.MY_KV.get('key')
  return c.json({ value })
})
```

### D1 Database 追加

```toml
# wrangler.toml
[[d1_databases]]
binding = "DB"
database_name = "my-db"
database_id = "your-db-id"
```

```typescript
// 型定義
type Bindings = {
  DB: D1Database
}

// 使用例
app.get('/users-db', async (c) => {
  const result = await c.env.DB.prepare('SELECT * FROM users').all()
  return c.json(result)
})
```

このアーキテクチャにより、スケーラブルでメンテナンス性の高いエッジ API を構築できます。
