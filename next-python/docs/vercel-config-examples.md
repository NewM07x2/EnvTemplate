# Vercel デプロイ設定例

このドキュメントは、Vercel にデプロイする際に使用できる設定ファイルの例を示します。

## vercel.json の設定例

プロジェクトルートに `vercel.json` を作成して、Vercel のビルド・デプロイ設定を指定します。

```json
{
  "buildCommand": "npx prisma generate && npm run build",
  "outputDirectory": ".next",
  "devCommand": "npm run dev",
  "cleanUrls": true,
  "trailingSlash": false,
  "env": {
    "NODE_ENV": "production"
  },
  "regions": ["nrt1"],
  "functions": {
    "src/app/api/**": {
      "memory": 1024,
      "maxDuration": 60
    }
  },
  "redirects": [
    {
      "source": "/old-page",
      "destination": "/new-page",
      "permanent": true
    }
  ],
  "rewrites": [
    {
      "source": "/api/:path*",
      "destination": "https://api.example.com/:path*"
    }
  ],
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        {
          "key": "X-Content-Type-Options",
          "value": "nosniff"
        },
        {
          "key": "X-Frame-Options",
          "value": "SAMEORIGIN"
        },
        {
          "key": "X-XSS-Protection",
          "value": "1; mode=block"
        }
      ]
    }
  ]
}
```

## next.config.mjs の設定例

```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  // 画像最適化
  images: {
    domains: ['example.com', 'cdn.example.com'],
    formats: ['image/avif', 'image/webp'],
    remotePatterns: [
      {
        protocol: 'https',
        hostname: '**.example.com',
      },
    ],
  },

  // セキュリティヘッダー
  async headers() {
    return [
      {
        source: '/:path*',
        headers: [
          {
            key: 'X-Content-Type-Options',
            value: 'nosniff',
          },
          {
            key: 'X-Frame-Options',
            value: 'SAMEORIGIN',
          },
          {
            key: 'X-XSS-Protection',
            value: '1; mode=block',
          },
          {
            key: 'Referrer-Policy',
            value: 'strict-origin-when-cross-origin',
          },
        ],
      },
    ]
  },

  // リダイレクト
  async redirects() {
    return [
      {
        source: '/old-page',
        destination: '/new-page',
        permanent: true,
      },
    ]
  },

  // URL リライト
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'https://api.example.com/:path*',
      },
    ]
  },

  // 環境変数
  env: {
    NEXT_PUBLIC_GRAPHQL_ENDPOINT: process.env.NEXT_PUBLIC_GRAPHQL_ENDPOINT,
  },

  // Swashbuckle 最適化
  swcMinify: true,

  // 本番環境での最適化
  poweredByHeader: false,

  // TypeScript チェック
  typescript: {
    tsconfigPath: './tsconfig.json',
  },

  // ESLint チェック
  eslint: {
    dirs: ['src'],
  },

  // WebP サポート
  webpackDevMiddleware: (config) => {
    return config
  },
}

export default nextConfig
```

## .env.production の設定例

```env
# 本番環境専用環境変数
NODE_ENV=production

# Database
DATABASE_URL=postgresql://prod_user:prod_password@prod-host.example.com:5432/prod_db

# GraphQL Endpoint
NEXT_PUBLIC_GRAPHQL_ENDPOINT=https://api.example.com/graphql

# API URL
NEXT_PUBLIC_API_URL=https://api.example.com

# Sentry (オプション)
NEXT_PUBLIC_SENTRY_DSN=https://key@sentry.io/project

# Analytics (オプション)
NEXT_PUBLIC_GA_ID=G-XXXXXXXXXX
```

## GitHub Actions での CI/CD 設定例

`.github/workflows/deploy.yml`:

```yaml
name: Deploy to Vercel

on:
  push:
    branches:
      - main

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'

      - name: Install dependencies
        run: npm ci

      - name: Run tests
        run: npm run test

      - name: Lint
        run: npm run lint

      - name: Deploy to Vercel
        uses: vercel/action@master
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
          production: true
```

## Dockerfile の設定例（ローカルテスト用）

```dockerfile
FROM node:18-alpine

WORKDIR /app

# 依存関係をコピー
COPY package.json package-lock.json ./
RUN npm ci

# ソースコードをコピー
COPY . .

# Prisma Client を生成
RUN npx prisma generate

# Next.js をビルド
RUN npm run build

# 本番環境で実行
CMD ["npm", "start"]

EXPOSE 3000
```

## 本番環境デプロイ チェックリスト

デプロイ前に以下を確認してください：

```
✓ 環境変数が全て設定されているか
✓ DATABASE_URL が本番 DB を指しているか
✓ NEXT_PUBLIC_GRAPHQL_ENDPOINT が本番エンドポイントか
✓ ローカルでビルドが成功するか (npm run build)
✓ ローカルで本番サーバーが正常に起動するか (npm start)
✓ テストが全て通っているか (npm run test)
✓ Lint エラーがないか (npm run lint)
✓ Prisma マイグレーションが最新か
✓ git main ブランチが最新か
✓ .env ファイルが .gitignore に含まれているか
```

## トラブルシューティング

### ビルド失敗時

1. ローカルで再現:
   ```bash
   npm ci
   npm run build
   ```

2. ログを確認:
   ```bash
   vercel logs -f
   ```

3. キャッシュをクリア:
   ```bash
   vercel env pull
   npm ci --no-fund --no-audit
   npm run build
   ```

### 環境変数が反映されない

1. Vercel ダッシュボード → Settings → Environment Variables で確認
2. 環境を選択し直す（Production / Preview）
3. デプロイを再実行

```bash
vercel --prod --force
```

### Cold Start 時間が長い

- バンドルサイズを削減
- 不要な API を削除
- Serverless Function を最適化

```bash
# バンドルサイズを確認
npm install -g webpack-bundle-analyzer
npm run analyze
```

## 参考資料

- [Vercel 公式ドキュメント](https://vercel.com/docs)
- [Next.js ビルド設定](https://nextjs.org/docs/api-reference/next-config-js)
- [Vercel CLI リファレンス](https://vercel.com/docs/cli)
