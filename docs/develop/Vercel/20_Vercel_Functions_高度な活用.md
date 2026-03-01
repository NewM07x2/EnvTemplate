# Vercel Functions 高度な活用

> **対象者**: Vercel Serverless Functions を最大限に活用したい開発者  
> **主要トピック**: Function の詳細設定 / パフォーマンス最適化 / セキュリティ / 複雑なワークフロー / スケーリング

---

## 📚 目次

1. [Function の詳細設定](#1-function-の詳細設定)
2. [Route Handlers (Next.js 13+)](#2-route-handlers-nextjs-13)
3. [Middleware・Edge Functions](#3-middlewareexge-functions)
4. [エラーハンドリング・リトライ](#4-エラーハンドリングリトライ)
5. [パフォーマンス最適化](#5-パフォーマンス最適化)
6. [セキュリティ・認証](#6-セキュリティ認証)
7. [複雑なワークフロー](#7-複雑なワークフロー)
8. [監視・デバッグ](#8-監視デバッグ)

---

## 1. Function の詳細設定

### 1.1 Function メタデータ

```typescript
// app/api/hello/route.ts
export const runtime = 'nodejs'; // 'nodejs' | 'edge'
export const preferredRegion = ['sfo1', 'iad1']; // リージョン指定
export const dynamic = 'force-dynamic'; // 'force-dynamic' | 'auto' | 'force-static'
export const maxDuration = 60; // 最大実行時間（秒）

export async function GET(request: Request) {
  return Response.json({ message: 'Hello' });
}
```

### 1.2 リージョン戦略

```typescript
// app/api/latency-sensitive/route.ts
// 低遅延が必須な処理
export const preferredRegion = 'sfo1'; // 単一リージョン

export async function GET(request: Request) {
  return Response.json({ timestamp: Date.now() });
}

// app/api/batch-processing/route.ts
// リージョン選択の柔軟性が必要
export const preferredRegion = ['sfo1', 'iad1', 'lhr1'];

export async function POST(request: Request) {
  // バックグラウンドタスク
  return Response.json({ queued: true });
}
```

### 1.3 タイムアウト管理

```typescript
// app/api/long-running/route.ts
export const maxDuration = 300; // 5分（有料プランのみ可能）

export async function POST(request: Request) {
  const start = Date.now();

  try {
    // 長時間処理
    const result = await heavyComputation();
    
    const duration = Date.now() - start;
    
    if (duration > 30000) {
      console.warn(`Computation took ${duration}ms`);
    }

    return Response.json({ result, duration });
  } catch (error) {
    if (error instanceof Error && error.message.includes('timeout')) {
      return Response.json(
        { error: 'Processing timeout' },
        { status: 504 }
      );
    }
    throw error;
  }
}
```

---

## 2. Route Handlers (Next.js 13+)

### 2.1 基本的な Route Handler

```typescript
// app/api/users/[id]/route.ts
import { NextRequest, NextResponse } from 'next/server';

export async function GET(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  try {
    const user = await getUser(params.id);
    
    if (!user) {
      return NextResponse.json(
        { error: 'User not found' },
        { status: 404 }
      );
    }

    return NextResponse.json(user);
  } catch (error) {
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}

export async function PATCH(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  const body = await request.json();
  const user = await updateUser(params.id, body);
  return NextResponse.json(user);
}

export async function DELETE(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  await deleteUser(params.id);
  return NextResponse.json({ success: true });
}
```

### 2.2 ストリーミング レスポンス

```typescript
// app/api/stream/route.ts
export async function GET(request: Request) {
  const encoder = new TextEncoder();

  const customReadable = new ReadableStream({
    async start(controller) {
      // データをチャンク単位で送信
      for (let i = 0; i < 10; i++) {
        const chunk = encoder.encode(`data: ${i}\n\n`);
        controller.enqueue(chunk);

        // 遅延
        await new Promise((resolve) => setTimeout(resolve, 1000));
      }

      controller.close();
    },
  });

  return new Response(customReadable, {
    headers: {
      'Content-Type': 'text/event-stream',
      'Cache-Control': 'no-cache',
      'Connection': 'keep-alive',
    },
  });
}
```

### 2.3 Server-Sent Events (SSE)

```typescript
// app/api/sse/route.ts
export async function GET(request: Request) {
  // クライアントが接続を切ったか確認
  const { signal } = request;

  const encoder = new TextEncoder();
  let counter = 0;

  const customReadable = new ReadableStream({
    async start(controller) {
      // 接続時にクライアント ID を生成
      const clientId = crypto.randomUUID();
      controller.enqueue(
        encoder.encode(`:connected\ndata: ${clientId}\n\n`)
      );

      const interval = setInterval(() => {
        if (signal.aborted) {
          clearInterval(interval);
          controller.close();
          return;
        }

        const data = JSON.stringify({
          timestamp: Date.now(),
          counter: counter++,
        });

        controller.enqueue(
          encoder.encode(`data: ${data}\n\n`)
        );
      }, 1000);

      // クライアント接続切断時の処理
      signal.addEventListener('abort', () => {
        clearInterval(interval);
        controller.close();
      });
    },
  });

  return new Response(customReadable, {
    headers: {
      'Content-Type': 'text/event-stream',
      'Cache-Control': 'no-cache',
      'Connection': 'keep-alive',
    },
  });
}
```

### 2.4 WebSocket (Vercel では非サポート、代替案)

```typescript
// WebSocket の代替：長ポーリング
// app/api/poll/route.ts
export async function POST(request: Request) {
  const { clientId, lastSeenId } = await request.json();

  // タイムアウト: 30秒
  let result = null;
  const startTime = Date.now();

  while (Date.now() - startTime < 30000) {
    // 新しいメッセージを確認
    result = await checkForNewMessages(clientId, lastSeenId);

    if (result) {
      return Response.json(result);
    }

    // 1秒待機
    await new Promise((resolve) => setTimeout(resolve, 1000));
  }

  // タイムアウト
  return Response.json({ status: 'timeout' });
}
```

---

## 3. Middleware・Edge Functions

### 3.1 Request Middleware

```typescript
// middleware.ts
import { NextRequest, NextResponse } from 'next/server';

export function middleware(request: NextRequest) {
  // リクエスト ID を追加
  const requestId = crypto.randomUUID();
  
  const response = NextResponse.next();
  response.headers.set('X-Request-ID', requestId);

  // API レート制限チェック
  const ip = request.headers.get('x-forwarded-for') || 'unknown';
  
  if (isRateLimited(ip)) {
    return NextResponse.json(
      { error: 'Rate limit exceeded' },
      { status: 429 }
    );
  }

  // 認証チェック
  const token = request.headers.get('authorization');
  
  if (request.nextUrl.pathname.startsWith('/admin')) {
    if (!token || !isValidToken(token)) {
      return NextResponse.redirect(
        new URL('/login', request.url)
      );
    }
  }

  return response;
}

export const config = {
  matcher: ['/api/:path*', '/admin/:path*'],
};
```

### 3.2 Response Transform Middleware

```typescript
// middleware.ts
export function middleware(request: NextRequest) {
  let response = NextResponse.next();

  // JSON レスポンスラッパー
  if (request.nextUrl.pathname.startsWith('/api')) {
    const originalResponse = response.clone();
    const status = response.status;
    const headers = Object.fromEntries(response.headers.entries());

    const transformedBody = {
      status,
      headers,
      timestamp: new Date().toISOString(),
    };

    response = new NextResponse(JSON.stringify(transformedBody), {
      status: response.status,
      headers: response.headers,
    });
  }

  return response;
}
```

### 3.3 Edge Function（地理情報活用）

```typescript
// app/api/geo/route.ts
import { NextRequest, NextResponse } from 'next/server';

export const runtime = 'edge';

export async function GET(request: NextRequest) {
  // 地理情報を取得
  const country = request.headers.get('x-vercel-ip-country');
  const city = request.headers.get('x-vercel-ip-city');
  const latitude = request.headers.get('x-vercel-ip-latitude');
  const longitude = request.headers.get('x-vercel-ip-longitude');

  // 地域別コンテンツを返す
  const content = await getContentForRegion(country);

  return NextResponse.json({
    geo: { country, city, latitude, longitude },
    content,
  });
}
```

---

## 4. エラーハンドリング・リトライ

### 4.1 構造化エラーレスポンス

```typescript
// lib/api-errors.ts
export class APIError extends Error {
  constructor(
    public statusCode: number,
    message: string,
    public code: string,
    public details?: any
  ) {
    super(message);
  }
}

export function handleAPIError(error: unknown) {
  if (error instanceof APIError) {
    return Response.json(
      {
        error: error.message,
        code: error.code,
        details: error.details,
      },
      { status: error.statusCode }
    );
  }

  if (error instanceof SyntaxError) {
    return Response.json(
      {
        error: 'Invalid request body',
        code: 'INVALID_JSON',
      },
      { status: 400 }
    );
  }

  // 予期しないエラー
  console.error('Unexpected error:', error);
  
  return Response.json(
    {
      error: 'Internal server error',
      code: 'INTERNAL_ERROR',
    },
    { status: 500 }
  );
}

// 使用例
export async function GET(request: Request) {
  try {
    const data = await fetchData();
    return Response.json(data);
  } catch (error) {
    return handleAPIError(error);
  }
}
```

### 4.2 リトライロジック

```typescript
// lib/retry-utils.ts
export interface RetryOptions {
  maxRetries?: number;
  delayMs?: number;
  backoff?: boolean;
  onRetry?: (attempt: number) => void;
}

export async function withRetry<T>(
  fn: () => Promise<T>,
  options: RetryOptions = {}
): Promise<T> {
  const {
    maxRetries = 3,
    delayMs = 100,
    backoff = true,
    onRetry,
  } = options;

  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try {
      return await fn();
    } catch (error) {
      if (attempt === maxRetries) {
        throw error;
      }

      const delay = backoff
        ? delayMs * Math.pow(2, attempt)
        : delayMs;

      onRetry?.(attempt + 1);

      await new Promise((resolve) =>
        setTimeout(resolve, delay)
      );
    }
  }

  throw new Error('Retry failed');
}

// 使用例
export async function fetchWithRetry(url: string) {
  return withRetry(
    () => fetch(url).then((r) => r.json()),
    {
      maxRetries: 3,
      backoff: true,
      onRetry: (attempt) => {
        console.log(`Retry attempt ${attempt}`);
      },
    }
  );
}
```

### 4.3 Circuit Breaker パターン

```typescript
// lib/circuit-breaker.ts
type CircuitState = 'closed' | 'open' | 'half-open';

export class CircuitBreaker {
  private state: CircuitState = 'closed';
  private failureCount = 0;
  private lastFailureTime?: number;

  constructor(
    private readonly failureThreshold: number = 5,
    private readonly resetTimeout: number = 60000 // 1分
  ) {}

  async execute<T>(fn: () => Promise<T>): Promise<T> {
    if (this.state === 'open') {
      if (
        this.lastFailureTime &&
        Date.now() - this.lastFailureTime > this.resetTimeout
      ) {
        this.state = 'half-open';
      } else {
        throw new Error('Circuit breaker is open');
      }
    }

    try {
      const result = await fn();

      if (this.state === 'half-open') {
        this.state = 'closed';
        this.failureCount = 0;
      }

      return result;
    } catch (error) {
      this.failureCount++;
      this.lastFailureTime = Date.now();

      if (this.failureCount >= this.failureThreshold) {
        this.state = 'open';
      }

      throw error;
    }
  }

  getState() {
    return this.state;
  }
}

// 使用例
const breaker = new CircuitBreaker(3, 30000);

export async function callExternalService() {
  return breaker.execute(() => fetch('/external-api').then(r => r.json()));
}
```

---

## 5. パフォーマンス最適化

### 5.1 コネクションプーリング

```typescript
// lib/db-pool.ts
import { createPool } from 'pg';

const pool = createPool({
  host: process.env.DB_HOST,
  port: parseInt(process.env.DB_PORT || '5432'),
  database: process.env.DB_NAME,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  max: 20,
  idleTimeoutMillis: 30000,
  connectionTimeoutMillis: 2000,
});

export async function queryDB(sql: string, params?: any[]) {
  const client = await pool.connect();
  try {
    return await client.query(sql, params);
  } finally {
    client.release();
  }
}
```

### 5.2 キャッシング層

```typescript
// lib/cached-fetch.ts
import { kv } from '@vercel/kv';

export async function fetchWithCache<T>(
  key: string,
  fetcher: () => Promise<T>,
  ttl: number = 3600
): Promise<T> {
  // キャッシュから取得
  const cached = await kv.get(key);
  if (cached) {
    return JSON.parse(cached as string);
  }

  // 取得
  const data = await fetcher();

  // キャッシュに保存
  await kv.setex(key, ttl, JSON.stringify(data));

  return data;
}

// API Route で使用
export async function GET(request: Request) {
  const data = await fetchWithCache(
    'expensive-data',
    () => fetchExpensiveData(),
    1800 // 30分
  );

  return Response.json(data);
}
```

### 5.3 バッチ処理

```typescript
// lib/batch-processor.ts
export class BatchProcessor<T, R> {
  private queue: T[] = [];
  private processing = false;

  constructor(
    private batchSize: number,
    private processor: (batch: T[]) => Promise<R[]>
  ) {}

  add(item: T): Promise<R> {
    return new Promise((resolve, reject) => {
      this.queue.push(item);

      if (this.queue.length >= this.batchSize) {
        this.flush().catch(reject);
      }
    });
  }

  async flush(): Promise<void> {
    if (this.processing || this.queue.length === 0) {
      return;
    }

    this.processing = true;

    try {
      const batch = this.queue.splice(0, this.batchSize);
      await this.processor(batch);
    } finally {
      this.processing = false;
    }
  }
}
```

---

## 6. セキュリティ・認証

### 6.1 API Key 認証

```typescript
// lib/api-auth.ts
export function verifyAPIKey(token?: string): boolean {
  if (!token) return false;

  const validKeys = (process.env.VALID_API_KEYS || '').split(',');
  return validKeys.includes(token);
}

// API Route で使用
export async function GET(request: Request) {
  const apiKey = request.headers.get('x-api-key');

  if (!verifyAPIKey(apiKey || undefined)) {
    return Response.json(
      { error: 'Invalid API key' },
      { status: 401 }
    );
  }

  return Response.json({ data: 'secret' });
}
```

### 6.2 CORS セキュリティ

```typescript
// lib/cors.ts
export function corsHeaders(
  origin?: string,
  allowedOrigins = ['https://example.com']
) {
  const isAllowed =
    origin && allowedOrigins.includes(origin);

  return {
    'Access-Control-Allow-Origin': isAllowed
      ? origin
      : 'null',
    'Access-Control-Allow-Methods': 'GET, POST, PATCH, DELETE',
    'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    'Access-Control-Max-Age': '86400',
  };
}

// API Route で使用
export async function OPTIONS(request: Request) {
  return Response.json({}, {
    headers: corsHeaders(request.headers.get('origin')),
  });
}

export async function GET(request: Request) {
  return Response.json(
    { data: 'public' },
    { headers: corsHeaders(request.headers.get('origin')) }
  );
}
```

### 6.3 入力検証

```typescript
// lib/validation.ts
import { z } from 'zod';

const userSchema = z.object({
  name: z.string().min(1).max(255),
  email: z.string().email(),
  age: z.number().int().min(0).max(150).optional(),
});

export type User = z.infer<typeof userSchema>;

export function validateUser(data: unknown): User {
  return userSchema.parse(data);
}

// API Route で使用
export async function POST(request: Request) {
  const body = await request.json();

  try {
    const user = validateUser(body);
    return Response.json(user);
  } catch (error) {
    if (error instanceof z.ZodError) {
      return Response.json(
        { error: 'Validation failed', issues: error.issues },
        { status: 400 }
      );
    }
    throw error;
  }
}
```

---

## 7. 複雑なワークフロー

### 7.1 複数ステップの処理

```typescript
// app/api/workflows/process/route.ts
import { sql } from '@vercel/postgres';

export async function POST(request: Request) {
  const { itemId } = await request.json();

  const steps = [
    { name: 'validate', fn: validateItem },
    { name: 'process', fn: processItem },
    { name: 'store', fn: storeResult },
    { name: 'notify', fn: notifyUser },
  ];

  const results: Record<string, any> = {};

  try {
    for (const step of steps) {
      console.log(`Step: ${step.name}`);
      results[step.name] = await step.fn(itemId, results);
    }

    return Response.json({
      status: 'success',
      results,
    });
  } catch (error) {
    // ロールバック
    await rollbackWorkflow(itemId, results);

    return Response.json(
      {
        status: 'failed',
        error: error instanceof Error ? error.message : 'Unknown error',
        completedSteps: Object.keys(results),
      },
      { status: 500 }
    );
  }
}

async function validateItem(itemId: string) {
  // バリデーション
}

async function processItem(itemId: string, prev: any) {
  // 処理
}

async function storeResult(itemId: string, prev: any) {
  // 保存
}

async function notifyUser(itemId: string, prev: any) {
  // 通知
}

async function rollbackWorkflow(itemId: string, results: any) {
  // ロールバック処理
}
```

### 7.2 非同期タスクキューイング

```typescript
// app/api/tasks/queue/route.ts
import { kv } from '@vercel/kv';

export async function POST(request: Request) {
  const task = await request.json();
  const taskId = crypto.randomUUID();

  // タスクをキューに追加
  await kv.rpush('task:queue', JSON.stringify({
    id: taskId,
    ...task,
    status: 'pending',
    createdAt: new Date().toISOString(),
  }));

  return Response.json({
    taskId,
    status: 'queued',
  });
}

// ワーカー（別の Function か cron から呼び出し）
export async function processTasks() {
  while (true) {
    const task = await kv.lpop('task:queue');

    if (!task) {
      // キューが空
      break;
    }

    const parsed = JSON.parse(task as string);

    try {
      await processTask(parsed);
      await kv.hset(`task:${parsed.id}`, {
        status: 'completed',
        completedAt: new Date().toISOString(),
      });
    } catch (error) {
      await kv.hset(`task:${parsed.id}`, {
        status: 'failed',
        error: error instanceof Error ? error.message : 'Unknown',
      });
    }
  }
}
```

---

## 8. 監視・デバッグ

### 8.1 Function の実行ログ

```typescript
// lib/function-logger.ts
import { logger } from '@vercel/functions';

export function logFunctionExecution(
  functionName: string,
  metadata?: any
) {
  const startTime = Date.now();

  return {
    end: (status: 'success' | 'error', result?: any) => {
      const duration = Date.now() - startTime;

      console.log(JSON.stringify({
        function: functionName,
        status,
        duration,
        timestamp: new Date().toISOString(),
        ...metadata,
        ...result,
      }));
    },
  };
}

// 使用例
export async function GET(request: Request) {
  const log = logFunctionExecution('getUser', {
    userId: request.nextUrl.searchParams.get('id'),
  });

  try {
    const user = await getUser('123');
    log.end('success', { userId: user.id });
    return Response.json(user);
  } catch (error) {
    log.end('error', {
      error: error instanceof Error ? error.message : 'Unknown',
    });
    throw error;
  }
}
```

### 8.2 パフォーマンスプロファイリング

```typescript
// lib/profiler.ts
export class Profiler {
  private marks = new Map<string, number>();

  mark(label: string) {
    this.marks.set(label, performance.now());
  }

  measure(label: string, startLabel: string) {
    const start = this.marks.get(startLabel);
    if (!start) return null;

    const end = this.marks.get(label) || performance.now();
    return end - start;
  }

  report() {
    return {
      marks: Array.from(this.marks.entries()),
      summary: this.getSummary(),
    };
  }

  private getSummary() {
    const durations = Array.from(this.marks.values());
    return {
      total: Math.max(...durations) - Math.min(...durations),
      count: this.marks.size,
    };
  }
}

// 使用例
const profiler = new Profiler();

export async function GET(request: Request) {
  profiler.mark('start');

  const data = await fetchData();
  profiler.mark('data-fetched');

  const result = processData(data);
  profiler.mark('processed');

  return Response.json({
    result,
    profiling: profiler.report(),
  });
}
```

---

## 📖 関連ドキュメント

- [09_API_ルート詳細.md](./09_API_ルート詳細.md) — API ルート基礎
- [12_Edge_Middleware・Serverless_Functions_実践.md](./12_Edge_Middleware・Serverless_Functions_実践.md) — Edge 最適化
