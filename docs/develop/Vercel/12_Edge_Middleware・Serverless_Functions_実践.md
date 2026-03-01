# Vercel Edge Middleware・Serverless Functions 実践

> **対象者**: Edge Network を活用した高度な機能実装を目指す開発者  
> **主要トピック**: Edge Middleware 高度な使用 / Cold Start 削減 / Streaming / Function 最適化

---

## 📚 目次

1. [Edge Middleware 高度な使用例](#1-edge-middleware-高度な使用例)
2. [Geo-Routing と地域別対応](#2-geo-routing-と地域別対応)
3. [A/B Testing 環境構築](#3-ab-testing-環境構築)
4. [Bot 検知・セキュリティ](#4-bot-検知セキュリティ)
5. [Cold Start 削減](#5-cold-start-削減)
6. [Function サイズ最適化](#6-function-サイズ最適化)
7. [Streaming Responses](#7-streaming-responses)
8. [実装パフォーマンスチューニング](#8-実装パフォーマンスチューニング)

---

## 1. Edge Middleware 高度な使用例

### 1.1 リクエスト変換・フィルタリング

```typescript
// middleware.ts
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  const response = NextResponse.next();

  // 1. リクエストヘッダー追加
  const requestHeaders = new Headers(request.headers);
  requestHeaders.set('x-pathname', request.nextUrl.pathname);
  requestHeaders.set('x-request-time', new Date().toISOString());

  // 2. カスタムヘッダー値取得
  const userAgent = request.headers.get('user-agent') || '';
  const country = request.geo?.country || 'unknown';

  // 3. レスポンスヘッダー追加
  response.headers.set('x-served-by', 'vercel-edge');
  response.headers.set('x-response-time', Date.now().toString());

  // 4. セキュリティヘッダー
  response.headers.set('X-Content-Type-Options', 'nosniff');
  response.headers.set('X-Frame-Options', 'DENY');
  response.headers.set('Strict-Transport-Security', 'max-age=31536000');

  return response;
}

export const config = {
  matcher: [
    // マッチャー設定
    '/((?!_next|static|favicon.ico).*)',
  ],
};
```

### 1.2 Request キャッシング（前処理）

```typescript
// middleware.ts - Conditional Caching
export function middleware(request: NextRequest) {
  // キャッシュ対象フォルダを判定
  if (request.nextUrl.pathname.startsWith('/api/')) {
    // API は Cache-Control で制御
    return NextResponse.next();
  }

  if (request.nextUrl.pathname.startsWith('/static/')) {
    // 静的ファイルは 1 年キャッシュ
    const response = NextResponse.next();
    response.headers.set(
      'Cache-Control',
      'public, max-age=31536000, immutable'
    );
    return response;
  }

  return NextResponse.next();
}
```

### 1.3 認証・認可（Edge で検証）

```typescript
// middleware.ts - JWT Validation at Edge
import { jwtVerify } from 'jose';

const secret = new TextEncoder().encode(process.env.JWT_SECRET || 'secret');

async function verifyAuth(request: NextRequest) {
  const token = request.cookies.get('token')?.value;

  if (!token) {
    return null;
  }

  try {
    const verified = await jwtVerify(token, secret);
    return verified.payload;
  } catch {
    return null;
  }
}

export async function middleware(request: NextRequest) {
  // 保護されたルート
  if (request.nextUrl.pathname.startsWith('/api/protected')) {
    const payload = await verifyAuth(request);

    if (!payload) {
      return new NextResponse(JSON.stringify({ error: 'Unauthorized' }), {
        status: 401,
        headers: { 'Content-Type': 'application/json' },
      });
    }

    // リクエストに user 情報を追加
    const requestHeaders = new Headers(request.headers);
    requestHeaders.set('x-user-id', payload.sub as string);

    return NextResponse.next({
      request: {
        headers: requestHeaders,
      },
    });
  }

  return NextResponse.next();
}

export const config = {
  matcher: ['/api/protected/:path*'],
};
```

---

## 2. Geo-Routing と地域別対応

### 2.1 国別ルーティング

```typescript
// middleware.ts - Geo-based Routing
import { NextResponse } from 'next/server';

export function middleware(request: NextRequest) {
  const country = request.geo?.country;

  // 日本からのアクセス
  if (country === 'JP') {
    return NextResponse.rewrite(new URL('/ja', request.url));
  }

  // 中国からのアクセス（特別対応）
  if (country === 'CN') {
    // 異なるコンテンツ提供
    return NextResponse.rewrite(new URL('/cn', request.url));
  }

  // EU（GDPR）向け
  if (['DE', 'FR', 'GB', 'IT', 'ES'].includes(country || '')) {
    // Cookie バナー表示
    const response = NextResponse.next();
    response.headers.set('x-show-gdpr-banner', 'true');
    return response;
  }

  return NextResponse.next();
}

export const config = {
  matcher: ['/:path*'],
};
```

### 2.2 リージョン別コンテンツ配信

```typescript
// middleware.ts - Content Variant by Region
export function middleware(request: NextRequest) {
  const country = request.geo?.country;
  const pathname = request.nextUrl.pathname;

  // /api/content → /api/content/ja に自動リライト
  if (pathname === '/api/content') {
    const regionPath = `/api/content/${country?.toLowerCase() || 'default'}`;
    return NextResponse.rewrite(new URL(regionPath, request.url));
  }

  return NextResponse.next();
}
```

### 2.3 リージョン別キャッシュ戦略

```typescript
// middleware.ts - Region-specific Caching
export function middleware(request: NextRequest) {
  const response = NextResponse.next();
  const country = request.geo?.country;

  // 地域によってキャッシュ戦略を変更
  if (['JP', 'KR', 'CN'].includes(country || '')) {
    // アジア向け：短めのキャッシュ（コンテンツ更新頻繁）
    response.headers.set('Cache-Control', 'public, max-age=3600');
  } else {
    // その他：長めのキャッシュ
    response.headers.set('Cache-Control', 'public, max-age=86400');
  }

  return response;
}
```

---

## 3. A/B Testing 環境構築

### 3.1 Cookie ベース実装

```typescript
// middleware.ts - A/B Test using Cookies
import { NextResponse } from 'next/server';

export function middleware(request: NextRequest) {
  let testVariant = request.cookies.get('ab-test')?.value;

  // テスト variant がない場合、ランダムに割り当て
  if (!testVariant) {
    testVariant = Math.random() > 0.5 ? 'control' : 'variant';
  }

  // テスト variant に応じてコンテンツを変更
  if (testVariant === 'variant') {
    // Variant A を提供
    const response = NextResponse.rewrite(new URL('/ab/variant-a', request.url));
    response.cookies.set('ab-test', 'variant', { maxAge: 30 * 24 * 60 * 60 });
    return response;
  } else {
    // Control (元々のコンテンツ)
    const response = NextResponse.next();
    response.cookies.set('ab-test', 'control', { maxAge: 30 * 24 * 60 * 60 });
    return response;
  }
}
```

### 3.2 URL パラメータベース

```typescript
// middleware.ts - A/B Test via URL
export function middleware(request: NextRequest) {
  const testParam = request.nextUrl.searchParams.get('ab-test');

  if (testParam === 'variant-b') {
    // Variant B の実験的機能を有効化
    const response = NextResponse.next();
    response.headers.set('x-ab-variant', 'b');
    response.headers.set('x-feature-beta', 'enabled');
    return response;
  }

  return NextResponse.next();
}
```

### 3.3 キャッシュキー分割

```typescript
// middleware.ts - A/B Testing with Vary Header
export function middleware(request: NextRequest) {
  const variant = request.cookies.get('ab-test')?.value || 'control';

  const response = NextResponse.next();

  // Vary ヘッダーで Cookie ベースのキャッシュ分割
  response.headers.set('Vary', 'Cookie');

  // カスタム ヘッダー（キャッシュキー構成）
  response.headers.set('x-ab-variant', variant);

  // キャッシュ制御（テスト期間は短め）
  response.headers.set('Cache-Control', 'public, max-age=300');

  return response;
}
```

---

## 4. Bot 検知・セキュリティ

### 4.1 ユーザーエージェント検査

```typescript
// middleware.ts - Bot Detection
const BOT_PATTERNS = [
  /googlebot/i,
  /bingbot/i,
  /slurp/i,
  /duckduckbot/i,
  /crawler/i,
  /scrapy/i,
];

function isBot(userAgent: string): boolean {
  return BOT_PATTERNS.some(pattern => pattern.test(userAgent));
}

export function middleware(request: NextRequest) {
  const userAgent = request.headers.get('user-agent') || '';

  if (isBot(userAgent)) {
    // Bot のキャッシュをより長く
    const response = NextResponse.next();
    response.headers.set('Cache-Control', 'public, max-age=86400');
    return response;
  }

  return NextResponse.next();
}
```

### 4.2 レート制限（IP ベース）

```typescript
// middleware.ts - Rate Limiting at Edge
import { Ratelimit } from '@vercel/edge-runtime';

// グローバルレートリミッター（メモリベース）
const ratelimit = new Ratelimit({
  key: (request) => request.ip || 'unknown',
  limit: 100,
  window: '1 m',
});

export async function middleware(request: NextRequest) {
  // 特定ルートのみ制限
  if (request.nextUrl.pathname.startsWith('/api/')) {
    const { success } = await ratelimit.limit(request);

    if (!success) {
      return new NextResponse(JSON.stringify({ error: 'Too many requests' }), {
        status: 429,
      });
    }
  }

  return NextResponse.next();
}
```

### 4.3 疑わしいリクエスト検知

```typescript
// middleware.ts - Suspicious Request Detection
export function middleware(request: NextRequest) {
  const userAgent = request.headers.get('user-agent') || '';
  const referer = request.headers.get('referer') || '';
  const ip = request.ip;

  // 疑わしいパターン
  const isSuspicious =
    !userAgent || // User-Agent なし
    userAgent.length < 5 || // 短すぎる
    /curl|wget|python|java(?!script)/i.test(userAgent) || // CLI ツール
    !referer && request.nextUrl.pathname.startsWith('/admin'); // Referer なしで管理画面

  if (isSuspicious) {
    // ログに記録（Vercel Analytics へ）
    console.warn(`[SUSPICIOUS] IP: ${ip}, UA: ${userAgent}`);

    // 追加検証が必要な場合
    if (request.nextUrl.pathname.startsWith('/admin')) {
      return new NextResponse(JSON.stringify({ error: 'Unauthorized' }), {
        status: 401,
      });
    }
  }

  return NextResponse.next();
}
```

---

## 5. Cold Start 削減

### 5.1 Function Bundle サイズ削減

```typescript
// ❌ 悪い例：不要な依存が全部バンドル
import _ from 'lodash';
import moment from 'moment';
import axios from 'axios';

export default function handler(req, res) {
  const date = moment().format('YYYY-MM-DD');
  res.json({ date });
}

// ✅ 良い例：必要な機能のみ
import { format } from 'date-fns';

export default function handler(req, res) {
  const date = format(new Date(), 'yyyy-MM-dd');
  res.json({ date });
}
```

### 5.2 動的インポート（遅延読み込み）

```typescript
// pages/api/heavy-computation.ts
export default async function handler(req, res) {
  // 遅延読み込み（必要になったら）
  const { heavyFunction } = await import('@/lib/heavy');

  const result = await heavyFunction();
  res.json(result);
}
```

### 5.3 Tree Shaking

```bash
# package.json でサイドエフェクト標記
{
  "sideEffects": false,  // Tree Shaking 有効化
  "main": "dist/index.js",
  "module": "dist/index.esm.js",
  "exports": {
    ".": {
      "import": "./dist/index.esm.js",
      "require": "./dist/index.js"
    }
  }
}
```

### 5.4 Node.js Bundled Dependencies

```typescript
// vercel.json - Function Bundling
{
  "functions": {
    "api/heavy/**": {
      "memory": 3008,  // メモリ増加 → 起動速度向上
      "maxDuration": 60
    },
    "api/light/**": {
      "memory": 512,   // 軽量関数
      "maxDuration": 10
    }
  }
}
```

---

## 6. Function サイズ最適化

### 6.1 バンドルサイズ計測

```bash
# Vercel deployment で表示される:
# api/users - 245 KB
# api/posts - 156 KB

# もし超過したら（50MB上限）
# nextjs/build-cache をクリア
vercel env add VERCEL_USE_LEGACY_RUNTIME true
```

### 6.2 不要なパッケージ削除

```bash
# 使用状況分析
npm ls | grep deduped

# 不要パッケージ削除
npm uninstall moment  # date-fns を使用
npm uninstall lodash  # ネイティブ関数を使用
npm uninstall express # Next.js API Routes で十分
```

### 6.3 コード分割・最小化

```typescript
// ✅ 分割
// pages/api/users.ts
export default async function handler(req, res) {
  const { getUser } = await import('@/lib/user');
  const user = await getUser(req.query.id);
  res.json(user);
}

// pages/api/posts.ts
export default async function handler(req, res) {
  const { getPost } = await import('@/lib/post');
  const post = await getPost(req.query.id);
  res.json(post);
}
```

---

## 7. Streaming Responses

### 7.1 大容量データストリーミング

```typescript
// pages/api/stream-data.ts
import { Readable } from 'stream';

export default async function handler(req, res) {
  res.setHeader('Content-Type', 'application/json');

  // Stream で大量データ返送
  const readable = Readable.from(
    (async function* () {
      for (let i = 0; i < 10000; i++) {
        yield JSON.stringify({ id: i, data: `item ${i}` }) + '\n';
      }
    })()
  );

  readable.pipe(res);
}
```

### 7.2 Server-Sent Events (SSE)

```typescript
// pages/api/events.ts
export default function handler(req, res) {
  res.setHeader('Content-Type', 'text/event-stream');
  res.setHeader('Cache-Control', 'no-cache');
  res.setHeader('Connection', 'keep-alive');

  // 定期的にデータ送信
  let count = 0;
  const interval = setInterval(() => {
    count++;
    res.write(`data: ${JSON.stringify({ timestamp: new Date(), count })}\n\n`);

    if (count >= 100) {
      clearInterval(interval);
      res.end();
    }
  }, 1000);

  req.on('close', () => clearInterval(interval));
}
```

### 7.3 Next.js App Router での Response Streaming

```typescript
// app/api/stream/route.ts
export const dynamic = 'force-dynamic';

export async function GET() {
  const stream = new ReadableStream({
    async start(controller) {
      for (let i = 0; i < 100; i++) {
        controller.enqueue(
          new TextEncoder().encode(`data: ${JSON.stringify({ id: i })}\n\n`)
        );
        await new Promise(resolve => setTimeout(resolve, 100));
      }
      controller.close();
    },
  });

  return new Response(stream, {
    headers: {
      'Content-Type': 'text/event-stream',
      'Cache-Control': 'no-cache',
    },
  });
}
```

---

## 8. 実装パフォーマンスチューニング

### 8.1 Function Duration 最適化

```typescript
// pages/api/slow.ts
export const config = {
  maxDuration: 60,  // 最大実行時間 60秒
};

export default async function handler(req, res) {
  // 重い処理
  console.time('process');
  
  const result = await heavyComputation();
  
  console.timeEnd('process');  // ログから所要時間確認
  
  res.json(result);
}
```

### 8.2 Database Connection Pool 最適化

```typescript
// lib/db.ts
let pool: any;

export async function getPool() {
  if (!pool) {
    pool = new Pool({
      connectionString: process.env.DATABASE_URL,
      max: 20,
      min: 2,
      idleTimeoutMillis: 30000,
      connectionTimeoutMillis: 2000,
    });
  }
  return pool;
}

// pages/api/users.ts
export default async function handler(req, res) {
  const pool = await getPool();
  const client = await pool.connect();

  try {
    const result = await client.query('SELECT * FROM users');
    res.json(result.rows);
  } finally {
    client.release();
  }
}
```

### 8.3 メモリ使用量監視

```typescript
// lib/monitoring.ts
export function logMemoryUsage(label: string) {
  if (process.env.NODE_ENV === 'development') {
    const usage = process.memoryUsage();
    console.log(`[${label}] Memory:`, {
      rss: `${Math.round(usage.rss / 1024 / 1024)} MB`,
      heapUsed: `${Math.round(usage.heapUsed / 1024 / 1024)} MB`,
      heapTotal: `${Math.round(usage.heapTotal / 1024 / 1024)} MB`,
    });
  }
}

// 使用
export default async function handler(req, res) {
  logMemoryUsage('Start');

  const data = await fetchData();

  logMemoryUsage('After fetch');

  res.json(data);
}
```

---

## 📖 関連ドキュメント

- [06_パフォーマンス最適化.md](./06_パフォーマンス最適化.md) — Core Web Vitals・基本最適化
- [09_API_ルート詳細.md](./09_API_ルート詳細.md) — API実装基礎
