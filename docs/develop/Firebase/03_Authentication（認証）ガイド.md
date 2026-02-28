# Authentication（認証）ガイド

> **レベル**: ★★☆（初中級）  
> **前提知識**: [02_クイックスタート](02_クイックスタート.md) の完了  
> **所要時間**: 約 35 分  
> **目標**: Firebase Authentication を使ってログイン・ログアウト・ユーザー管理ができるようになる

---

## 📚 目次

1. [Firebase Authentication とは](#1-firebase-authenticationとは)
2. [対応している認証プロバイダ](#2-対応している認証プロバイダ)
3. [コンソールでの有効化](#3-コンソールでの有効化)
4. [メール・パスワード認証](#4-メールパスワード認証)
5. [Google ログイン（ソーシャル認証）](#5-google-ログインソーシャル認証)
6. [ログアウト・パスワードリセット](#6-ログアウトパスワードリセット)
7. [認証状態の監視](#7-認証状態の監視)
8. [Next.js での認証フロー](#8-nextjsでの認証フロー)
9. [ユーザー情報の取得・更新](#9-ユーザー情報の取得更新)
10. [エラーハンドリング](#10-エラーハンドリング)
11. [よくあるミスとベストプラクティス](#11-よくあるミスとベストプラクティス)

---

## 1. Firebase Authentication とは

**Firebase Authentication** は、ユーザーの **ログイン・ログアウト・アカウント管理** をほぼコードなしで実現できる認証サービスです。

```
【認証の流れ】

クライアント  →  Firebase Auth  →  JWT トークン発行
                                       ↓
クライアント  →  Firestore クエリ  →  JWT を検証してアクセス制御
```

> 💡 **JWT（JSON Web Token）とは**  
> ユーザーが「認証済みであること」を証明するデジタルチケットです。  
> Firebase が自動で生成・検証するため、開発者が意識する必要はほとんどありません。

---

## 2. 対応している認証プロバイダ

| プロバイダ | 説明 | 主なユースケース |
|----------|------|----------------|
| **メール / パスワード** | 基本的なメール認証。メール確認も設定可能 | 一般的な Web アプリ |
| **Google** | ソーシャルログインの中で最も利用率が高い | Web・モバイルアプリ全般 |
| **Apple** | Apple ID でログイン | iOS アプリ（App Store 審査で必須） |
| **GitHub** | GitHub アカウントでログイン | 開発者向けツール |
| **Twitter / X** | X アカウントでログイン | SNS 連携アプリ |
| **Facebook** | Facebook アカウントでログイン | SNS 連携アプリ |
| **電話番号（SMS）** | SMS 認証コードでログイン | セキュリティ重視のアプリ |
| **匿名認証** | ログインなしで仮ユーザー ID を発行 | お試し利用・ゲストユーザー |

---

## 3. コンソールでの有効化

1. [Firebase Console](https://console.firebase.google.com/) を開く
2. 左メニュー → 「**Authentication**」→「**始める**」
3. 「**ログイン方法**」タブで使いたいプロバイダを有効化

```
┌────────────────────────────────────┐
│ ログイン方法                        │
├────────────────────────────────────┤
│ メール / パスワード   [有効]  ✅   │
│ Google               [有効]  ✅   │
│ Apple                [無効]       │
│ GitHub               [無効]       │
└────────────────────────────────────┘
```

---

## 4. メール・パスワード認証

### ヘルパー関数 (`src/lib/firebase/auth.ts`)

```typescript
import {
  createUserWithEmailAndPassword,
  signInWithEmailAndPassword,
  signOut,
  sendPasswordResetEmail,
  sendEmailVerification,
  updateProfile,
  type User,
} from 'firebase/auth'
import { auth } from './config'

/** 新規ユーザー登録 */
export async function signUp(email: string, password: string, displayName?: string) {
  const credential = await createUserWithEmailAndPassword(auth, email, password)

  // 表示名を設定
  if (displayName) {
    await updateProfile(credential.user, { displayName })
  }

  // メール確認を送信
  await sendEmailVerification(credential.user)

  return credential.user
}

/** ログイン */
export async function signIn(email: string, password: string) {
  const credential = await signInWithEmailAndPassword(auth, email, password)
  return credential.user
}

/** ログアウト */
export async function logOut() {
  await signOut(auth)
}

/** パスワードリセットメールを送信 */
export async function resetPassword(email: string) {
  await sendPasswordResetEmail(auth, email)
}
```

### サインアップフォームの例

```typescript
// src/components/SignUpForm.tsx
'use client'

import { useState } from 'react'
import { signUp } from '@/lib/firebase/auth'
import { useRouter } from 'next/navigation'

export default function SignUpForm() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [name, setName] = useState('')
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)
  const router = useRouter()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError(null)

    try {
      await signUp(email, password, name)
      router.push('/dashboard')
    } catch (err: unknown) {
      setError(getFirebaseErrorMessage(err))
    } finally {
      setLoading(false)
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      <input value={name} onChange={(e) => setName(e.target.value)}
        placeholder="名前" />
      <input type="email" value={email} onChange={(e) => setEmail(e.target.value)}
        placeholder="メールアドレス" required />
      <input type="password" value={password} onChange={(e) => setPassword(e.target.value)}
        placeholder="パスワード（6文字以上）" required />
      {error && <p className="text-red-500">{error}</p>}
      <button type="submit" disabled={loading}>
        {loading ? '登録中...' : '新規登録'}
      </button>
    </form>
  )
}
```

---

## 5. Google ログイン（ソーシャル認証）

### ポップアップ方式（Web アプリ推奨）

```typescript
// src/lib/firebase/auth.ts に追加
import { GoogleAuthProvider, signInWithPopup, signInWithRedirect } from 'firebase/auth'

const googleProvider = new GoogleAuthProvider()

/** Google ログイン（ポップアップ方式） */
export async function signInWithGoogle() {
  const credential = await signInWithPopup(auth, googleProvider)
  return credential.user
}

/**
 * Google ログイン（リダイレクト方式）
 * モバイルブラウザではポップアップがブロックされる場合があるため
 * モバイル対応アプリではこちらを推奨
 */
export async function signInWithGoogleRedirect() {
  await signInWithRedirect(auth, googleProvider)
}
```

```typescript
// Google ログインボタンの例
'use client'

import { signInWithGoogle } from '@/lib/firebase/auth'
import { useRouter } from 'next/navigation'

export function GoogleLoginButton() {
  const router = useRouter()

  const handleGoogleLogin = async () => {
    try {
      await signInWithGoogle()
      router.push('/dashboard')
    } catch (error) {
      console.error('Google ログインエラー:', error)
    }
  }

  return (
    <button onClick={handleGoogleLogin} type="button">
      Google でログイン
    </button>
  )
}
```

---

## 6. ログアウト・パスワードリセット

```typescript
import { signOut, sendPasswordResetEmail } from 'firebase/auth'
import { auth } from '@/lib/firebase/config'

// ログアウト
async function logout() {
  await signOut(auth)
  console.log('✅ ログアウト成功')
}

// パスワードリセットメール送信
async function resetPassword(email: string) {
  await sendPasswordResetEmail(auth, email)
  console.log('✅ パスワードリセットメールを送信しました')
}
```

---

## 7. 認証状態の監視

Firebase Auth では `onAuthStateChanged` でログイン状態の変化をリアルタイムに監視できます。  
**ページ読み込み直後は `auth.currentUser` が `null` の場合があるため、必ずこの方法で状態を取得してください。**

```typescript
import { onAuthStateChanged, type User } from 'firebase/auth'
import { auth } from './config'

const unsubscribe = onAuthStateChanged(auth, (user: User | null) => {
  if (user) {
    console.log('ログイン中:', user.email)
    console.log('UID:', user.uid)
    console.log('メール確認済み:', user.emailVerified)
    console.log('表示名:', user.displayName)
    console.log('プロフィール写真:', user.photoURL)
  } else {
    console.log('未ログイン')
  }
})

// 監視を停止する場合（コンポーネントのアンマウント時など）
unsubscribe()
```

---

## 8. Next.js での認証フロー

### Context プロバイダー

```typescript
// src/contexts/AuthContext.tsx
'use client'

import { createContext, useContext, useEffect, useState, type ReactNode } from 'react'
import { onAuthStateChanged, type User } from 'firebase/auth'
import { auth } from '@/lib/firebase/config'

type AuthContextType = {
  user: User | null
  loading: boolean
}

const AuthContext = createContext<AuthContextType>({ user: null, loading: true })

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, (user) => {
      setUser(user)
      setLoading(false)
    })
    return () => unsubscribe() // ← クリーンアップ忘れずに
  }, [])

  return (
    <AuthContext.Provider value={{ user, loading }}>
      {children}
    </AuthContext.Provider>
  )
}

export const useAuth = () => useContext(AuthContext)
```

```typescript
// src/app/layout.tsx にプロバイダーを追加
import { AuthProvider } from '@/contexts/AuthContext'

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="ja">
      <body>
        <AuthProvider>{children}</AuthProvider>
      </body>
    </html>
  )
}
```

### 認証が必要なページの保護

```typescript
// src/components/ProtectedRoute.tsx
'use client'

import { useAuth } from '@/contexts/AuthContext'
import { useRouter } from 'next/navigation'
import { useEffect } from 'react'

export function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const { user, loading } = useAuth()
  const router = useRouter()

  useEffect(() => {
    if (!loading && !user) {
      router.push('/login') // 未ログインならログインページへ
    }
  }, [user, loading, router])

  if (loading) return <div>読み込み中...</div>
  if (!user) return null

  return <>{children}</>
}
```

### カスタムフック

```typescript
// src/hooks/useAuthActions.ts
'use client'

import { useAuth } from '@/contexts/AuthContext'
import { signIn, logOut, signUp, signInWithGoogle } from '@/lib/firebase/auth'
import { useState } from 'react'

export function useAuthActions() {
  const { user, loading } = useAuth()
  const [actionLoading, setActionLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleSignIn = async (email: string, password: string) => {
    setActionLoading(true)
    setError(null)
    try {
      await signIn(email, password)
    } catch (err) {
      setError(getFirebaseErrorMessage(err))
    } finally {
      setActionLoading(false)
    }
  }

  const handleSignOut = async () => {
    setActionLoading(true)
    try {
      await logOut()
    } finally {
      setActionLoading(false)
    }
  }

  return {
    user,
    loading: loading || actionLoading,
    error,
    signIn: handleSignIn,
    signOut: handleSignOut,
    signInWithGoogle,
  }
}
```

---

## 9. ユーザー情報の取得・更新

```typescript
import { updateProfile, updateEmail } from 'firebase/auth'
import { auth } from '@/lib/firebase/config'

// プロフィールの更新
async function updateUserProfile(displayName: string, photoURL?: string) {
  if (!auth.currentUser) return
  await updateProfile(auth.currentUser, {
    displayName,
    photoURL: photoURL ?? null,
  })
}

// メールアドレスの更新
async function changeEmail(newEmail: string) {
  if (!auth.currentUser) return
  await updateEmail(auth.currentUser, newEmail)
}
```

---

## 10. エラーハンドリング

Firebase のエラーコードを日本語メッセージに変換するユーティリティを用意しておくと便利です。

```typescript
/** Firebase のエラーコードを日本語メッセージに変換 */
export function getFirebaseErrorMessage(error: unknown): string {
  if (typeof error === 'object' && error !== null && 'code' in error) {
    const code = (error as { code: string }).code
    const messages: Record<string, string> = {
      'auth/email-already-in-use': 'このメールアドレスは既に使用されています',
      'auth/invalid-email': 'メールアドレスの形式が正しくありません',
      'auth/weak-password': 'パスワードは 6 文字以上で設定してください',
      'auth/user-not-found': 'メールアドレスまたはパスワードが間違っています',
      'auth/wrong-password': 'メールアドレスまたはパスワードが間違っています',
      'auth/too-many-requests': 'ログイン試行が多すぎます。しばらくしてから再試行してください',
      'auth/user-disabled': 'このアカウントは無効化されています',
      'auth/popup-closed-by-user': 'ログインがキャンセルされました',
    }
    return messages[code] ?? `エラーが発生しました（${code}）`
  }
  return '予期しないエラーが発生しました'
}
```

**主なエラーコード一覧：**

| エラーコード | 原因 |
|------------|------|
| `auth/email-already-in-use` | メールアドレスが既に使われている |
| `auth/invalid-email` | メールアドレスの形式が不正 |
| `auth/weak-password` | パスワードが 6 文字未満 |
| `auth/user-not-found` | ユーザーが存在しない |
| `auth/wrong-password` | パスワードが違う |
| `auth/too-many-requests` | ログイン試行回数が多すぎる |
| `auth/user-disabled` | アカウントが無効化されている |
| `auth/popup-closed-by-user` | ユーザーがポップアップを閉じた |

---

## 11. よくあるミスとベストプラクティス

### ❌ よくあるミス

```typescript
// ❌ NG: auth.currentUser をページ読み込み直後に使う
// 初期化前は null になりうる
const user = auth.currentUser // null になりうる！

// ❌ NG: onAuthStateChanged の unsubscribe を忘れる
useEffect(() => {
  onAuthStateChanged(auth, (user) => { ... }) // return しない NG！
}, [])
```

### ✅ ベストプラクティス

```typescript
// ✅ OK: onAuthStateChanged でユーザーを取得する
onAuthStateChanged(auth, (user) => {
  // ここでユーザー状態を確実に取得できる
})

// ✅ OK: unsubscribe を必ず return する
useEffect(() => {
  const unsubscribe = onAuthStateChanged(auth, (user) => { ... })
  return () => unsubscribe() // ← 必須
}, [])

// ✅ OK: エラーコードで丁寧にハンドリング
try {
  await signIn(email, password)
} catch (err) {
  setError(getFirebaseErrorMessage(err))
}
```

---

## 📌 まとめ

| 操作 | 関数 |
|------|------|
| 新規登録 | `createUserWithEmailAndPassword` |
| ログイン | `signInWithEmailAndPassword` |
| Google ログイン | `signInWithPopup(auth, googleProvider)` |
| ログアウト | `signOut` |
| パスワードリセット | `sendPasswordResetEmail` |
| メール確認送信 | `sendEmailVerification` |
| 認証状態の監視 | `onAuthStateChanged` |
| プロフィール更新 | `updateProfile` |

---

## 次のステップ

- [Firestore（データベース）ガイド](04_Firestore（データベース）ガイド.md) → データの読み書き・リアルタイム同期
