# Vercel Image Optimization・CDN 戦略

> **対象者**: Web UX・パフォーマンスを追求する開発者  
> **主要トピック**: Image Optimization / Responsive Images / WebP・AVIF / CDN 活用 / キャッシング戦略

---

## 📚 目次

1. [Next.js Image コンポーネント](#1-nextjs-image-コンポーネント)
2. [Responsive Images](#2-responsive-images)
3. [画像フォーマット最適化](#3-画像フォーマット最適化)
4. [動的画像生成・変換](#4-動的画像生成変換)
5. [CDN 戦略](#5-cdn-戦略)
6. [キャッシング制御](#6-キャッシング制御)
7. [パフォーマンス監視](#7-パフォーマンス監視)
8. [実装ベストプラクティス](#8-実装ベストプラクティス)

---

## 1. Next.js Image コンポーネント

### 1.1 基本的な使用法

```typescript
// app/components/OptimizedImage.tsx
import Image from 'next/image';

// 静的画像
import staticImage from '@/public/logo.png';

export function OptimizedImage() {
  return (
    <Image
      src={staticImage}
      alt="Logo"
      priority // LCP 候補の場合
      className="w-full h-auto"
    />
  );
}

// 動的画像
export function DynamicOptimizedImage() {
  return (
    <Image
      src="/images/blog-cover.jpg"
      alt="Blog cover"
      width={1200}
      height={630}
      className="w-full h-auto object-cover"
    />
  );
}
```

### 1.2 詳細オプション

```typescript
// 最適化制御
<Image
  src="/photo.jpg"
  alt="Photo"
  width={1200}
  height={800}
  
  // ローディング戦略
  priority={true}  // LCP 候補はこれを指定
  loading="lazy"   // デフォルト。オフスクリーン画像は遅延
  
  // サイズ最適化
  sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
  
  // 品質調整
  quality={75}  // 1-100、デフォルト75
  
  // フォーマット
  unoptimized={false}  // Vercelの最適化を使用
  
  // 外部画像対応
  crossOrigin="anonymous"
  
  // プレースホルダー
  placeholder="blur"
  blurDataURL="data:image/jpeg;base64,..."
/>
```

### 1.3 画像ローダー

```typescript
// next.config.mjs
export default {
  images: {
    // リモート画像ホスト許可
    remotePatterns: [
      { protocol: 'https', hostname: 'cdn.example.com' },
      { protocol: 'https', hostname: '*.cloudinary.com' },
    ],
    
    // デバイスサイズ
    deviceSizes: [640, 750, 828, 1080, 1200, 1920, 2048, 3840],
    
    // 画像サイズ
    imageSizes: [16, 32, 48, 64, 96, 128, 256, 384],
    
    // キャッシュ最大年齢
    minimumCacheTTL: 31536000, // 1年
  },
};
```

### 1.4 カスタムローダー

```typescript
// lib/image-loader.ts
import { ImageLoaderProps } from 'next/image';

export function customImageLoader({
  src,
  width,
  quality,
}: ImageLoaderProps) {
  // Cloudinary を使用
  if (src.startsWith('http')) {
    const params = new URLSearchParams();
    params.set('w', width.toString());
    params.set('q', (quality || 75).toString());
    params.set('f', 'auto');
    
    return `${src}?${params.toString()}`;
  }

  // Vercel CDN を使用
  return `/_next/image?url=${encodeURIComponent(src)}&w=${width}&q=${quality || 75}`;
}

// next.config.mjs
export default {
  images: {
    loader: 'custom',
    loaderFile: './lib/image-loader.ts',
  },
};
```

---

## 2. Responsive Images

### 2.1 Responsive Image コンポーネント

```typescript
// app/components/ResponsiveImage.tsx
import Image from 'next/image';

interface ResponsiveImageProps {
  src: string;
  alt: string;
  aspectRatio?: 'square' | 'video' | '3:2' | '16:9';
}

export function ResponsiveImage({
  src,
  alt,
  aspectRatio = '16:9',
}: ResponsiveImageProps) {
  const aspectRatios = {
    square: 'aspect-square',
    video: 'aspect-video',
    '3:2': 'aspect-[3/2]',
    '16:9': 'aspect-video',
  };

  return (
    <div className={`relative w-full ${aspectRatios[aspectRatio]}`}>
      <Image
        src={src}
        alt={alt}
        fill
        className="object-cover"
        sizes="(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 33vw"
        priority={false}
      />
    </div>
  );
}
```

### 2.2 アートディレクション

```typescript
// app/components/ArtDirectedImage.tsx
import Image from 'next/image';

export function ArtDirectedImage() {
  return (
    <>
      {/* モバイル用（スクエア） */}
      <picture>
        <source 
          srcSet="/images/hero-mobile.jpg" 
          media="(max-width: 640px)" 
        />
        
        {/* タブレット用（3:2） */}
        <source 
          srcSet="/images/hero-tablet.jpg" 
          media="(max-width: 1024px)" 
        />
        
        {/* デスクトップ用（16:9） */}
        <source 
          srcSet="/images/hero-desktop.jpg" 
          media="(min-width: 1024px)" 
        />
        
        {/* フォールバック */}
        <img
          src="/images/hero-desktop.jpg"
          alt="Hero image"
          className="w-full h-auto"
        />
      </picture>
    </>
  );
}
```

### 2.3 プログレッシブ読み込み

```typescript
// app/components/ProgressiveImage.tsx
'use client';

import Image from 'next/image';
import { useState } from 'react';
import clsx from 'clsx';

interface ProgressiveImageProps {
  blurSrc: string;
  src: string;
  alt: string;
}

export function ProgressiveImage({
  blurSrc,
  src,
  alt,
}: ProgressiveImageProps) {
  const [isLoaded, setIsLoaded] = useState(false);

  return (
    <div className="relative">
      {/* ぼかしプレースホルダー */}
      <Image
        src={blurSrc}
        alt={alt}
        width={1200}
        height={630}
        className={clsx(
          'transition-opacity duration-300',
          isLoaded ? 'opacity-0' : 'opacity-100'
        )}
      />

      {/* メイン画像 */}
      <Image
        src={src}
        alt={alt}
        width={1200}
        height={630}
        onLoadingComplete={() => setIsLoaded(true)}
        className={clsx(
          'absolute inset-0 transition-opacity duration-300',
          isLoaded ? 'opacity-100' : 'opacity-0'
        )}
      />
    </div>
  );
}
```

---

## 3. 画像フォーマット最適化

### 3.1 WebP・AVIF サポート

```typescript
// app/components/ModernImageFormats.tsx
import Image from 'next/image';

// Next.js は自動的に WebP/AVIF サポート
export function ModernFormats() {
  return (
    <Image
      src="/photo.jpg"
      alt="Photo"
      width={1200}
      height={630}
      // Vercel が自動的に最適なフォーマットを選択
      // - Chrome → AVIF または WebP
      // - Safari → WebP または JPEG
      // - それ以外 → JPEG
    />
  );
}
```

### 3.2 フォーマット別バリエーション

```typescript
// lib/image-variants.ts
export interface ImageVariant {
  format: 'webp' | 'avif' | 'jpg' | 'png';
  quality: number;
  width: number;
}

export const IMAGE_VARIANTS: ImageVariant[] = [
  { format: 'avif', quality: 70, width: 1200 },
  { format: 'webp', quality: 75, width: 1200 },
  { format: 'jpg', quality: 80, width: 1200 },
];

// Cloudinary URL 構築例
export function buildCloudinaryUrl(
  publicId: string,
  format: ImageVariant
) {
  return `https://res.cloudinary.com/myaccount/image/upload/` +
    `w_${format.width},` +
    `q_${format.quality},` +
    `f_${format.format}/` +
    `${publicId}`;
}
```

### 3.3 画像最適化スクリプト

```bash
#!/bin/bash
# scripts/optimize-images.sh

# ImageMagick を使用
for file in public/images/**/*.jpg; do
  # WebP 変換
  convert "$file" -quality 85 "${file%.jpg}.webp"
  
  # AVIF 変換（cwebp）
  cwebp -q 80 "$file" -o "${file%.jpg}.avif"
  
  # JPEG 最適化
  jpegoptim --max=85 "$file"
done

echo "Image optimization completed"
```

---

## 4. 動的画像生成・変換

### 4.1 サムネイル自動生成

```typescript
// app/api/thumbnails/[id]/route.ts
import sharp from 'sharp';
import { NextRequest, NextResponse } from 'next/server';
import { get } from '@vercel/blob';

export async function GET(
  req: NextRequest,
  { params }: { params: { id: string } }
) {
  try {
    // 元画像を取得
    const blob = await get(`images/${params.id}.jpg`);
    
    if (!blob) {
      return NextResponse.json(
        { error: 'Image not found' },
        { status: 404 }
      );
    }

    const buffer = await blob.arrayBuffer();

    // クエリパラメータで変換設定
    const { searchParams } = req.nextUrl;
    const width = parseInt(searchParams.get('w') || '200');
    const format = searchParams.get('f') || 'webp';

    // 変換処理
    const transformer = sharp(buffer).resize(width, width, {
      fit: 'cover',
      position: 'center',
    });

    let output;
    switch (format) {
      case 'avif':
        output = await transformer.avif({ quality: 75 }).toBuffer();
        break;
      case 'png':
        output = await transformer.png({ compressionLevel: 9 }).toBuffer();
        break;
      case 'webp':
      default:
        output = await transformer.webp({ quality: 80 }).toBuffer();
    }

    return new Response(output, {
      headers: {
        'Content-Type': `image/${format}`,
        'Cache-Control': 'public, max-age=31536000', // 1年
      },
    });
  } catch (error) {
    return NextResponse.json(
      { error: 'Failed to process image' },
      { status: 500 }
    );
  }
}
```

### 4.2 動的 OG 画像生成（既出だが追加例）

```typescript
// app/api/og/posts/[slug]/route.tsx
import { ImageResponse } from '@vercel/og';
import { getPost } from '@/lib/blog';

export const runtime = 'edge';

export async function GET(
  request: Request,
  { params }: { params: { slug: string } }
) {
  const post = await getPost(params.slug);

  return new ImageResponse(
    (
      <div
        style={{
          width: 1200,
          height: 630,
          background: 'linear-gradient(45deg, #667eea 0%, #764ba2 100%)',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          padding: 60,
          fontFamily: '"Noto Sans JP"',
        }}
      >
        <div
          style={{
            fontSize: 60,
            fontWeight: 'bold',
            color: 'white',
            textAlign: 'center',
            marginBottom: 30,
            lineHeight: 1.2,
          }}
        >
          {post.title}
        </div>
        <div style={{ fontSize: 32, color: 'rgba(255,255,255,0.8)' }}>
          {post.author}
        </div>
      </div>
    ),
    { width: 1200, height: 630 }
  );
}
```

---

## 5. CDN 戦略

### 5.1 Vercel CDN の活用

```typescript
// next.config.mjs
export default {
  images: {
    // Vercel の Edge Network を自動利用
    // 全エッジロケーションでキャッシュ
    minimumCacheTTL: 31536000, // 1年
  },
  
  headers: async () => {
    return [
      {
        source: '/images/:path*',
        headers: [
          {
            key: 'Cache-Control',
            value: 'public, max-age=31536000, immutable',
          },
          {
            key: 'CDN-Cache-Control',
            value: 'max-age=31536000',
          },
        ],
      },
    ];
  },
};
```

### 5.2 カスタム CDN 統合（Cloudinary）

```typescript
// next.config.mjs
export default {
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'res.cloudinary.com',
      },
    ],
    loader: 'custom',
    loaderFile: './lib/cloudinary-loader.ts',
  },
};

// lib/cloudinary-loader.ts
export default function cloudinaryLoader({
  src,
  width,
  quality,
}: {
  src: string;
  width: number;
  quality?: number;
}) {
  const params = [
    ['w', width],
    ['q', quality || 75],
    ['f', 'auto'],
  ];

  const querystring = params
    .map(([key, value]) => `${key}_${value}`)
    .join(',');

  return `${src}?${querystring}`;
}
```

### 5.3 リージョン別キャッシング

```typescript
// middleware.ts
import { NextRequest, NextResponse } from 'next/server';

export function middleware(request: NextRequest) {
  const response = NextResponse.next();

  // リージョン別キャッシング戦略
  const region = request.headers.get('x-vercel-ip-country');

  if (request.nextUrl.pathname.startsWith('/images')) {
    if (region === 'JP') {
      // 日本ユーザーは1時間キャッシュ
      response.headers.set('Cache-Control', 'public, max-age=3600');
    } else {
      // その他は24時間キャッシュ
      response.headers.set('Cache-Control', 'public, max-age=86400');
    }
  }

  return response;
}
```

---

## 6. キャッシング制御

### 6.1 キャッシュヘッダー設定

```typescript
// next.config.mjs
export default {
  headers: async () => {
    return [
      // 不変な画像（フィンガープリント）
      {
        source: '/images/_next/:hash/:file',
        headers: [
          {
            key: 'Cache-Control',
            value: 'public, max-age=31536000, immutable',
          },
        ],
      },
      
      // キャッシュバージョン付き
      {
        source: '/api/images/:path*',
        headers: [
          {
            key: 'Cache-Control',
            value: 'public, max-age=86400, s-maxage=31536000',
          },
        ],
      },
      
      // ダイナミック画像
      {
        source: '/api/og/:path*',
        headers: [
          {
            key: 'Cache-Control',
            value: 'public, max-age=3600, s-maxage=86400',
          },
        ],
      },
    ];
  },
};
```

### 6.2 キャッシュバスティング

```typescript
// lib/image-utils.ts
export function getImageUrl(filename: string, version?: string) {
  const query = version ? `?v=${version}` : `?t=${Date.now()}`;
  return `/images/${filename}${query}`;
}

// 使用例
export function getImageWithVersion(filename: string) {
  const version = process.env.NEXT_PUBLIC_IMAGE_VERSION || '1';
  return getImageUrl(filename, version);
}
```

### 6.3 Stale-While-Revalidate

```typescript
// next.config.mjs
export default {
  headers: async () => {
    return [
      {
        source: '/images/:path*',
        headers: [
          {
            key: 'Cache-Control',
            // ブラウザ：1日、CDN：30日、SWR：さらに1日
            value: 'public, max-age=86400, s-maxage=2592000, stale-while-revalidate=86400',
          },
        ],
      },
    ];
  },
};
```

---

## 7. パフォーマンス監視

### 7.1 画像ローディング メトリクス

```typescript
// lib/image-metrics.ts
import { track } from '@vercel/analytics';

export function trackImageMetrics(imageSrc: string, duration: number) {
  track('image_load', {
    src: imageSrc,
    duration: `${duration.toFixed(0)}ms`,
    fast: duration < 500,
  });
}

// コンポーネント内で使用
export function MonitoredImage({
  src,
  alt,
}: {
  src: string;
  alt: string;
}) {
  const startTime = performance.now();

  return (
    <img
      src={src}
      alt={alt}
      onLoad={() => {
        const duration = performance.now() - startTime;
        trackImageMetrics(src, duration);
      }}
    />
  );
}
```

### 7.2 LCP 監視

```typescript
// lib/lcp-monitor.ts
import { getLCP } from 'web-vitals';
import { track } from '@vercel/analytics';

export function monitorLCP() {
  getLCP((metric) => {
    track('lcp', {
      value: metric.value,
      element: metric.attribution?.largestShiftingElementXPath || 'unknown',
    });

    // LCP が画像の場合は追加分析
    if (metric.attribution?.url?.includes('/images')) {
      console.log('Image caused LCP:', metric.attribution.url);
    }
  });
}
```

---

## 8. 実装ベストプラクティス

### 8.1 チェックリスト

```
画像最適化チェックリスト:

基本
- [ ] すべての画像に width・height を指定
- [ ] LCP 候補は priority={true}
- [ ] サイズ属性で責任あるデザイン実装
- [ ] Alt テキストを記入

フォーマット
- [ ] WebP・AVIF サポート確認
- [ ] 品質設定を最適化（JPG:75-85, WebP:75, AVIF:70）
- [ ] 定期的なサイズ削減

パフォーマンス
- [ ] 遅延ローディング活用
- [ ] CDN キャッシュ設定確認
- [ ] LCP < 2.5s を維持
- [ ] CLS < 0.1 に制御
```

### 8.2 最適な画像セットアップ

```typescript
// 完全な例
import Image from 'next/image';

export function OptimizedHeroImage() {
  return (
    <div className="relative w-full aspect-video">
      <Image
        src="/images/hero.jpg"
        alt="Page hero image"
        fill
        className="object-cover"
        priority={true}  // LCP 候補
        quality={80}     // ファイルサイズ最適化
        sizes="(max-width: 640px) 100vw, (max-width: 1024px) 85vw, 1200px"
        placeholder="blur"
        blurDataURL="data:image/jpeg;base64,..."
      />
    </div>
  );
}
```

---

## 📖 関連ドキュメント

- [06_パフォーマンス最適化.md](./06_パフォーマンス最適化.md) — Core Web Vitals
- [15_SEO・メタデータ・OG画像生成.md](./15_SEO・メタデータ・OG画像生成.md) — OG 画像生成
