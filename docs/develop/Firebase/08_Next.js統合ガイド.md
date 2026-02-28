# Next.js × Firebase 統合ガイド

> **レベル**: ★★★ / 所要時間: 約 60 分  
> **前提**: [クイックスタート](02_クイックスタート.md) と [Authentication ガイド](03_Authentication（認証）ガイド.md) の完了推奨

---

## 目次

- [Next.js × Firebase 統合ガイド](#nextjs--firebase-統合ガイド)
  - [目次](#目次)
  - [1. App Router における Firebase の注意点](#1-app-router-における-firebase-の注意点)
  - [2. Firebase 初期化パターン（シングルトン）](#2-firebase-初期化パターンシングルトン)
    - [Client SDK（`src/lib/firebase/client.ts`）](#client-sdksrclibfirebaseclientts)
    - [Admin SDK（`src/lib/firebase/admin.ts`）](#admin-sdksrclibfirebaseadmints)
  - [3. Server Components での Firestore アクセス](#3-server-components-での-firestore-アクセス)
  - [4. Client Components での Firebase 利用](#4-client-components-での-firebase-利用)
    - [Server Component と Client Component の組み合わせ](#server-component-と-client-component-の組み合わせ)
  - [5. Route Handler（API Routes）での Admin SDK 利用](#5-route-handlerapi-routesでの-admin-sdk-利用)
    - [クライアント側から Route Handler を呼ぶ](#クライアント側から-route-handler-を呼ぶ)
  - [6. Server Actions × Firebase](#6-server-actions--firebase)
  - [7. 認証状態に基づく Middleware でのルート保護](#7-認証状態に基づく-middleware-でのルート保護)
    - [セッション Cookie の発行（Route Handler）](#セッション-cookie-の発行route-handler)
    - [Middleware でのルート保護](#middleware-でのルート保護)
  - [8. SSG / ISR との組み合わせ](#8-ssg--isr-との組み合わせ)
    - [generateStaticParams との組み合わせ（SSG）](#generatestaticparams-との組み合わせssg)
    - [ISR（Incremental Static Regeneration）](#isrincremental-static-regeneration)
  - [9. 環境変数の管理](#9-環境変数の管理)
  - [10. よくある落とし穴と対策](#10-よくある落とし穴と対策)
    - [❌ Server Component で Client SDK をインポート](#-server-component-で-client-sdk-をインポート)
    - [❌ firebase-admin を Client Component でインポート](#-firebase-admin-を-client-component-でインポート)
    - [❌ `useEffect` なしで `onSnapshot` を呼ぶ](#-useeffect-なしで-onsnapshot-を呼ぶ)
    - [❌ Admin SDK の重複初期化](#-admin-sdk-の重複初期化)
    - [❌ ID トークンをキャッシュせずに毎回待つ](#-id-トークンをキャッシュせずに毎回待つ)
  - [まとめ](#まとめ)
  - [次のステップ](#次のステップ)

---

## 1. App Router における Firebase の注意点

Next.js 13+ の App Router では、デフォルトで全コンポーネントが **Server Component** として扱われます。Firebase Client SDK はブラウザ環境専用のため、以下の使い分けが必要です。

```
┌──────────────────────────────────────────────────────────┐
│                   Next.js App Router                      │
│                                                            │
│  Server Component          Client Component               │
│  ─────────────────         ─────────────────              │
│  Firebase Admin SDK   ←→   Firebase Client SDK            │
│  （Node.js 専用）           （'use client' が必要）         │
│                                                            │
│  使用場所:                  使用場所:                       │
│  ・page.tsx（初期値取得）   ・useState/useEffect あり      │
│  ・Route Handler            ・onSnapshot（リアルタイム）   │
│  ・Server Actions           ・signIn / signOut             │
└──────────────────────────────────────────────────────────┘
```

| SDK | 実行場所 | 認証情報 | 主な用途 |
|-----|---------|---------|---------|
| **Firebase Client SDK** (`firebase`) | ブラウザ | ユーザー権限（RLS/セキュリティルール適用） | 認証、リアルタイム同期、クライアント操作 |
| **Firebase Admin SDK** (`firebase-admin`) | サーバー（Node.js） | サービスアカウント（管理者権限） | サーバーサイドデータ取得、ID トークン検証 |

---

## 2. Firebase 初期化パターン（シングルトン）

### Client SDK（`src/lib/firebase/client.ts`）

```typescript
import { initializeApp, getApps, getApp, type FirebaseApp } from 'firebase/app';
import { getAuth, type Auth } from 'firebase/auth';
import { getFirestore, type Firestore } from 'firebase/firestore';
import { getStorage, type FirebaseStorage } from 'firebase/storage';

const firebaseConfig = {
  apiKey:            process.env.NEXT_PUBLIC_FIREBASE_API_KEY!,
  authDomain:        process.env.NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN!,
  projectId:         process.env.NEXT_PUBLIC_FIREBASE_PROJECT_ID!,
  storageBucket:     process.env.NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET!,
  messagingSenderId: process.env.NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID!,
  appId:             process.env.NEXT_PUBLIC_FIREBASE_APP_ID!,
};

// シングルトン: 開発時のホットリロードで重複初期化を防ぐ
function createFirebaseApp(): FirebaseApp {
  return getApps().length > 0 ? getApp() : initializeApp(firebaseConfig);
}

const app = createFirebaseApp();

export const auth: Auth            = getAuth(app);
export const db: Firestore         = getFirestore(app);
export const storage: FirebaseStorage = getStorage(app);
```

### Admin SDK（`src/lib/firebase/admin.ts`）

```typescript
import { initializeApp, getApps, cert, type App } from 'firebase-admin/app';
import { getAuth } from 'firebase-admin/auth';
import { getFirestore } from 'firebase-admin/firestore';

function createAdminApp(): App {
  if (getApps().length > 0) return getApps()[0];

  return initializeApp({
    credential: cert({
      projectId:   process.env.FIREBASE_ADMIN_PROJECT_ID!,
      clientEmail: process.env.FIREBASE_ADMIN_CLIENT_EMAIL!,
      // 改行文字のエスケープ解除
      privateKey:  process.env.FIREBASE_ADMIN_PRIVATE_KEY!.replace(/\\n/g, '\n'),
    }),
  });
}

createAdminApp();

export const adminAuth = getAuth();
export const adminDb   = getFirestore();
```

> **ポイント**: `firebase-admin` は `'use client'` コンポーネントからは絶対にインポートしない。

---

## 3. Server Components での Firestore アクセス

Server Component では Admin SDK を使ってサーバーサイドでデータを取得し、HTML として返します。

```typescript
// app/posts/page.tsx（Server Component）
import { adminDb } from '@/lib/firebase/admin';

type Post = {
  id: string;
  title: string;
  content: string;
  createdAt: FirebaseFirestore.Timestamp;
};

export default async function PostsPage() {
  // サーバーサイドで Firestore からデータ取得
  const snapshot = await adminDb
    .collection('posts')
    .orderBy('createdAt', 'desc')
    .limit(10)
    .get();

  const posts: Post[] = snapshot.docs.map((doc) => ({
    id: doc.id,
    ...(doc.data() as Omit<Post, 'id'>),
  }));

  return (
    <ul>
      {posts.map((post) => (
        <li key={post.id}>
          <h2>{post.title}</h2>
          <p>{post.content}</p>
        </li>
      ))}
    </ul>
  );
}
```

> **メリット**: ページの初期表示が速い（SEO に有利）。セキュリティルールではなく Admin 権限でアクセスするため、サービスアカウントキーを厳重に管理すること。

---

## 4. Client Components での Firebase 利用

リアルタイム同期やユーザー操作が必要な部分は Client Component に切り出します。

```typescript
// components/PostList.tsx
'use client';

import { useEffect, useState } from 'react';
import { collection, query, orderBy, onSnapshot, type QuerySnapshot } from 'firebase/firestore';
import { db } from '@/lib/firebase/client';

type Post = { id: string; title: string; content: string };

export function PostList() {
  const [posts, setPosts]   = useState<Post[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const q = query(collection(db, 'posts'), orderBy('createdAt', 'desc'));

    // リアルタイム購読
    const unsubscribe = onSnapshot(q, (snapshot: QuerySnapshot) => {
      const data = snapshot.docs.map((doc) => ({
        id: doc.id,
        ...(doc.data() as Omit<Post, 'id'>),
      }));
      setPosts(data);
      setLoading(false);
    });

    // クリーンアップ: コンポーネントのアンマウント時に購読解除
    return () => unsubscribe();
  }, []);

  if (loading) return <p>読み込み中...</p>;

  return (
    <ul>
      {posts.map((post) => (
        <li key={post.id}>{post.title}</li>
      ))}
    </ul>
  );
}
```

### Server Component と Client Component の組み合わせ

```typescript
// app/posts/page.tsx（Server Component）
import { PostList } from '@/components/PostList'; // Client Component

export default function PostsPage() {
  return (
    <main>
      <h1>投稿一覧</h1>
      {/* リアルタイム部分だけ Client Component に委譲 */}
      <PostList />
    </main>
  );
}
```

---

## 5. Route Handler（API Routes）での Admin SDK 利用

`app/api/` 配下の Route Handler はサーバーサイドで実行されるため、Admin SDK を安全に使用できます。

```typescript
// app/api/posts/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { adminAuth, adminDb } from '@/lib/firebase/admin';

export async function GET(request: NextRequest) {
  // Authorization ヘッダーから ID トークンを取得
  const authorization = request.headers.get('Authorization');
  if (!authorization?.startsWith('Bearer ')) {
    return NextResponse.json({ error: '認証が必要です' }, { status: 401 });
  }

  const idToken = authorization.split('Bearer ')[1];

  try {
    // ID トークンを検証してユーザー情報を取得
    const decodedToken = await adminAuth.verifyIdToken(idToken);
    const uid = decodedToken.uid;

    // ユーザーの投稿を取得
    const snapshot = await adminDb
      .collection('posts')
      .where('authorId', '==', uid)
      .get();

    const posts = snapshot.docs.map((doc) => ({
      id: doc.id,
      ...doc.data(),
    }));

    return NextResponse.json({ posts });
  } catch {
    return NextResponse.json({ error: 'トークンが無効です' }, { status: 401 });
  }
}

export async function POST(request: NextRequest) {
  const authorization = request.headers.get('Authorization');
  if (!authorization?.startsWith('Bearer ')) {
    return NextResponse.json({ error: '認証が必要です' }, { status: 401 });
  }

  const idToken = authorization.split('Bearer ')[1];

  try {
    const decodedToken = await adminAuth.verifyIdToken(idToken);
    const body = await request.json();

    const docRef = await adminDb.collection('posts').add({
      ...body,
      authorId:  decodedToken.uid,
      createdAt: new Date(),
    });

    return NextResponse.json({ id: docRef.id }, { status: 201 });
  } catch {
    return NextResponse.json({ error: 'トークンが無効です' }, { status: 401 });
  }
}
```

### クライアント側から Route Handler を呼ぶ

```typescript
// lib/api/posts.ts
import { auth } from '@/lib/firebase/client';

export async function fetchMyPosts() {
  const user = auth.currentUser;
  if (!user) throw new Error('ログインが必要です');

  // 最新の ID トークンを取得（有効期限 1 時間のため毎回取得を推奨）
  const idToken = await user.getIdToken();

  const response = await fetch('/api/posts', {
    headers: { Authorization: `Bearer ${idToken}` },
  });

  if (!response.ok) throw new Error('取得に失敗しました');
  return response.json();
}
```

---

## 6. Server Actions × Firebase

Next.js 14+ の Server Actions でも Admin SDK を利用できます。

```typescript
// app/posts/actions.ts
'use server';

import { revalidatePath } from 'next/cache';
import { cookies } from 'next/headers';
import { adminAuth, adminDb } from '@/lib/firebase/admin';

export async function createPost(formData: FormData) {
  // セッション Cookie から認証（後述の Cookie ベース認証を参照）
  const cookieStore = await cookies();
  const sessionCookie = cookieStore.get('session')?.value;
  if (!sessionCookie) throw new Error('未認証です');

  const decodedClaims = await adminAuth.verifySessionCookie(sessionCookie, true);

  const title   = formData.get('title') as string;
  const content = formData.get('content') as string;

  await adminDb.collection('posts').add({
    title,
    content,
    authorId:  decodedClaims.uid,
    createdAt: new Date(),
  });

  // キャッシュを再検証して画面を更新
  revalidatePath('/posts');
}
```

```tsx
// app/posts/new/page.tsx
import { createPost } from '../actions';

export default function NewPostPage() {
  return (
    <form action={createPost}>
      <input  name="title"   placeholder="タイトル" required />
      <textarea name="content" placeholder="本文"   required />
      <button type="submit">投稿する</button>
    </form>
  );
}
```

---

## 7. 認証状態に基づく Middleware でのルート保護

Firebase の ID トークンは Cookie に保存し、`middleware.ts` でサーバーサイドに検証することでリダイレクトを高速化できます。

### セッション Cookie の発行（Route Handler）

```typescript
// app/api/auth/session/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { adminAuth } from '@/lib/firebase/admin';

// ログイン時にセッション Cookie を発行
export async function POST(request: NextRequest) {
  const { idToken } = await request.json();

  // セッション Cookie の有効期限（最大 14 日）
  const expiresIn = 60 * 60 * 24 * 5 * 1000; // 5日間

  try {
    const sessionCookie = await adminAuth.createSessionCookie(idToken, { expiresIn });

    const response = NextResponse.json({ status: 'success' });
    response.cookies.set('session', sessionCookie, {
      maxAge:   expiresIn / 1000,
      httpOnly: true,
      secure:   process.env.NODE_ENV === 'production',
      path:     '/',
      sameSite: 'lax',
    });

    return response;
  } catch {
    return NextResponse.json({ error: 'セッション作成に失敗しました' }, { status: 401 });
  }
}

// ログアウト時にセッション Cookie を削除
export async function DELETE() {
  const response = NextResponse.json({ status: 'success' });
  response.cookies.delete('session');
  return response;
}
```

### Middleware でのルート保護

```typescript
// middleware.ts（プロジェクトルート）
import { NextRequest, NextResponse } from 'next/server';

// 認証が必要なパスのパターン
const PROTECTED_PATHS = ['/dashboard', '/profile', '/settings'];
const AUTH_PATHS      = ['/login', '/signup'];

export async function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;
  const sessionCookie = request.cookies.get('session')?.value;

  const isProtectedPath = PROTECTED_PATHS.some((p) => pathname.startsWith(p));
  const isAuthPath      = AUTH_PATHS.some((p) => pathname.startsWith(p));

  // 保護ルートへのアクセスにセッションがない場合はログインへ
  if (isProtectedPath && !sessionCookie) {
    return NextResponse.redirect(new URL('/login', request.url));
  }

  // ログイン済みでログインページへのアクセスはダッシュボードへ
  if (isAuthPath && sessionCookie) {
    return NextResponse.redirect(new URL('/dashboard', request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: [
    '/((?!api|_next/static|_next/image|favicon.ico).*)',
  ],
};
```

> **注意**: Middleware では `firebase-admin` を直接使えません（Edge Runtime 非対応）。Cookie の存在確認のみ行い、ページ内またはRoute Handlerで詳細な検証を行います。

---

## 8. SSG / ISR との組み合わせ

### generateStaticParams との組み合わせ（SSG）

```typescript
// app/posts/[id]/page.tsx
import { adminDb } from '@/lib/firebase/admin';

// ビルド時にすべての投稿 ID を取得
export async function generateStaticParams() {
  const snapshot = await adminDb.collection('posts').get();
  return snapshot.docs.map((doc) => ({ id: doc.id }));
}

// ビルド時にデータを取得してページを静的生成
export default async function PostPage({ params }: { params: { id: string } }) {
  const doc = await adminDb.collection('posts').doc(params.id).get();
  if (!doc.exists) return <p>投稿が見つかりません</p>;

  const post = doc.data()!;

  return (
    <article>
      <h1>{post.title}</h1>
      <p>{post.content}</p>
    </article>
  );
}
```

### ISR（Incremental Static Regeneration）

```typescript
// app/posts/[id]/page.tsx
// revalidate を設定することで一定時間後に再生成
export const revalidate = 60; // 60 秒ごとに再検証

export default async function PostPage({ params }: { params: { id: string } }) {
  // ...（上記と同様）
}
```

---

## 9. 環境変数の管理

```bash
# .env.local（ローカル開発用・Git 管理外）

# ── Client SDK（ブラウザに公開される） ──────────────────────
NEXT_PUBLIC_FIREBASE_API_KEY=AIza...
NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN=my-app.firebaseapp.com
NEXT_PUBLIC_FIREBASE_PROJECT_ID=my-app
NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET=my-app.appspot.com
NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID=123456789
NEXT_PUBLIC_FIREBASE_APP_ID=1:123456789:web:abc...

# ── Admin SDK（サーバーサイドのみ・絶対に公開しない） ────────
FIREBASE_ADMIN_PROJECT_ID=my-app
FIREBASE_ADMIN_CLIENT_EMAIL=firebase-adminsdk-xxxxx@my-app.iam.gserviceaccount.com
FIREBASE_ADMIN_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\nMIIEvQ...\n-----END PRIVATE KEY-----\n"
```

| 変数名 | 使用場所 | Git 管理 |
|-------|---------|---------|
| `NEXT_PUBLIC_*` | ブラウザ・サーバー両方 | ❌ しない |
| `FIREBASE_ADMIN_*` | サーバーサイドのみ | ❌ しない |

> **Vercel/本番環境**: Vercel ダッシュボードの Environment Variables に直接入力。`FIREBASE_ADMIN_PRIVATE_KEY` は改行を `\n` のまま貼り付けてOK（Vercel が自動処理）。

---

## 10. よくある落とし穴と対策

### ❌ Server Component で Client SDK をインポート

```typescript
// app/posts/page.tsx ← Server Component
// NG: Client SDK を Server Component で使うとビルドエラーになる
import { db } from '@/lib/firebase/client'; // ← エラー!
```

```typescript
// ✅ Admin SDK を使う
import { adminDb } from '@/lib/firebase/admin';
```

---

### ❌ firebase-admin を Client Component でインポート

```typescript
'use client';
// NG: サービスアカウントキーが漏洩する重大なセキュリティリスク
import { adminDb } from '@/lib/firebase/admin'; // ← 絶対NG!
```

---

### ❌ `useEffect` なしで `onSnapshot` を呼ぶ

```typescript
'use client';
// NG: レンダリングのたびにリスナーが増殖する
const unsubscribe = onSnapshot(q, (snap) => { ... });
```

```typescript
'use client';
// ✅ useEffect 内でクリーンアップ
useEffect(() => {
  const unsubscribe = onSnapshot(q, (snap) => { ... });
  return () => unsubscribe(); // ← 必須
}, []);
```

---

### ❌ Admin SDK の重複初期化

```typescript
// NG: 毎回 initializeApp() を呼ぶと「already exists」エラー
initializeApp({ credential: cert({ ... }) });
```

```typescript
// ✅ シングルトンパターン
if (getApps().length === 0) {
  initializeApp({ credential: cert({ ... }) });
}
```

---

### ❌ ID トークンをキャッシュせずに毎回待つ

```typescript
// NG: await の連鎖で UX が悪化する
const idToken = await user.getIdToken(); // 有効期限チェック・更新で遅延
const res = await fetch('/api/data', { headers: { Authorization: `Bearer ${idToken}` } });
```

```typescript
// ✅ 強制リフレッシュは必要な場合のみ
// getIdToken(false) = キャッシュを利用（デフォルト）
// getIdToken(true)  = 強制リフレッシュ（有効期限切れ疑いのとき）
const idToken = await user.getIdToken(false);
```

---

## まとめ

| 状況 | 使用する SDK | ファイル |
|-----|------------|---------|
| Server Component でデータ取得 | Admin SDK | `lib/firebase/admin.ts` |
| Route Handler でデータ取得・検証 | Admin SDK | `lib/firebase/admin.ts` |
| Server Action でデータ操作 | Admin SDK | `lib/firebase/admin.ts` |
| Client Component でリアルタイム同期 | Client SDK | `lib/firebase/client.ts` |
| Client Component で認証操作 | Client SDK | `lib/firebase/client.ts` |
| Middleware でのルート保護 | Cookie のみ確認（SDK 不使用） | `middleware.ts` |

---

## 次のステップ

- [セキュリティルール詳細ガイド](09_セキュリティルール詳細ガイド.md) — データアクセス制御の詳細
- [コスト・料金管理ガイド](10_コスト・料金管理ガイド.md) — 課金を抑えるためのベストプラクティス
