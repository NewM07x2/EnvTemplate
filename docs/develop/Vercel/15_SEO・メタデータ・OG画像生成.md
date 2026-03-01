# Vercel SEO・メタデータ・OG 画像生成

> **対象者**: Web アプリケーション・ブログプラットフォームの SEO を強化したい開発者  
> **主要トピック**: メタデータ / OG 画像 / Sitemap / Schema.org / SEO 監視

---

## 📚 目次

1. [Next.js Metadata API](#1-nextjs-metadata-api)
2. [Open Graph / Twitter Card](#2-open-graph--twitter-card)
3. [動的 OG 画像生成](#3-動的-og-画像生成)
4. [Sitemap・robots.txt](#4-sitemaprobootstxt)
5. [Schema.org マークアップ](#5-schemaorg-マークアップ)
6. [SEO 監視・分析](#6-seo-監視分析)
7. [構造化データ検証](#7-構造化データ検証)
8. [ベストプラクティス](#8-ベストプラクティス)

---

## 1. Next.js Metadata API

### 1.1 基本メタデータ設定

```typescript
// app/layout.tsx (Next.js 13+)
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'My Awesome App',
  description: 'アプリケーション説明（150字前後推奨）',
  keywords: ['Next.js', 'Vercel', 'SEO'],
  authors: [
    {
      name: 'Author Name',
      url: 'https://example.com',
    },
  ],
  creator: 'Company Name',
  publisher: 'Company Name',
  robots: {
    index: true,
    follow: true,
    nocache: true,
    'max-snippet': -1,
    'max-image-preview': 'large',
    'max-video-preview': -1,
  },
  openGraph: {
    type: 'website',
    locale: 'ja_JP',
    url: 'https://example.com',
    siteName: 'My Site',
    title: 'My Awesome App',
    description: 'アプリケーション説明',
    images: [
      {
        url: 'https://example.com/og-image.png',
        width: 1200,
        height: 630,
        alt: 'My Site OG Image',
      },
    ],
  },
  twitter: {
    card: 'summary_large_image',
    site: '@mysite',
    creator: '@author',
    title: 'My Awesome App',
    description: 'アプリケーション説明',
    images: ['https://example.com/og-image.png'],
  },
  icons: {
    icon: '/favicon.ico',
    apple: '/apple-touch-icon.png',
  },
  manifest: '/site.webmanifest',
  alternates: {
    languages: {
      'en-US': 'https://example.com/en',
      'ja-JP': 'https://example.com/ja',
    },
    canonical: 'https://example.com',
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="ja">
      <head>
        {/* メタデータは自動生成 */}
      </head>
      <body>{children}</body>
    </html>
  );
}
```

### 1.2 動的メタデータ（ページごと）

```typescript
// app/blog/[slug]/page.tsx
import type { Metadata } from 'next';
import { getBlogPost } from '@/lib/blog';

interface Props {
  params: { slug: string };
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const post = await getBlogPost(params.slug);

  if (!post) {
    return {
      title: 'Post Not Found',
    };
  }

  return {
    title: post.title,
    description: post.excerpt,
    authors: [{ name: post.author }],
    publishedTime: post.publishedAt,
    modifiedTime: post.updatedAt,
    openGraph: {
      type: 'article',
      title: post.title,
      description: post.excerpt,
      images: [post.coverImage],
      publishedTime: post.publishedAt,
      authors: [post.author],
    },
    twitter: {
      card: 'summary_large_image',
      title: post.title,
      description: post.excerpt,
      images: [post.coverImage],
    },
  };
}

export default function BlogPost({ params }: Props) {
  // ページコンテンツ
}
```

### 1.3 Pages Router での設定（互換性）

```typescript
// pages/index.tsx
import Head from 'next/head';

export default function Home() {
  return (
    <>
      <Head>
        <title>My Awesome App</title>
        <meta name="description" content="アプリケーション説明" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>
      {/* ページコンテンツ */}
    </>
  );
}
```

---

## 2. Open Graph / Twitter Card

### 2.1 OG メタデータの最適化

```typescript
// lib/og-metadata.ts
export interface OGMetadata {
  title: string;
  description: string;
  image: string;
  url: string;
  type?: 'website' | 'article' | 'video';
  width?: number;
  height?: number;
  locale?: string;
}

export function generateOGMetadata(data: OGMetadata) {
  return {
    openGraph: {
      type: data.type || 'website',
      title: data.title,
      description: data.description,
      url: data.url,
      images: [
        {
          url: data.image,
          width: data.width || 1200,
          height: data.height || 630,
          alt: data.title,
        },
      ],
      locale: data.locale || 'ja_JP',
    },
    twitter: {
      card: 'summary_large_image',
      title: data.title,
      description: data.description,
      images: [data.image],
    },
  };
}
```

### 2.2 SNS シェア最適化

```typescript
// app/article/[id]/page.tsx
import { generateOGMetadata } from '@/lib/og-metadata';

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const article = await getArticle(params.id);

  return generateOGMetadata({
    title: article.title,
    description: article.summary,
    image: article.ogImage,
    url: `${process.env.VERCEL_URL}/article/${params.id}`,
    type: 'article',
  });
}
```

### 2.3 Twitter Card の詳細設定

```typescript
export const metadata: Metadata = {
  twitter: {
    card: 'summary_large_image',  // 大きい画像（1200x628推奨）
    // card: 'summary',  // 小さい画像
    site: '@mycompany',  // サイト アカウント
    creator: '@author',  // 作成者 アカウント
    title: 'タイトル',
    description: '説明文',
    images: ['https://example.com/og-image.png'],
  },
};
```

---

## 3. 動的 OG 画像生成

### 3.1 Vercel OG ライブラリ

```bash
npm install @vercel/og
```

```typescript
// app/api/og/route.tsx
import { ImageResponse } from '@vercel/og';

export const runtime = 'edge';

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const title = searchParams.get('title') || 'Default Title';
  const author = searchParams.get('author') || 'Author';

  return new ImageResponse(
    (
      <div
        style={{
          fontSize: 128,
          background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
          width: '100%',
          height: '100%',
          display: 'flex',
          textAlign: 'center',
          alignItems: 'center',
          justifyContent: 'center',
          flexDirection: 'column',
          color: 'white',
          fontFamily: 'system-ui',
          padding: '40px',
        }}
      >
        <div style={{ fontSize: 88, fontWeight: 'bold', marginBottom: 20 }}>
          {title}
        </div>
        <div style={{ fontSize: 48, opacity: 0.8 }}>
          by {author}
        </div>
      </div>
    ),
    {
      width: 1200,
      height: 630,
    }
  );
}
```

### 3.2 ブログ記事用 OG 画像

```typescript
// app/api/og/blog/route.tsx
import { ImageResponse } from '@vercel/og';
import { getBlogPost } from '@/lib/blog';

export const runtime = 'edge';

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const slug = searchParams.get('slug');

  if (!slug) {
    return new ImageResponse(
      <div style={{ fontSize: 50, color: 'red' }}>Missing slug</div>,
      { width: 1200, height: 630 }
    );
  }

  const post = await getBlogPost(slug);

  return new ImageResponse(
    (
      <div
        style={{
          width: '100%',
          height: '100%',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          background: 'white',
          padding: 60,
          fontFamily: '"Noto Sans JP"',
        }}
      >
        <img
          src={post.authorAvatar}
          style={{
            width: 80,
            height: 80,
            borderRadius: '50%',
            marginBottom: 20,
          }}
        />
        <div
          style={{
            fontSize: 60,
            fontWeight: 'bold',
            textAlign: 'center',
            marginBottom: 30,
            color: '#333',
          }}
        >
          {post.title}
        </div>
        <div
          style={{
            fontSize: 32,
            color: '#666',
            marginBottom: 30,
          }}
        >
          {post.excerpt}
        </div>
        <div
          style={{
            fontSize: 24,
            color: '#999',
          }}
        >
          {post.author} • {new Date(post.publishedAt).toLocaleDateString('ja-JP')}
        </div>
      </div>
    ),
    {
      width: 1200,
      height: 630,
    }
  );
}
```

### 3.3 メタデータで動的 OG 画像を参照

```typescript
// app/blog/[slug]/page.tsx
export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const post = await getBlogPost(params.slug);

  const ogImageUrl = `/api/og/blog?slug=${params.slug}`;

  return {
    title: post.title,
    description: post.excerpt,
    openGraph: {
      type: 'article',
      title: post.title,
      description: post.excerpt,
      images: [
        {
          url: ogImageUrl,
          width: 1200,
          height: 630,
          alt: post.title,
        },
      ],
    },
  };
}
```

---

## 4. Sitemap・robots.txt

### 4.1 動的 Sitemap 生成

```typescript
// app/sitemap.ts
import type { MetadataRoute } from 'next';
import { getAllBlogPosts } from '@/lib/blog';

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const baseUrl = 'https://example.com';

  // 静的ページ
  const staticPages: MetadataRoute.Sitemap = [
    {
      url: baseUrl,
      lastModified: new Date(),
      changeFrequency: 'weekly',
      priority: 1,
    },
    {
      url: `${baseUrl}/blog`,
      lastModified: new Date(),
      changeFrequency: 'daily',
      priority: 0.8,
    },
    {
      url: `${baseUrl}/about`,
      lastModified: new Date(),
      changeFrequency: 'monthly',
      priority: 0.5,
    },
  ];

  // 動的ページ（ブログ記事）
  const posts = await getAllBlogPosts();
  const dynamicPages: MetadataRoute.Sitemap = posts.map(post => ({
    url: `${baseUrl}/blog/${post.slug}`,
    lastModified: new Date(post.updatedAt),
    changeFrequency: 'monthly' as const,
    priority: 0.7,
  }));

  return [...staticPages, ...dynamicPages];
}
```

### 4.2 robots.txt

```typescript
// app/robots.ts
import type { MetadataRoute } from 'next';

export default function robots(): MetadataRoute.Robots {
  return {
    rules: [
      {
        userAgent: '*',
        allow: '/',
        disallow: ['/admin', '/api', '/private'],
      },
      {
        userAgent: 'GPTBot',  // ChatGPT web crawler
        disallow: '/',
      },
    ],
    sitemap: 'https://example.com/sitemap.xml',
  };
}
```

### 4.3 RSS フィード（オプション）

```typescript
// app/feed.xml/route.ts
import { getAllBlogPosts } from '@/lib/blog';

export async function GET() {
  const posts = await getAllBlogPosts();

  const rssContent = `<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:content="http://purl.org/rss/1.0/modules/content/">
  <channel>
    <title>My Blog</title>
    <link>https://example.com</link>
    <description>Latest posts</description>
    ${posts
      .map(
        post => `
      <item>
        <title>${post.title}</title>
        <link>https://example.com/blog/${post.slug}</link>
        <description>${post.excerpt}</description>
        <pubDate>${new Date(post.publishedAt).toUTCString()}</pubDate>
        <content:encoded><![CDATA[${post.content}]]></content:encoded>
      </item>
    `
      )
      .join('')}
  </channel>
</rss>`;

  return new Response(rssContent, {
    headers: {
      'Content-Type': 'application/xml',
      'Cache-Control': 'public, max-age=3600',
    },
  });
}
```

---

## 5. Schema.org マークアップ

### 5.1 Article Schema

```typescript
// app/blog/[slug]/page.tsx
import { ArticleJsonLd } from 'next-seo';

export default function BlogPost({ params }: Props) {
  const post = await getBlogPost(params.slug);

  return (
    <>
      <ArticleJsonLd
        url={`${process.env.VERCEL_URL}/blog/${params.slug}`}
        title={post.title}
        images={[post.coverImage]}
        datePublished={post.publishedAt}
        dateModified={post.updatedAt}
        authorName={post.author}
        description={post.excerpt}
      />
      {/* ページコンテンツ */}
    </>
  );
}
```

### 5.2 Organization Schema

```typescript
// app/layout.tsx
import { OrganizationJsonLd } from 'next-seo';

export default function RootLayout({ children }) {
  return (
    <>
      <OrganizationJsonLd
        type="Organization"
        id="https://example.com"
        name="Company Name"
        logo="https://example.com/logo.png"
        url="https://example.com"
        phone="+81-xx-xxxx-xxxx"
        email="contact@example.com"
        address={{
          streetAddress: '123 Main St',
          addressLocality: 'Tokyo',
          addressRegion: 'JP',
          postalCode: '100-0001',
          addressCountry: 'JP',
        }}
        sameAs={[
          'https://twitter.com/mycompany',
          'https://facebook.com/mycompany',
        ]}
      />
      {/* ページ */}
    </>
  );
}
```

### 5.3 製品・サービス Schema

```typescript
// app/products/[id]/page.tsx
export function generateJsonLD(product) {
  return {
    '@context': 'https://schema.org',
    '@type': 'Product',
    name: product.name,
    description: product.description,
    image: product.image,
    brand: {
      '@type': 'Brand',
      name: 'My Brand',
    },
    offers: {
      '@type': 'Offer',
      price: product.price,
      priceCurrency: 'JPY',
      availability: 'https://schema.org/InStock',
    },
    aggregateRating: {
      '@type': 'AggregateRating',
      ratingValue: product.rating,
      reviewCount: product.reviewCount,
    },
  };
}
```

---

## 6. SEO 監視・分析

### 6.1 Google Search Console 統合

```typescript
// public/google-site-verification.html
<!-- Google Search Console 確認用 -->
<meta name="google-site-verification" content="xxxxxxxxxxxx" />
```

```typescript
// app/layout.tsx
export const metadata: Metadata = {
  verification: {
    google: 'xxxxxxxxxxxx',
  },
};
```

### 6.2 Google Analytics 統合

```bash
npm install @react-google-analytics/core
```

```typescript
// app/layout.tsx
import { GoogleAnalytics } from '@react-google-analytics/core';

export default function RootLayout({ children }) {
  return (
    <html>
      <head>
        <GoogleAnalytics trackingId={process.env.NEXT_PUBLIC_GA_ID} />
      </head>
      <body>{children}</body>
    </html>
  );
}
```

### 6.3 Web Vitals 監視

```typescript
// app/layout.tsx
import { Analytics } from '@vercel/analytics/react';

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        {children}
        <Analytics />
      </body>
    </html>
  );
}
```

### 6.4 リッチスニペット テスト

```typescript
// pages/seo/test.tsx
import Head from 'next/head';

export default function SEOTest() {
  return (
    <Head>
      <title>SEO Test</title>
      <script type="application/ld+json">
        {JSON.stringify({
          '@context': 'https://schema.org',
          '@type': 'Organization',
          name: 'Example.com',
          url: 'https://example.com',
        })}
      </script>
    </Head>
  );
}
```

---

## 7. 構造化データ検証

### 7.1 JSON-LD バリデーション

```bash
# オンラインツール
https://search.google.com/test/rich-results
https://validator.schema.org/
```

### 7.2 自動バリデーション

```typescript
// lib/validate-schema.ts
export function validateSchema(jsonLD: any) {
  // Schema.org 仕様に従っているか確認
  const requiredFields = ['@context', '@type'];
  return requiredFields.every(field => field in jsonLD);
}
```

---

## 8. ベストプラクティス

### 8.1 SEO チェックリスト

```
メタデータ
- [ ] title タグ（50-60文字）
- [ ] description（120-160文字）
- [ ] keywords（3-5個）
- [ ] canonical URL

Open Graph
- [ ] og:title
- [ ] og:description
- [ ] og:image（1200x630px）
- [ ] og:url

Schema.org
- [ ] Organization Schema
- [ ] Article Schema（ブログ）
- [ ] Product Schema（製品ページ）

技術的 SEO
- [ ] robots.txt
- [ ] sitemap.xml
- [ ] Structured data markup
- [ ] Mobile responsive
- [ ] Fast loading (< 2.5s LCP)

その他
- [ ] Internal links
- [ ] Heading hierarchy (H1 → H2 → H3)
- [ ] Image alt text
- [ ] 404 ページ最適化
```

### 8.2 ページごと最適化例

```typescript
// 完全な例
export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const post = await getBlogPost(params.slug);

  const ogUrl = `${process.env.VERCEL_URL}/api/og/blog?slug=${params.slug}`;
  const canonicalUrl = `${process.env.VERCEL_URL}/blog/${params.slug}`;

  return {
    title: post.title,  // 50-60字
    description: post.excerpt,  // 120-160字
    keywords: post.tags,
    alternates: {
      canonical: canonicalUrl,
    },
    openGraph: {
      type: 'article',
      title: post.title,
      description: post.excerpt,
      url: canonicalUrl,
      images: [ogUrl],
      publishedTime: post.publishedAt,
      modifiedTime: post.updatedAt,
      authors: [post.author],
    },
    twitter: {
      card: 'summary_large_image',
      title: post.title,
      description: post.excerpt,
      images: [ogUrl],
    },
    robots: {
      index: true,
      follow: true,
    },
  };
}
```

---

## 📖 関連ドキュメント

- [06_パフォーマンス最適化.md](./06_パフォーマンス最適化.md) — Core Web Vitals
- [01_基本情報.md](./01_基本情報.md) — Next.js フレームワーク
