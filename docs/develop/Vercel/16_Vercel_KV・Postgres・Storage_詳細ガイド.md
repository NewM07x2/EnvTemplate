# Vercel KV・Postgres・Storage 詳細ガイド

> **対象者**: Vercel の統合データベース・ストレージサービスを本格活用したい開発者  
> **主要トピック**: KV Redis / Vercel Postgres / Blob Storage / キャッシング戦略 / 価格最適化

---

## 📚 目次

1. [Vercel KV (Redis)](#1-vercel-kv-redis)
2. [Vercel Postgres](#2-vercel-postgres)
3. [Vercel Blob Storage](#3-vercel-blob-storage)
4. [キャッシング戦略](#4-キャッシング戦略)
5. [複合データ設計](#5-複合データ設計)
6. [監視・最適化](#6-監視最適化)
7. [エラーハンドリング](#7-エラーハンドリング)
8. [価格最適化](#8-価格最適化)

---

## 1. Vercel KV (Redis)

### 1.1 基本セットアップ

```bash
npm install @vercel/kv
```

```typescript
// lib/redis.ts
import { kv } from '@vercel/kv';

// 接続テスト
export async function testConnection() {
  try {
    const result = await kv.ping();
    console.log('KV Connected:', result);
    return true;
  } catch (error) {
    console.error('KV Connection Failed:', error);
    return false;
  }
}

// セッション保存
export async function setSession(userId: string, sessionData: any) {
  const key = `session:${userId}`;
  const ttl = 86400; // 24時間

  await kv.setex(key, ttl, JSON.stringify(sessionData));
}

// セッション取得
export async function getSession(userId: string) {
  const key = `session:${userId}`;
  const data = await kv.get(key);
  return data ? JSON.parse(data as string) : null;
}
```

### 1.2 キャッシング実装

```typescript
// lib/cache.ts
import { kv } from '@vercel/kv';

const CACHE_VERSION = 'v1';

export async function getCachedData<T>(
  key: string,
  fetchFn: () => Promise<T>,
  ttl: number = 3600
): Promise<T> {
  const cacheKey = `${CACHE_VERSION}:${key}`;

  // キャッシュから取得
  try {
    const cached = await kv.get(cacheKey);
    if (cached) {
      console.log(`Cache hit: ${key}`);
      return JSON.parse(cached as string);
    }
  } catch (error) {
    console.warn(`Cache get failed: ${key}`, error);
  }

  // キャッシュがない場合、データ取得
  const data = await fetchFn();

  // キャッシュに保存
  try {
    await kv.setex(cacheKey, ttl, JSON.stringify(data));
  } catch (error) {
    console.warn(`Cache set failed: ${key}`, error);
  }

  return data;
}

// キャッシュ削除
export async function invalidateCache(key: string) {
  const cacheKey = `${CACHE_VERSION}:${key}`;
  await kv.del(cacheKey);
}
```

### 1.3 レート制限

```typescript
// lib/rate-limit.ts
import { kv } from '@vercel/kv';

interface RateLimitConfig {
  limit: number;    // 制限数
  window: number;   // 秒単位
}

export async function checkRateLimit(
  identifier: string,
  config: RateLimitConfig
): Promise<{ success: boolean; remaining: number; reset: number }> {
  const key = `ratelimit:${identifier}`;

  const current = await kv.incr(key);

  if (current === 1) {
    // 初回アクセス時に有効期限設定
    await kv.expire(key, config.window);
  }

  const ttl = await kv.ttl(key);
  const remaining = Math.max(0, config.limit - current);

  return {
    success: current <= config.limit,
    remaining,
    reset: Date.now() + ttl * 1000,
  };
}

// API ルートで使用
export async function rateLimit(
  req: Request,
  config: RateLimitConfig
) {
  const ip = req.headers.get('x-forwarded-for') || 'unknown';
  const limit = await checkRateLimit(ip, config);

  if (!limit.success) {
    return new Response('Too Many Requests', {
      status: 429,
      headers: {
        'X-RateLimit-Remaining': limit.remaining.toString(),
        'X-RateLimit-Reset': limit.reset.toString(),
      },
    });
  }

  return null;
}
```

### 1.4 リスト・セット操作

```typescript
// lib/kv-collections.ts
import { kv } from '@vercel/kv';

// リスト（Queue 実装）
export async function enqueue(queueName: string, item: any) {
  await kv.rpush(`queue:${queueName}`, JSON.stringify(item));
}

export async function dequeue(queueName: string) {
  const item = await kv.lpop(`queue:${queueName}`);
  return item ? JSON.parse(item as string) : null;
}

// セット（ユーザーフォロー管理）
export async function addFollower(userId: string, followerId: string) {
  await kv.sadd(`followers:${userId}`, followerId);
}

export async function getFollowers(userId: string) {
  return await kv.smembers(`followers:${userId}`);
}

export async function isFollowing(userId: string, followerId: string) {
  return await kv.sismember(`followers:${userId}`, followerId);
}

// ハッシュ（オブジェクト保存）
export async function setUserPreferences(
  userId: string,
  preferences: Record<string, string>
) {
  await kv.hset(`user:${userId}:prefs`, preferences);
}

export async function getUserPreferences(userId: string) {
  return await kv.hgetall(`user:${userId}:prefs`);
}
```

---

## 2. Vercel Postgres

### 2.1 基本セットアップ

```bash
npm install @vercel/postgres
```

```typescript
// lib/db.ts
import { sql } from '@vercel/postgres';

// 接続テスト
export async function testConnection() {
  try {
    const result = await sql`SELECT 1`;
    console.log('Postgres Connected');
    return true;
  } catch (error) {
    console.error('Postgres Connection Failed:', error);
    return false;
  }
}
```

### 2.2 テーブル定義・マイグレーション

```typescript
// lib/migrations.ts
import { sql } from '@vercel/postgres';

export async function createTables() {
  try {
    // ユーザーテーブル
    await sql`
      CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        email VARCHAR(255) UNIQUE NOT NULL,
        password_hash VARCHAR(255),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      );
    `;

    // 記事テーブル
    await sql`
      CREATE TABLE IF NOT EXISTS articles (
        id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users(id),
        title VARCHAR(255) NOT NULL,
        slug VARCHAR(255) UNIQUE NOT NULL,
        content TEXT,
        published BOOLEAN DEFAULT FALSE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      );
    `;

    // タグテーブル
    await sql`
      CREATE TABLE IF NOT EXISTS tags (
        id SERIAL PRIMARY KEY,
        article_id INTEGER REFERENCES articles(id) ON DELETE CASCADE,
        tag VARCHAR(50),
        UNIQUE(article_id, tag)
      );
    `;

    // インデックス作成
    await sql`CREATE INDEX idx_articles_slug ON articles(slug);`;
    await sql`CREATE INDEX idx_articles_user_id ON articles(user_id);`;
    await sql`CREATE INDEX idx_articles_published ON articles(published);`;

    console.log('Migrations completed');
  } catch (error) {
    console.error('Migration failed:', error);
    throw error;
  }
}
```

### 2.3 CRUD 操作

```typescript
// lib/postgres-queries.ts
import { sql } from '@vercel/postgres';

// Create
export async function createUser(email: string, passwordHash: string) {
  const result = await sql`
    INSERT INTO users (email, password_hash)
    VALUES (${email}, ${passwordHash})
    RETURNING id, email, created_at;
  `;
  return result.rows[0];
}

// Read
export async function getUserById(id: number) {
  const result = await sql`
    SELECT id, email, created_at, updated_at
    FROM users
    WHERE id = ${id};
  `;
  return result.rows[0];
}

export async function getUserByEmail(email: string) {
  const result = await sql`
    SELECT id, email, password_hash
    FROM users
    WHERE email = ${email};
  `;
  return result.rows[0];
}

// Update
export async function updateUser(id: number, updates: Record<string, any>) {
  const setClauses = Object.keys(updates)
    .map((key) => `${key} = $${key}`)
    .join(', ');

  const result = await sql`
    UPDATE users
    SET ${sql(setClauses)}, updated_at = CURRENT_TIMESTAMP
    WHERE id = ${id}
    RETURNING id, email, updated_at;
  `;
  return result.rows[0];
}

// Delete
export async function deleteUser(id: number) {
  await sql`DELETE FROM users WHERE id = ${id};`;
}

// List with pagination
export async function getArticles(page: number = 1, pageSize: number = 10) {
  const offset = (page - 1) * pageSize;

  const result = await sql`
    SELECT 
      a.id, a.title, a.slug, a.user_id,
      u.email as author_email,
      COUNT(t.id) as tag_count
    FROM articles a
    LEFT JOIN users u ON a.user_id = u.id
    LEFT JOIN tags t ON a.id = t.article_id
    WHERE a.published = true
    GROUP BY a.id, u.id
    ORDER BY a.created_at DESC
    LIMIT ${pageSize} OFFSET ${offset};
  `;

  const countResult = await sql`
    SELECT COUNT(*) as total FROM articles WHERE published = true;
  `;

  return {
    articles: result.rows,
    total: parseInt(countResult.rows[0].total),
    pages: Math.ceil(parseInt(countResult.rows[0].total) / pageSize),
  };
}
```

### 2.4 トランザクション

```typescript
// lib/transactions.ts
import { sql } from '@vercel/postgres';

export async function createArticleWithTags(
  userId: number,
  title: string,
  content: string,
  tags: string[]
) {
  const client = await sql.connect();

  try {
    await client.query('BEGIN');

    // 記事作成
    const articleResult = await client.query(
      `
      INSERT INTO articles (user_id, title, slug, content)
      VALUES ($1, $2, $3, $4)
      RETURNING id;
      `,
      [userId, title, title.toLowerCase().replace(/\s+/g, '-'), content]
    );

    const articleId = articleResult.rows[0].id;

    // タグ追加
    for (const tag of tags) {
      await client.query(
        `INSERT INTO tags (article_id, tag) VALUES ($1, $2);`,
        [articleId, tag]
      );
    }

    await client.query('COMMIT');

    return { success: true, articleId };
  } catch (error) {
    await client.query('ROLLBACK');
    throw error;
  } finally {
    client.release();
  }
}
```

---

## 3. Vercel Blob Storage

### 3.1 基本セットアップ

```bash
npm install @vercel/blob
```

```typescript
// lib/blob.ts
import { put, del, get, list } from '@vercel/blob';

// アップロード
export async function uploadFile(
  file: File,
  pathname: string
): Promise<{ url: string; downloadUrl: string }> {
  const blob = await put(pathname, file, { access: 'public' });
  return {
    url: blob.url,
    downloadUrl: blob.downloadUrl,
  };
}

// ダウンロード
export async function getFile(pathname: string) {
  const blob = await get(pathname);
  return blob;
}

// 削除
export async function deleteFile(pathname: string) {
  await del(pathname);
}

// リスト
export async function listFiles(prefix: string = '') {
  const blobs = await list({ prefix });
  return blobs.blobs;
}
```

### 3.2 画像アップロード・サムネイル生成

```typescript
// lib/image-upload.ts
import { put } from '@vercel/blob';
import sharp from 'sharp';

export async function uploadImageWithThumbnail(
  file: File,
  userId: string
): Promise<{ original: string; thumbnail: string }> {
  const buffer = await file.arrayBuffer();

  // オリジナル画像アップロード
  const originalBlob = await put(
    `images/${userId}/${file.name}`,
    new Blob([buffer], { type: file.type }),
    { access: 'public' }
  );

  // サムネイル生成
  const thumbnailBuffer = await sharp(buffer)
    .resize(200, 200, { fit: 'cover' })
    .webp({ quality: 80 })
    .toBuffer();

  const thumbnailBlob = await put(
    `images/${userId}/thumb-${file.name}`,
    new Blob([thumbnailBuffer], { type: 'image/webp' }),
    { access: 'public' }
  );

  return {
    original: originalBlob.url,
    thumbnail: thumbnailBlob.url,
  };
}
```

### 3.3 API ルートでの使用

```typescript
// app/api/upload/route.ts
import { uploadFile } from '@/lib/blob';
import { NextRequest, NextResponse } from 'next/server';

export async function POST(req: NextRequest) {
  try {
    const formData = await req.formData();
    const file = formData.get('file') as File;

    if (!file) {
      return NextResponse.json(
        { error: 'No file provided' },
        { status: 400 }
      );
    }

    const pathname = `uploads/${Date.now()}-${file.name}`;
    const blob = await uploadFile(file, pathname);

    return NextResponse.json(blob);
  } catch (error) {
    return NextResponse.json(
      { error: 'Upload failed' },
      { status: 500 }
    );
  }
}
```

---

## 4. キャッシング戦略

### 4.1 多層キャッシュ（CDN + KV + DB）

```typescript
// lib/multi-layer-cache.ts
import { kv } from '@vercel/kv';
import { sql } from '@vercel/postgres';

export async function getDataWithMultiLayerCache(
  key: string,
  fetchFn: () => Promise<any>,
  kvTtl: number = 3600,
  dbTtl: number = 86400
) {
  // L1: KV キャッシュ（最速、秒単位）
  try {
    const cached = await kv.get(`cache:${key}`);
    if (cached) {
      console.log(`L1 Cache hit: ${key}`);
      return JSON.parse(cached as string);
    }
  } catch (error) {
    console.warn(`L1 Cache miss: ${key}`);
  }

  // L2: DB キャッシュ（中速、長期保存）
  try {
    const dbResult = await sql`
      SELECT data, created_at FROM cache_table
      WHERE key = ${key}
      AND created_at > NOW() - INTERVAL '${dbTtl} seconds';
    `;

    if (dbResult.rows.length > 0) {
      const data = dbResult.rows[0].data;
      // L1 に戻す
      await kv.setex(`cache:${key}`, kvTtl, JSON.stringify(data));
      console.log(`L2 Cache hit: ${key}`);
      return data;
    }
  } catch (error) {
    console.warn(`L2 Cache miss: ${key}`);
  }

  // L3: 元データソース（最遅）
  console.log(`L3 Fetch: ${key}`);
  const data = await fetchFn();

  // キャッシュに保存
  await Promise.all([
    kv.setex(`cache:${key}`, kvTtl, JSON.stringify(data)),
    sql`
      INSERT INTO cache_table (key, data)
      VALUES (${key}, ${JSON.stringify(data)})
      ON CONFLICT (key) DO UPDATE SET data = EXCLUDED.data;
    `,
  ]);

  return data;
}
```

### 4.2 キャッシュ無効化戦略

```typescript
// lib/cache-invalidation.ts
import { kv } from '@vercel/kv';
import { sql } from '@vercel/postgres';

export async function invalidateRelatedCaches(patterns: string[]) {
  const keys = await kv.keys('cache:*');

  for (const pattern of patterns) {
    const regex = new RegExp(pattern);
    const toDelete = keys.filter((key) => regex.test(key));

    for (const key of toDelete) {
      await kv.del(key);
    }
  }
}

// 使用例
export async function updateArticle(articleId: number, data: any) {
  // DB 更新
  await sql`UPDATE articles SET ... WHERE id = ${articleId};`;

  // 関連キャッシュを無効化
  await invalidateRelatedCaches([
    `article:${articleId}`,
    `articles:.*`,
    `feed:.*`,
  ]);
}
```

---

## 5. 複合データ設計

### 5.1 ユーザー・記事・コメント システム

```typescript
// lib/models/article.ts
import { sql } from '@vercel/postgres';
import { kv } from '@vercel/kv';

export interface Article {
  id: number;
  title: string;
  slug: string;
  authorId: number;
  content: string;
  published: boolean;
  likes: number;
  createdAt: Date;
  updatedAt: Date;
}

export async function getArticleWithAuthor(slug: string) {
  const cacheKey = `article:${slug}`;

  // キャッシュから取得
  const cached = await kv.get(cacheKey);
  if (cached) {
    return JSON.parse(cached as string);
  }

  // DB から取得
  const result = await sql`
    SELECT 
      a.id, a.title, a.slug, a.content, a.published,
      a.created_at, a.updated_at,
      u.id as author_id, u.email, u.name,
      COUNT(l.id) as likes,
      COUNT(c.id) as comment_count
    FROM articles a
    LEFT JOIN users u ON a.user_id = u.id
    LEFT JOIN likes l ON a.id = l.article_id
    LEFT JOIN comments c ON a.id = c.article_id
    WHERE a.slug = ${slug}
    GROUP BY a.id, u.id;
  `;

  if (result.rows.length === 0) {
    return null;
  }

  const article = result.rows[0];

  // キャッシュに保存（1時間）
  await kv.setex(cacheKey, 3600, JSON.stringify(article));

  return article;
}

export async function getRelatedArticles(slug: string, limit: number = 5) {
  const cacheKey = `related:${slug}`;

  const cached = await kv.get(cacheKey);
  if (cached) {
    return JSON.parse(cached as string);
  }

  // タグベースで関連記事を取得
  const result = await sql`
    SELECT DISTINCT
      a.id, a.title, a.slug, a.created_at
    FROM articles a
    INNER JOIN tags t1 ON a.id = t1.article_id
    INNER JOIN tags t2 ON t1.tag = t2.tag
    INNER JOIN articles a2 ON t2.article_id = a2.id
    WHERE a2.slug = ${slug}
    AND a.id != a2.id
    AND a.published = true
    ORDER BY a.created_at DESC
    LIMIT ${limit};
  `;

  const articles = result.rows;
  await kv.setex(cacheKey, 3600, JSON.stringify(articles));

  return articles;
}
```

---

## 6. 監視・最適化

### 6.1 データベース パフォーマンス監視

```typescript
// lib/monitoring.ts
import { sql } from '@vercel/postgres';
import { kv } from '@vercel/kv';

export async function logQueryPerformance(
  query: string,
  duration: number
) {
  const timestamp = new Date().toISOString();

  // メトリクス保存
  await kv.lpush(
    'metrics:queries',
    JSON.stringify({
      query: query.substring(0, 100),
      duration,
      timestamp,
    })
  );

  // 古いメトリクスを削除（最新1000件を保持）
  await kv.ltrim('metrics:queries', 0, 999);

  // スローログ
  if (duration > 1000) {
    console.warn(`Slow query (${duration}ms): ${query}`);
  }
}

export async function getPerformanceStats() {
  const metrics = await kv.lrange('metrics:queries', 0, -1);

  const parsed = metrics.map((m) => JSON.parse(m as string));

  return {
    count: parsed.length,
    avgDuration: parsed.reduce((sum, m) => sum + m.duration, 0) / parsed.length,
    slowQueries: parsed.filter((m) => m.duration > 500).length,
  };
}
```

### 6.2 ストレージ 監視

```typescript
// lib/storage-monitoring.ts
import { list } from '@vercel/blob';
import { sql } from '@vercel/postgres';

export async function getStorageStats() {
  const blobs = await list();

  let totalSize = 0;
  const byType: Record<string, { count: number; size: number }> = {};

  for (const blob of blobs.blobs) {
    totalSize += blob.size;
    const ext = blob.pathname.split('.').pop() || 'unknown';

    if (!byType[ext]) {
      byType[ext] = { count: 0, size: 0 };
    }
    byType[ext].count++;
    byType[ext].size += blob.size;
  }

  // 統計をログ
  await sql`
    INSERT INTO storage_stats (total_size, by_type, recorded_at)
    VALUES (${totalSize}, ${JSON.stringify(byType)}, CURRENT_TIMESTAMP);
  `;

  return {
    totalSize,
    byType,
    formatted: `${(totalSize / 1024 / 1024).toFixed(2)} MB`,
  };
}
```

---

## 7. エラーハンドリング

### 7.1 再試行ロジック

```typescript
// lib/retry.ts
export async function withRetry<T>(
  fn: () => Promise<T>,
  options: {
    maxRetries?: number;
    delayMs?: number;
    backoff?: boolean;
  } = {}
): Promise<T> {
  const { maxRetries = 3, delayMs = 100, backoff = true } = options;

  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try {
      return await fn();
    } catch (error) {
      if (attempt === maxRetries) {
        throw error;
      }

      const delay = backoff ? delayMs * Math.pow(2, attempt) : delayMs;
      console.log(
        `Retry attempt ${attempt + 1}/${maxRetries} after ${delay}ms`
      );
      await new Promise((resolve) => setTimeout(resolve, delay));
    }
  }

  throw new Error('Retry logic failed');
}

// 使用例
export async function getSafeData(key: string) {
  return withRetry(
    () => kv.get(key),
    { maxRetries: 3, backoff: true }
  );
}
```

### 7.2 エラー分類・ログ

```typescript
// lib/error-handling.ts
export class DatabaseError extends Error {
  constructor(message: string, public code: string) {
    super(message);
  }
}

export class StorageError extends Error {
  constructor(message: string, public code: string) {
    super(message);
  }
}

export function logError(error: Error, context: any) {
  const errorLog = {
    timestamp: new Date().toISOString(),
    message: error.message,
    stack: error.stack,
    context,
  };

  console.error(JSON.stringify(errorLog));

  // 本番環境では外部ロギングサービスに送信
  if (process.env.NODE_ENV === 'production') {
    // Sentry, LogRocket, Datadog等に送信
  }
}
```

---

## 8. 価格最適化

### 8.1 KV 使用量の削減

```
費用削減チェックリスト（KV）:
- [ ] 不要なキャッシュ キー削除戦略実装
- [ ] TTL（Time To Live）を短すぎず設定
- [ ] バッチ操作使用（個別操作より効率的）
- [ ] パイプライン処理で複数操作を一度に
```

```typescript
// パイプライン処理（複数操作を一度に）
export async function batchCacheSet(
  entries: Array<{ key: string; value: any; ttl: number }>
) {
  const pipeline = kv.pipeline();

  for (const entry of entries) {
    pipeline.setex(entry.key, entry.ttl, JSON.stringify(entry.value));
  }

  await pipeline.exec();
}
```

### 8.2 Postgres 最適化

```
費用削減チェックリスト（Postgres）:
- [ ] インデックス設定（クエリ高速化）
- [ ] 不要な行・列の定期削除
- [ ] バッチ挿入（個別より効率的）
- [ ] 接続プーリング設定
- [ ] クエリの N+1 問題解決
```

```typescript
// バッチ挿入
export async function batchInsertUsers(
  users: Array<{ email: string; name: string }>
) {
  const values = users
    .map(
      (u, i) => `('${u.email}', '${u.name}')`
    )
    .join(',');

  await sql`
    INSERT INTO users (email, name) VALUES ${sql.raw(values)};
  `;
}
```

### 8.3 Blob 最適化

```
費用削減チェックリスト（Blob）:
- [ ] 画像圧縮（WebP/AVIF）
- [ ] サムネイル生成で帯域削減
- [ ] 定期的な不要ファイル削除
- [ ] キャッシュ制御ヘッダー設定
```

---

## 📖 関連ドキュメント

- [05_データベース連携.md](./05_データベース連携.md) — 外部DB 統合
- [06_パフォーマンス最適化.md](./06_パフォーマンス最適化.md) — キャッシング基礎
