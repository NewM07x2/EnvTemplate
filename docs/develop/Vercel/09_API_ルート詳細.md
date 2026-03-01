# Vercel API ルート詳細

> **対象者**: Vercel でサーバーレス API を構築・運用する開発者  
> **主要トピック**: API ルート / リクエスト処理 / 認証・認可 / レート制限 / エラーハンドリング

---

## 📚 目次

1. [API ルート基礎](#1-api-ルート基礎)
2. [リクエスト・レスポンス処理](#2-リクエストレスポンス処理)
3. [認証・認可](#3-認証認可)
4. [レート制限](#4-レート制限)
5. [バリデーション](#5-バリデーション)
6. [エラーハンドリング](#6-エラーハンドリング)
7. [CORS 対応](#7-cors-対応)
8. [パフォーマンス最適化](#8-パフォーマンス最適化)

---

## 1. API ルート基礎

### 1.1 API ルート作成

**Next.js (Pages Router)**

```typescript
// pages/api/hello.ts
import type { NextApiRequest, NextApiResponse } from 'next';

type Data = {
  message: string;
};

export default function handler(
  req: NextApiRequest,
  res: NextApiResponse<Data>
) {
  res.status(200).json({ message: 'Hello' });
}
```

**Next.js (App Router)**

```typescript
// app/api/hello/route.ts
import { NextRequest, NextResponse } from 'next/server';

export async function GET(request: NextRequest) {
  return NextResponse.json({ message: 'Hello' });
}

export async function POST(request: NextRequest) {
  const data = await request.json();
  return NextResponse.json(data);
}
```

### 1.2 HTTP メソッド対応

```typescript
// pages/api/users/[id].ts
export default async function handler(req, res) {
  const { id } = req.query;

  if (req.method === 'GET') {
    // ユーザー取得
    const user = await getUser(id);
    res.json(user);
  } else if (req.method === 'PUT') {
    // ユーザー更新
    const updated = await updateUser(id, req.body);
    res.json(updated);
  } else if (req.method === 'DELETE') {
    // ユーザー削除
    await deleteUser(id);
    res.status(204).end();
  } else {
    res.status(405).json({ error: 'Method not allowed' });
  }
}
```

### 1.3 Middleware 実装

```typescript
// middleware/auth.ts
import { NextApiRequest, NextApiResponse } from 'next';

export function withAuth(handler: Function) {
  return async (req: NextApiRequest, res: NextApiResponse) => {
    const token = req.headers.authorization?.split(' ')[1];

    if (!token) {
      return res.status(401).json({ error: 'Unauthorized' });
    }

    try {
      const decoded = verifyToken(token);
      (req as any).user = decoded;
      return handler(req, res);
    } catch {
      return res.status(401).json({ error: 'Invalid token' });
    }
  };
}

// 使用
// pages/api/protected.ts
import { withAuth } from '@/middleware/auth';

export default withAuth(async (req, res) => {
  const user = (req as any).user;
  res.json({ message: `Hello ${user.name}` });
});
```

---

## 2. リクエスト・レスポンス処理

### 2.1 リクエストボディ解析

```typescript
export default async function handler(req, res) {
  // JSON ボディ
  if (req.headers['content-type'] === 'application/json') {
    const body = req.body;  // 自動解析
    console.log(body);
  }

  // フォームデータ
  if (req.headers['content-type']?.includes('form-data')) {
    const form = new FormData();
    // multipart 処理
  }

  // クエリパラメータ
  const { name, age } = req.query;

  // URL パラメータ
  const { id } = req.query;

  res.json({ received: true });
}
```

### 2.2 ファイルアップロード

```bash
npm install formidable
```

```typescript
import formidable from 'formidable';
import fs from 'fs';

export const config = {
  api: {
    bodyParser: false,  // Next.js の自動パーサー無効化
  },
};

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).end();
  }

  const form = formidable({ uploadDir: './public/uploads' });
  const [fields, files] = await form.parse(req);

  const file = files.file?.[0];
  console.log(`Uploaded: ${file?.newFilename}`);

  res.json({ filename: file?.newFilename });
}
```

### 2.3 大量データ処理

```typescript
export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).end();
  }

  // ストリーミング処理
  const chunks = [];
  
  req.on('data', (chunk) => {
    chunks.push(chunk);
  });

  req.on('end', async () => {
    const data = Buffer.concat(chunks).toString();
    const parsed = JSON.parse(data);

    // 処理
    res.json({ processed: true });
  });

  req.on('error', (error) => {
    res.status(400).json({ error: error.message });
  });
}
```

### 2.4 レスポンスヘッダー設定

```typescript
export default function handler(req, res) {
  // キャッシュ
  res.setHeader('Cache-Control', 'public, max-age=3600');

  // CORS
  res.setHeader('Access-Control-Allow-Origin', '*');

  // セキュリティ
  res.setHeader('X-Content-Type-Options', 'nosniff');

  // カスタムヘッダー
  res.setHeader('X-API-Version', '1.0');

  res.json({ data: 'value' });
}
```

---

## 3. 認証・認可

### 3.1 JWT (JSON Web Token)

```bash
npm install jsonwebtoken
```

```typescript
import jwt from 'jsonwebtoken';

// トークン生成
export function generateToken(user) {
  return jwt.sign(
    { id: user.id, email: user.email },
    process.env.JWT_SECRET!,
    { expiresIn: '7d' }
  );
}

// トークン検証
export function verifyToken(token: string) {
  try {
    return jwt.verify(token, process.env.JWT_SECRET!);
  } catch {
    throw new Error('Invalid token');
  }
}
```

```typescript
// pages/api/auth/login.ts
import { generateToken } from '@/lib/auth';

export default async function handler(req, res) {
  const { email, password } = req.body;

  // ユーザー検証
  const user = await verifyCredentials(email, password);
  if (!user) {
    return res.status(401).json({ error: 'Invalid credentials' });
  }

  const token = generateToken(user);
  res.json({ token });
}
```

```typescript
// pages/api/me.ts
import { verifyToken } from '@/lib/auth';

export default async function handler(req, res) {
  const token = req.headers.authorization?.split(' ')[1];

  if (!token) {
    return res.status(401).json({ error: 'No token' });
  }

  try {
    const payload = verifyToken(token);
    res.json({ user: payload });
  } catch {
    res.status(401).json({ error: 'Invalid token' });
  }
}
```

### 3.2 OAuth 連携

```bash
npm install next-auth
```

```typescript
// pages/api/auth/[...nextauth].ts
import NextAuth from 'next-auth';
import GoogleProvider from 'next-auth/providers/google';

export default NextAuth({
  providers: [
    GoogleProvider({
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
    }),
  ],
  secret: process.env.NEXTAUTH_SECRET,
});
```

### 3.3 セッション管理

```typescript
// pages/api/admin.ts
import { getSession } from 'next-auth/react';

export default async function handler(req, res) {
  const session = await getSession({ req });

  if (!session) {
    return res.status(401).json({ error: 'Unauthorized' });
  }

  if (session.user.role !== 'admin') {
    return res.status(403).json({ error: 'Forbidden' });
  }

  res.json({ data: 'admin-only' });
}
```

---

## 4. レート制限

### 4.1 メモリベースの実装

```typescript
const rateLimitMap = new Map<string, number[]>();

export function isRateLimited(clientId: string, limit: number, windowMs: number) {
  const now = Date.now();
  const requests = rateLimitMap.get(clientId) || [];

  // 期限切れリクエスト削除
  const recentRequests = requests.filter((t) => now - t < windowMs);

  if (recentRequests.length >= limit) {
    return true;
  }

  recentRequests.push(now);
  rateLimitMap.set(clientId, recentRequests);

  return false;
}

// 使用
export default function handler(req, res) {
  const clientIp = req.headers['x-forwarded-for'] as string;

  if (isRateLimited(clientIp, 100, 60 * 1000)) {
    return res.status(429).json({ error: 'Too many requests' });
  }

  res.json({ data: 'OK' });
}
```

### 4.2 Vercel KV を使用

```bash
npm install @vercel/kv
```

```typescript
import { kv } from '@vercel/kv';

export default async function handler(req, res) {
  const clientIp = req.headers['x-forwarded-for'] as string;
  const key = `ratelimit:${clientIp}`;

  const count = await kv.incr(key);

  if (count === 1) {
    await kv.expire(key, 60);  // 60秒で自動削除
  }

  if (count > 100) {
    return res.status(429).json({ error: 'Too many requests' });
  }

  res.json({ data: 'OK', remaining: 100 - count });
}
```

### 4.3 npm ライブラリ

```bash
npm install express-rate-limit
```

```typescript
import rateLimit from 'express-rate-limit';

const limiter = rateLimit({
  windowMs: 15 * 60 * 1000,  // 15分
  max: 100,                    // リクエスト上限
  message: 'Too many requests',
});

export default limiter(async (req, res) => {
  res.json({ data: 'OK' });
});
```

---

## 5. バリデーション

### 5.1 Zod スキーマバリデーション

```bash
npm install zod
```

```typescript
import { z } from 'zod';

const createUserSchema = z.object({
  name: z.string().min(1),
  email: z.string().email(),
  age: z.number().int().positive(),
});

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).end();
  }

  try {
    const data = createUserSchema.parse(req.body);
    const user = await createUser(data);
    res.status(201).json(user);
  } catch (error) {
    if (error instanceof z.ZodError) {
      return res.status(400).json({ errors: error.errors });
    }
    res.status(500).json({ error: 'Server error' });
  }
}
```

### 5.2 Joi スキーマ

```bash
npm install joi
```

```typescript
import Joi from 'joi';

const schema = Joi.object({
  name: Joi.string().required(),
  email: Joi.string().email().required(),
});

export default async function handler(req, res) {
  const { error, value } = schema.validate(req.body);

  if (error) {
    return res.status(400).json({ error: error.details });
  }

  res.json({ validated: value });
}
```

### 5.3 カスタムバリデーション

```typescript
export default async function handler(req, res) {
  const { email } = req.body;

  // メールアドレス形式
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    return res.status(400).json({ error: 'Invalid email' });
  }

  // 既存チェック
  const exists = await userExists(email);
  if (exists) {
    return res.status(409).json({ error: 'Email already registered' });
  }

  res.json({ valid: true });
}
```

---

## 6. エラーハンドリング

### 6.1 統一的なエラーレスポンス

```typescript
interface ApiError {
  statusCode: number;
  message: string;
  details?: any;
}

export function sendError(res, error: ApiError) {
  res.status(error.statusCode).json({
    error: {
      message: error.message,
      details: error.details,
    },
  });
}

// 使用
export default async function handler(req, res) {
  try {
    const data = await fetchData();
    res.json(data);
  } catch (error) {
    sendError(res, {
      statusCode: 500,
      message: 'Failed to fetch data',
      details: error.message,
    });
  }
}
```

### 6.2 エラークラス

```typescript
export class ApiError extends Error {
  constructor(
    public statusCode: number,
    message: string,
    public details?: any
  ) {
    super(message);
  }
}

export class NotFoundError extends ApiError {
  constructor(resource: string) {
    super(404, `${resource} not found`);
  }
}

export class ValidationError extends ApiError {
  constructor(details: any) {
    super(400, 'Validation failed', details);
  }
}

// 使用
export default async function handler(req, res) {
  try {
    const user = await getUser(id);
    if (!user) throw new NotFoundError('User');
    res.json(user);
  } catch (error) {
    if (error instanceof ApiError) {
      return res.status(error.statusCode).json({ error: error.message });
    }
    res.status(500).json({ error: 'Internal server error' });
  }
}
```

### 6.3 Sentry 統合

```bash
npm install @sentry/nextjs
```

```typescript
import * as Sentry from '@sentry/nextjs';

export default async function handler(req, res) {
  try {
    const data = await riskyOperation();
    res.json(data);
  } catch (error) {
    Sentry.captureException(error, {
      contexts: {
        request: { method: req.method, url: req.url },
      },
    });
    res.status(500).json({ error: 'Internal error' });
  }
}
```

---

## 7. CORS 対応

### 7.1 CORS ミドルウェア

```typescript
export function withCORS(handler: Function) {
  return async (req, res) => {
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE,OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type,Authorization');

    if (req.method === 'OPTIONS') {
      return res.status(200).end();
    }

    return handler(req, res);
  };
}

// 使用
export default withCORS(async (req, res) => {
  res.json({ data: 'OK' });
});
```

### 7.2 特定のオリジン許可

```typescript
const ALLOWED_ORIGINS = ['https://example.com', 'https://app.example.com'];

export default async function handler(req, res) {
  const origin = req.headers.origin;

  if (origin && ALLOWED_ORIGINS.includes(origin)) {
    res.setHeader('Access-Control-Allow-Origin', origin);
  }

  res.json({ data: 'OK' });
}
```

---

## 8. パフォーマンス最適化

### 8.1 キャッシング

```typescript
export default async function handler(req, res) {
  // 24時間キャッシュ
  res.setHeader('Cache-Control', 'public, max-age=86400');

  const data = await fetchExpensiveData();
  res.json(data);
}
```

### 8.2 圧縮

```typescript
import { compress } from 'brotli';

export default async function handler(req, res) {
  const data = JSON.stringify({ large: 'dataset' });
  const compressed = await compress(Buffer.from(data));

  res.setHeader('Content-Encoding', 'br');
  res.send(compressed);
}
```

### 8.3 Connection Pool

```typescript
import { Pool } from 'pg';

const pool = new Pool({
  max: 20,
  idleTimeoutMillis: 30000,
});

export default async function handler(req, res) {
  const client = await pool.connect();
  try {
    const result = await client.query('SELECT * FROM users');
    res.json(result.rows);
  } finally {
    client.release();
  }
}
```

---

## 📖 関連ドキュメント

- [03_フレームワーク別設定.md](./03_フレームワーク別設定.md) — フレームワーク設定
- [04_環境設定・CI-CD.md](./04_環境設定・CI-CD.md) — 環境設定
