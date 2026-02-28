# 05. Next.js 統合ガイド

> **レベル**: ★★★☆☆（中級）  
> **前提知識**: [01_クイックスタート](01_クイックスタート.md)・[02_認証ガイド](02_認証ガイド.md)・[04_RLSガイド](04_RLSガイド.md) の完了  
> **所要時間**: 約 60 分

---

## 📚 目次

1. [セットアップ](#1-セットアップ)
2. [Supabase クライアントの設定](#2-supabase-クライアントの設定)
3. [Server Components での利用](#3-server-components-での利用)
4. [Client Components での利用](#4-client-components-での利用)
5. [認証フロー（App Router 対応）](#5-認証フローapp-router-対応)
6. [カスタムフックの作成](#6-カスタムフックの作成)
7. [Server Actions での利用](#7-server-actions-での利用)
8. [環境変数の管理](#8-環境変数の管理)

---

## 1. セットアップ

### パッケージのインストール

```bash
# Next.js プロジェクトに Supabase クライアントを追加
npm install @supabase/supabase-js @supabase/ssr
```

| パッケージ | 説明 |
|-----------|------|
| `@supabase/supabase-js` | Supabase の基本クライアント |
| `@supabase/ssr` | Next.js の SSR・App Router 向け最適化ライブラリ |

---

## 2. Supabase クライアントの設定

### ディレクトリ構成

```
src/
├── lib/
│   └── supabase/
│       ├── client.ts       ← ブラウザ用（Client Components）
│       ├── server.ts       ← サーバー用（Server Components / Server Actions）
│       └── middleware.ts   ← ミドルウェア用
├── middleware.ts            ← Next.js ミドルウェア
└── types/
    └── database.types.ts   ← DB 型定義（自動生成）
```

### ブラウザ用クライアント (`src/lib/supabase/client.ts`)

```typescript
import { createBrowserClient } from '@supabase/ssr'
import type { Database } from '@/types/database.types'

export function createClient() {
  return createBrowserClient<Database>(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
  )
}
```

### サーバー用クライアント (`src/lib/supabase/server.ts`)

```typescript
import { createServerClient } from '@supabase/ssr'
import { cookies } from 'next/headers'
import type { Database } from '@/types/database.types'

export async function createClient() {
  const cookieStore = await cookies()

  return createServerClient<Database>(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        getAll() {
          return cookieStore.getAll()
        },
        setAll(cookiesToSet) {
          try {
            cookiesToSet.forEach(({ name, value, options }) =>
              cookieStore.set(name, value, options)
            )
          } catch {
            // Server Component からの呼び出しでは set できないため無視
          }
        },
      },
    }
  )
}
```

### ミドルウェア用クライアント (`src/lib/supabase/middleware.ts`)

```typescript
import { createServerClient } from '@supabase/ssr'
import { NextResponse, type NextRequest } from 'next/server'
import type { Database } from '@/types/database.types'

export async function updateSession(request: NextRequest) {
  let supabaseResponse = NextResponse.next({ request })

  const supabase = createServerClient<Database>(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        getAll() {
          return request.cookies.getAll()
        },
        setAll(cookiesToSet) {
          cookiesToSet.forEach(({ name, value }) =>
            request.cookies.set(name, value)
          )
          supabaseResponse = NextResponse.next({ request })
          cookiesToSet.forEach(({ name, value, options }) =>
            supabaseResponse.cookies.set(name, value, options)
          )
        },
      },
    }
  )

  // セッションを更新（重要：この呼び出しを省略しないこと）
  const { data: { user } } = await supabase.auth.getUser()

  // 未認証ユーザーをログインページにリダイレクト
  if (!user && !request.nextUrl.pathname.startsWith('/auth')) {
    const url = request.nextUrl.clone()
    url.pathname = '/auth/login'
    return NextResponse.redirect(url)
  }

  return supabaseResponse
}
```

### Next.js ミドルウェア (`src/middleware.ts`)

```typescript
import { type NextRequest } from 'next/server'
import { updateSession } from '@/lib/supabase/middleware'

export async function middleware(request: NextRequest) {
  return await updateSession(request)
}

export const config = {
  matcher: [
    /*
     * 以下を除くすべてのパスにマッチ:
     * - _next/static（静的ファイル）
     * - _next/image（画像最適化）
     * - favicon.ico
     */
    '/((?!_next/static|_next/image|favicon.ico|.*\\.(?:svg|png|jpg|jpeg|gif|webp)$).*)',
  ],
}
```

---

## 3. Server Components での利用

Server Components では、サーバー側でデータを取得できます。クライアントに JS を送らず、SEO にも有利です。

### データ取得の例

```typescript
// src/app/posts/page.tsx
import { createClient } from '@/lib/supabase/server'

export default async function PostsPage() {
  const supabase = await createClient()

  const { data: posts, error } = await supabase
    .from('posts')
    .select(`
      id,
      title,
      content,
      created_at,
      author:users(id, name, avatar_url)
    `)
    .order('created_at', { ascending: false })
    .limit(10)

  if (error) {
    console.error('投稿取得エラー:', error.message)
    return <div>データの取得に失敗しました</div>
  }

  return (
    <main>
      <h1>投稿一覧</h1>
      <ul>
        {posts.map((post) => (
          <li key={post.id}>
            <h2>{post.title}</h2>
            <p>{post.author?.name}</p>
          </li>
        ))}
      </ul>
    </main>
  )
}
```

### 認証ユーザーの取得

```typescript
// src/app/dashboard/page.tsx
import { createClient } from '@/lib/supabase/server'
import { redirect } from 'next/navigation'

export default async function DashboardPage() {
  const supabase = await createClient()

  // サーバー側でユーザーを取得（getSession より getUser が安全）
  const { data: { user } } = await supabase.auth.getUser()

  if (!user) {
    redirect('/auth/login')
  }

  return (
    <div>
      <h1>ダッシュボード</h1>
      <p>ようこそ、{user.email} さん</p>
    </div>
  )
}
```

> ⚠️ **注意**: `getSession()` ではなく `getUser()` を使うこと。`getSession()` はトークンをサーバー側で検証しないため、セキュリティリスクがある。

---

## 4. Client Components での利用

Client Components は、インタラクティブな UI（リアルタイム更新・フォーム等）に使います。

### リアルタイムデータの表示

```typescript
'use client'

import { useEffect, useState } from 'react'
import { createClient } from '@/lib/supabase/client'

type Message = {
  id: number
  content: string
  user_id: string
  created_at: string
}

export default function RealtimeMessages({ roomId }: { roomId: string }) {
  const [messages, setMessages] = useState<Message[]>([])
  const supabase = createClient()

  useEffect(() => {
    // 初回データ取得
    const fetchMessages = async () => {
      const { data } = await supabase
        .from('messages')
        .select('*')
        .eq('room_id', roomId)
        .order('created_at', { ascending: true })

      if (data) setMessages(data)
    }

    fetchMessages()

    // リアルタイム購読
    const channel = supabase
      .channel(`room-${roomId}`)
      .on(
        'postgres_changes',
        {
          event: 'INSERT',
          schema: 'public',
          table: 'messages',
          filter: `room_id=eq.${roomId}`,
        },
        (payload) => {
          setMessages((prev) => [...prev, payload.new as Message])
        }
      )
      .subscribe()

    // クリーンアップ
    return () => {
      supabase.removeChannel(channel)
    }
  }, [roomId])

  return (
    <ul>
      {messages.map((msg) => (
        <li key={msg.id}>{msg.content}</li>
      ))}
    </ul>
  )
}
```

---

## 5. 認証フロー（App Router 対応）

### ログインフォーム

```typescript
// src/app/auth/login/page.tsx
'use client'

import { useState } from 'react'
import { createClient } from '@/lib/supabase/client'
import { useRouter } from 'next/navigation'

export default function LoginPage() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)
  const router = useRouter()
  const supabase = createClient()

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError(null)

    const { error } = await supabase.auth.signInWithPassword({
      email,
      password,
    })

    if (error) {
      setError(error.message)
      setLoading(false)
      return
    }

    router.push('/dashboard')
    router.refresh() // Server Components のキャッシュを更新
  }

  return (
    <form onSubmit={handleLogin}>
      <input
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        placeholder="メールアドレス"
        required
      />
      <input
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        placeholder="パスワード"
        required
      />
      {error && <p className="text-red-500">{error}</p>}
      <button type="submit" disabled={loading}>
        {loading ? 'ログイン中...' : 'ログイン'}
      </button>
    </form>
  )
}
```

### ログアウト（Server Action）

```typescript
// src/app/auth/actions.ts
'use server'

import { createClient } from '@/lib/supabase/server'
import { redirect } from 'next/navigation'

export async function logout() {
  const supabase = await createClient()
  await supabase.auth.signOut()
  redirect('/auth/login')
}
```

```typescript
// ログアウトボタン（使用例）
import { logout } from '@/app/auth/actions'

export function LogoutButton() {
  return (
    <form action={logout}>
      <button type="submit">ログアウト</button>
    </form>
  )
}
```

---

## 6. カスタムフックの作成

再利用可能なフックでデータ取得ロジックを共通化します。

### useUser フック

```typescript
// src/hooks/useUser.ts
'use client'

import { useEffect, useState } from 'react'
import { createClient } from '@/lib/supabase/client'
import type { User } from '@supabase/supabase-js'

export function useUser() {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)
  const supabase = createClient()

  useEffect(() => {
    // 現在のセッションを取得
    const getUser = async () => {
      const { data: { user } } = await supabase.auth.getUser()
      setUser(user)
      setLoading(false)
    }

    getUser()

    // 認証状態の変更を監視
    const { data: { subscription } } = supabase.auth.onAuthStateChange(
      (_event, session) => {
        setUser(session?.user ?? null)
        setLoading(false)
      }
    )

    return () => subscription.unsubscribe()
  }, [])

  return { user, loading }
}
```

### useSupabaseQuery フック（汎用データ取得）

```typescript
// src/hooks/useSupabaseQuery.ts
'use client'

import { useEffect, useState } from 'react'

type QueryResult<T> = {
  data: T | null
  error: string | null
  loading: boolean
  refetch: () => void
}

export function useSupabaseQuery<T>(
  queryFn: () => Promise<{ data: T | null; error: { message: string } | null }>
): QueryResult<T> {
  const [data, setData] = useState<T | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(true)
  const [trigger, setTrigger] = useState(0)

  useEffect(() => {
    let isMounted = true

    const execute = async () => {
      setLoading(true)
      const result = await queryFn()

      if (!isMounted) return

      if (result.error) {
        setError(result.error.message)
        setData(null)
      } else {
        setData(result.data)
        setError(null)
      }
      setLoading(false)
    }

    execute()
    return () => { isMounted = false }
  }, [trigger])

  return {
    data,
    error,
    loading,
    refetch: () => setTrigger((n) => n + 1),
  }
}
```

---

## 7. Server Actions での利用

フォーム送信やデータ変更には Server Actions を使うと型安全で簡潔に書けます。

```typescript
// src/app/posts/actions.ts
'use server'

import { createClient } from '@/lib/supabase/server'
import { revalidatePath } from 'next/cache'

export async function createPost(formData: FormData) {
  const supabase = await createClient()

  const { data: { user } } = await supabase.auth.getUser()
  if (!user) throw new Error('認証が必要です')

  const title = formData.get('title') as string
  const content = formData.get('content') as string

  const { error } = await supabase.from('posts').insert({
    title,
    content,
    user_id: user.id,
  })

  if (error) throw new Error(error.message)

  // キャッシュを再検証して最新データを表示
  revalidatePath('/posts')
}

export async function deletePost(postId: string) {
  const supabase = await createClient()

  const { data: { user } } = await supabase.auth.getUser()
  if (!user) throw new Error('認証が必要です')

  const { error } = await supabase
    .from('posts')
    .delete()
    .eq('id', postId)
    .eq('user_id', user.id) // 自分の投稿のみ削除可能

  if (error) throw new Error(error.message)

  revalidatePath('/posts')
}
```

---

## 8. 環境変数の管理

### `.env.local`（開発環境）

```bash
# Supabase 接続情報（ダッシュボード > Settings > API から取得）
NEXT_PUBLIC_SUPABASE_URL=https://xxxxxxxxxxxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# ⚠️ SERVICE_ROLE_KEY はクライアントに公開しないこと
SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

> ⚠️ `NEXT_PUBLIC_` プレフィックスが付いた変数はブラウザから見えます。**ANON_KEY はブラウザに公開されますが、これは意図的な設計**です。RLS でセキュリティを確保します。  
> **SERVICE_ROLE_KEY は絶対にブラウザに公開しないこと**（RLS をバイパスする管理者権限）。

### 型定義の自動生成

Supabase CLI で型定義ファイルを自動生成できます。

```bash
# Supabase CLI のインストール
npm install supabase --save-dev

# ログイン
npx supabase login

# 型定義を生成
npx supabase gen types typescript --project-id <YOUR_PROJECT_ID> \
  > src/types/database.types.ts
```

生成される型定義を使うことで、クエリに型安全性が生まれます：

```typescript
import type { Database } from '@/types/database.types'

// テーブルの型を取得
type Post = Database['public']['Tables']['posts']['Row']
type PostInsert = Database['public']['Tables']['posts']['Insert']
```

---

## 📌 まとめ

| 用途 | 使うクライアント | 理由 |
|------|----------------|------|
| Server Component でのデータ取得 | `server.ts` | サーバーサイドで Cookie を直接操作できる |
| Client Component でのインタラクション | `client.ts` | ブラウザの Cookie と Session を自動管理 |
| Middleware での認証チェック | `middleware.ts` | リクエスト/レスポンスの Cookie を操作できる |
| Server Action でのデータ変更 | `server.ts` | サーバーサイドで安全に実行できる |

---

## 次のステップ

- [Edge Functions ガイド](06_EdgeFunctionsガイド.md) → サーバーレス関数によるカスタムロジックの実装
