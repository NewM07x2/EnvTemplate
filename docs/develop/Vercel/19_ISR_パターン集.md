# Vercel Incremental Static Regeneration (ISR) パターン集

> **対象者**: キャッシング戦略を駆使した高速・スケーラブルなサイト構築したい開発者  
> **主要トピック**: ISR 基礎 / Revalidate 戦略 / On-Demand Revalidation / キャッシュ無効化 / ハイブリッドレンダリング

---

## 📚 目次

1. [ISR の基礎](#1-isr-の基礎)
2. [Revalidate 戦略](#2-revalidate-戦略)
3. [On-Demand Revalidation](#3-on-demand-revalidation)
4. [キャッシュ無効化パターン](#4-キャッシュ無効化パターン)
5. [ハイブリッドレンダリング](#5-ハイブリッドレンダリング)
6. [フォールバック戦略](#6-フォールバック戦略)
7. [リージョン別キャッシング](#7-リージョン別キャッシング)
8. [トラブルシューティング](#8-トラブルシューティング)

---

## 1. ISR の基礎

### 1.1 基本的な ISR 実装

```typescript
// app/blog/[slug]/page.tsx
import { revalidatePath } from 'next/cache';
import { getBlogPost } from '@/lib/blog';

export const revalidate = 60; // 60秒ごとに再検証

export async function generateStaticParams() {
  const posts = await getBlogPost('');
  return posts.map((post) => ({
    slug: post.slug,
  }));
}

export default async function BlogPost({
  params,
}: {
  params: { slug: string };
}) {
  const post = await getBlogPost(params.slug);

  return (
    <article>
      <h1>{post.title}</h1>
      <div>{post.content}</div>
      <small>Updated: {post.updatedAt}</small>
    </article>
  );
}
```

### 1.2 複数パラメータの ISR

```typescript
// app/[category]/[slug]/page.tsx
interface Params {
  category: string;
  slug: string;
}

export const revalidate = 3600; // 1時間

export async function generateStaticParams(): Promise<Params[]> {
  const categories = await getCategories();
  
  const params: Params[] = [];
  for (const category of categories) {
    const items = await getItemsByCategory(category);
    params.push(
      ...items.map((item) => ({
        category,
        slug: item.slug,
      }))
    );
  }

  return params;
}

export default async function Page({
  params,
}: {
  params: Params;
}) {
  const item = await getItem(params.category, params.slug);
  return <div>{item.title}</div>;
}
```

### 1.3 動的ルート追加（fallback）

```typescript
// app/products/[id]/page.tsx
export const revalidate = 300; // 5分

export async function generateStaticParams() {
  // 人気の製品のみ事前生成
  const topProducts = await getTopProducts(100);
  return topProducts.map((p) => ({ id: p.id }));
}

export default async function ProductPage({
  params,
}: {
  params: { id: string };
}) {
  try {
    const product = await getProduct(params.id);
    
    if (!product) {
      // 見つからない場合は 404
      return <div>Product not found</div>;
    }

    return (
      <div>
        <h1>{product.name}</h1>
        <p>{product.description}</p>
      </div>
    );
  } catch (error) {
    // フォールバック：キャッシュから返す
    return <div>Loading product...</div>;
  }
}
```

---

## 2. Revalidate 戦略

### 2.1 時間ベース Revalidate

```typescript
// 秒単位で指定
export const revalidate = 60; // 60秒

// 無限キャッシュ
export const revalidate = false;

// リアルタイム（ISR なし）
export const revalidate = 0;
```

### 2.2 コンテンツ特性別の revalidate 設定

```typescript
// app/components/cache-config.ts
export const REVALIDATE_CONFIG = {
  // 静的コンテンツ（変更が少ない）
  STATIC: false,           // 無限キャッシュ
  
  // 準静的（週1回程度の更新）
  SEMI_STATIC: 7 * 86400,  // 7日
  
  // 動的（日1回～数回の更新）
  DYNAMIC: 3600,           // 1時間
  
  // 頻繁に変わる
  FAST_CHANGING: 60,       // 1分
  
  // ほぼリアルタイム
  REALTIME: 0,             // 毎回取得
};

// 使用例
export const revalidate = REVALIDATE_CONFIG.DYNAMIC;
```

### 2.3 エラー時の revalidate 延長

```typescript
// app/dynamic/page.tsx
export const revalidate = 60;

async function fetchDataWithFallback() {
  try {
    return await fetchFromAPI();
  } catch (error) {
    console.error('API error, extending cache');
    
    // エラー時はキャッシュを再利用するよう指示
    // 次の revalidate までは古いデータを返す
    return null;
  }
}
```

---

## 3. On-Demand Revalidation

### 3.1 単一ページの再生成

```typescript
// app/api/revalidate/blog/route.ts
import { revalidatePath } from 'next/cache';
import { NextRequest, NextResponse } from 'next/server';

export async function POST(req: NextRequest) {
  // 認証確認
  const token = req.headers.get('x-revalidate-token');
  
  if (token !== process.env.REVALIDATE_TOKEN) {
    return NextResponse.json(
      { error: 'Invalid token' },
      { status: 401 }
    );
  }

  const { slug } = await req.json();

  try {
    // 特定のパスを再検証
    revalidatePath(`/blog/${slug}`, 'page');
    
    return NextResponse.json({
      revalidated: true,
      now: Date.now(),
      path: `/blog/${slug}`,
    });
  } catch (error) {
    return NextResponse.json(
      { error: 'Revalidation failed' },
      { status: 500 }
    );
  }
}
```

### 3.2 複数ページの一括再生成

```typescript
// app/api/revalidate/bulk/route.ts
import { revalidatePath } from 'next/cache';
import { NextRequest, NextResponse } from 'next/server';

export async function POST(req: NextRequest) {
  const token = req.headers.get('x-revalidate-token');
  
  if (token !== process.env.REVALIDATE_TOKEN) {
    return NextResponse.json(
      { error: 'Invalid token' },
      { status: 401 }
    );
  }

  const { paths, type = 'page' } = await req.json();

  const results = [];

  for (const path of paths) {
    try {
      revalidatePath(path, type);
      results.push({ path, success: true });
    } catch (error) {
      results.push({ path, success: false, error: String(error) });
    }
  }

  return NextResponse.json({
    revalidated: true,
    results,
    timestamp: new Date().toISOString(),
  });
}
```

### 3.3 データベース更新時の自動再生成

```typescript
// lib/db-hooks.ts
export async function updateBlogPost(id: number, data: any) {
  // DB 更新
  const post = await updatePost(id, data);

  // 関連ページを再生成
  try {
    const response = await fetch(
      `${process.env.VERCEL_URL}/api/revalidate/blog`,
      {
        method: 'POST',
        headers: {
          'x-revalidate-token': process.env.REVALIDATE_TOKEN!,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ slug: post.slug }),
      }
    );

    if (!response.ok) {
      console.warn('Revalidation request failed');
    }
  } catch (error) {
    console.error('Failed to trigger revalidation:', error);
  }

  return post;
}
```

### 3.4 Webhook ベースの再生成（CMS 連携）

```typescript
// app/api/webhooks/contentful/route.ts
import { revalidatePath } from 'next/cache';
import { NextRequest, NextResponse } from 'next/server';
import crypto from 'crypto';

function verifyContentfulWebhook(
  body: string,
  signature: string
): boolean {
  const hash = crypto
    .createHmac('sha256', process.env.CONTENTFUL_WEBHOOK_SECRET!)
    .update(body)
    .digest('base64');

  return hash === signature;
}

export async function POST(req: NextRequest) {
  const body = await req.text();
  const signature = req.headers.get('x-contentful-content-management-webhook-signature');

  if (!verifyContentfulWebhook(body, signature!)) {
    return NextResponse.json(
      { error: 'Invalid signature' },
      { status: 403 }
    );
  }

  const data = JSON.parse(body);

  // エンティティタイプに応じた再生成
  switch (data.sys.contentType.sys.id) {
    case 'blogPost':
      revalidatePath(`/blog/${data.fields.slug['en-US']}`);
      break;
    case 'category':
      revalidatePath(`/categories/${data.fields.slug['en-US']}`);
      break;
  }

  return NextResponse.json({ revalidated: true });
}
```

---

## 4. キャッシュ無効化パターン

### 4.1 パターンマッチングによる無効化

```typescript
// lib/revalidate-utils.ts
import { revalidatePath } from 'next/cache';

export async function revalidateByPattern(pattern: string) {
  // ワイルドカード対応
  if (pattern.includes('*')) {
    // /blog/* → すべてのブログページ
    revalidatePath(pattern, 'page');
  } else if (pattern.includes('?')) {
    // 正規表現的なマッチング
    // 実装は Next.js のバージョンに依存
    revalidatePath(pattern, 'page');
  } else {
    // 完全一致
    revalidatePath(pattern, 'page');
  }
}

// 使用例
export async function invalidateRelated(entityType: string, id: number) {
  switch (entityType) {
    case 'post':
      // ブログ記事更新 → 関連ページすべて無効化
      revalidatePath('/blog');
      revalidatePath('/');
      revalidatePath('/sitemap.xml');
      break;

    case 'user':
      // ユーザー更新 → プロフィールページ無効化
      revalidatePath(`/users/${id}`);
      break;

    case 'settings':
      // 設定変更 → サイト全体を無効化
      revalidatePath('/', 'layout');
      break;
  }
}
```

### 4.2 タグベースのキャッシュ管理（実験的）

```typescript
// lib/tagged-cache.ts
// Next.js 14+ の実験的機能
import { unstable_cache } from 'next/cache';

export async function getCachedPost(slug: string) {
  return unstable_cache(
    async () => {
      return await getPost(slug);
    },
    [`post:${slug}`], // キャッシュキー
    {
      tags: ['posts', `post:${slug}`], // タグ
      revalidate: 3600, // 1時間
    }
  )();
}

// API で一括無効化
export async function revalidatePostTags(tags: string[]) {
  // revalidateTag() は Server Action でのみ使用可能
  // または API Route で以下を実装：
  
  // キャッシュキーに対応するタグを削除する
  for (const tag of tags) {
    // キャッシュシステムでタグを削除
  }
}
```

### 4.3 世代管理によるキャッシュバスティング

```typescript
// lib/cache-busting.ts
export function getCacheVersion() {
  return process.env.NEXT_PUBLIC_CACHE_VERSION || '1';
}

export function getImageWithVersion(filename: string) {
  return `/images/${filename}?v=${getCacheVersion()}`;
}

export async function bumpCacheVersion() {
  // 環境変数を更新（CI/CD で実行）
  // または Vercel KV に保存
  
  const newVersion = (parseInt(getCacheVersion()) + 1).toString();
  // キャッシュバージョンを更新
}
```

---

## 5. ハイブリッドレンダリング

### 5.1 ページレベルのハイブリッド

```typescript
// app/dashboard/page.tsx
export const revalidate = 60; // 動的部分は1分

interface PageData {
  staticContent: string;  // ISR キャッシュ
  dynamicContent: string; // リアルタイム
}

async function getStaticContent() {
  // キャッシュ対応 DB クエリ
  return await getStaticData();
}

async function getDynamicContent(userId: string) {
  // キャッシュなし（常に最新）
  return await getUserData(userId);
}

export default async function Dashboard({
  searchParams,
}: {
  searchParams: { userId?: string };
}) {
  const staticContent = await getStaticContent();
  const dynamicContent = await getDynamicContent(searchParams.userId || '');

  return (
    <div>
      {/* ISR でキャッシュ */}
      <section>{staticContent}</section>

      {/* 常に最新 */}
      <section>{dynamicContent}</section>
    </div>
  );
}
```

### 5.2 コンポーネントレベルのハイブリッド

```typescript
// app/components/HybridCard.tsx
// 静的部分
async function StaticCardContent() {
  const data = await getStaticData();
  return <div>{data}</div>;
}

// 動的部分
async function DynamicCardContent({ id }: { id: string }) {
  // no-store で常に最新を取得
  const data = await fetch(`/api/data/${id}`, {
    cache: 'no-store',
  }).then((r) => r.json());

  return <div>{data}</div>;
}

export async function HybridCard({ id }: { id: string }) {
  return (
    <div>
      <StaticCardContent />
      <DynamicCardContent id={id} />
    </div>
  );
}
```

### 5.3 段階的な更新（Stale-While-Revalidate）

```typescript
// app/api/data/route.ts
export async function GET(req: Request) {
  return Response.json(
    { data: 'current' },
    {
      headers: {
        'Cache-Control': 
          'public, s-maxage=60, stale-while-revalidate=86400',
        // キャッシュ：60秒
        // その後24時間は古いデータを返しつつ、バックグラウンドで更新
      },
    }
  );
}
```

---

## 6. フォールバック戦略

### 6.1 生成失敗時のフォールバック

```typescript
// app/fallback/page.tsx
export const revalidate = 60;

export default async function Page({
  params,
}: {
  params: { slug: string };
}) {
  let data;

  try {
    // プライマリデータソース
    data = await fetchPrimarySource(params.slug);
  } catch (primaryError) {
    try {
      // セカンダリデータソース
      data = await fetchSecondarySource(params.slug);
    } catch (secondaryError) {
      // テーシャリデータソース（キャッシュなど）
      data = await fetchCachedData(params.slug);

      if (!data) {
        // すべてのソースが失敗
        return <div>Content unavailable</div>;
      }
    }
  }

  return <div>{data}</div>;
}
```

### 6.2 時間ベースのフォールバック

```typescript
// lib/data-fetching.ts
const CACHE_TIMEOUT = 5000; // 5秒

export async function fetchWithTimeout<T>(
  fn: () => Promise<T>,
  fallback: T
): Promise<T> {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), CACHE_TIMEOUT);

  try {
    return await Promise.race([
      fn(),
      new Promise<T>((_, reject) =>
        setTimeout(() => reject(new Error('Timeout')), CACHE_TIMEOUT)
      ),
    ]);
  } catch (error) {
    console.warn('Fetch timeout, using fallback');
    return fallback;
  } finally {
    clearTimeout(timeoutId);
  }
}
```

---

## 7. リージョン別キャッシング

### 7.1 地域別 revalidate 戦略

```typescript
// middleware.ts
import { NextRequest, NextResponse } from 'next/server';

export function middleware(request: NextRequest) {
  const region = request.headers.get('x-vercel-ip-country');

  const response = NextResponse.next();

  // リージョン別 キャッシュ戦略
  if (region === 'JP') {
    // 日本 → 人気コンテンツのため短いキャッシュ
    response.headers.set(
      'Cache-Control',
      'public, max-age=300, s-maxage=3600'
    );
  } else {
    // その他 → 長いキャッシュ
    response.headers.set(
      'Cache-Control',
      'public, max-age=3600, s-maxage=86400'
    );
  }

  return response;
}
```

### 7.2 言語別キャッシング

```typescript
// app/[lang]/blog/[slug]/page.tsx
export const revalidate = 3600;

interface Params {
  lang: 'en' | 'ja' | 'de';
  slug: string;
}

export async function generateStaticParams(): Promise<Params[]> {
  const languages: Params['lang'][] = ['en', 'ja', 'de'];
  const posts = await getAllPosts();

  const params: Params[] = [];
  for (const lang of languages) {
    for (const post of posts) {
      params.push({ lang, slug: post.slug });
    }
  }

  return params;
}

export default async function Page({ params }: { params: Params }) {
  const post = await getPost(params.lang, params.slug);
  return <article>{post.title}</article>;
}
```

---

## 8. トラブルシューティング

### 8.1 キャッシュが更新されない

```typescript
// デバッグモード
export async function debugRevalidation() {
  // キャッシュの状態を確認
  const debugInfo = {
    timestamp: new Date().toISOString(),
    revalidateValue: 'see_page_exports',
    cachedAt: 'check_x-cache_header',
    message: 'Check _next/static and _next/cache-tags'
  };

  return debugInfo;
}

// 以下を確認：
// 1. x-cache ヘッダー
// 2. x-cache-status ヘッダー
// 3. age ヘッダー
// 4. Vercel ダッシュボードのキャッシュ統計
```

### 8.2 エラーハンドリング

```typescript
// app/error.tsx
'use client';

export default function Error({
  error,
  reset,
}: {
  error: Error;
  reset: () => void;
}) {
  return (
    <div>
      <h2>Something went wrong!</h2>
      <p>{error.message}</p>
      <button onClick={() => reset()}>Try again</button>
      {/* フォールバック内容を表示 */}
      <p>キャッシュから復旧を試行中...</p>
    </div>
  );
}
```

### 8.3 パフォーマンス確認

```bash
# キャッシュヒット率の確認
curl -I https://example.com/blog/post
# x-cache: HIT (キャッシュから返答)
# x-cache: MISS (新規生成)
# age: 123 (キャッシュ経過時間)
```

---

## 📖 関連ドキュメント

- [06_パフォーマンス最適化.md](./06_パフォーマンス最適化.md) — キャッシング基礎
- [13_デプロイ・リリース戦略.md](./13_デプロイ・リリース戦略.md) — デプロイメント管理
