# Firestore（データベース）ガイド

> **レベル**: ★★☆（初中級）  
> **前提知識**: [02_クイックスタート](02_クイックスタート.md) の完了  
> **所要時間**: 約 45 分  
> **目標**: Firestore の基本概念を理解し、データの読み書き・リアルタイム同期・セキュリティルールを実装できるようになる

---

## 📚 目次

1. [Firestore とは](#1-firestoreとは)
2. [データモデルの理解](#2-データモデルの理解)
3. [データの読み取り（Read）](#3-データの読み取りread)
4. [データの書き込み（Create）](#4-データの書き込みcreate)
5. [データの更新（Update）](#5-データの更新update)
6. [データの削除（Delete）](#6-データの削除delete)
7. [クエリ（絞り込み・並び替え）](#7-クエリ絞り込み並び替え)
8. [リアルタイム同期](#8-リアルタイム同期)
9. [セキュリティルール](#9-セキュリティルール)
10. [Realtime Database との比較](#10-realtime-databaseとの比較)
11. [よくあるミスとベストプラクティス](#11-よくあるミスとベストプラクティス)

---

## 1. Firestore とは

**Cloud Firestore** は、Firebase が提供する **NoSQL ドキュメント型データベース** です。

```
【Firestore の特徴】

✅ NoSQL（テーブルではなくドキュメントでデータを管理）
✅ リアルタイム同期（データ変更が即座に全クライアントへ反映）
✅ オフライン対応（ネット接続なしでも動作 → 復帰時に自動同期）
✅ スケーラブル（Google のインフラで自動スケール）
✅ マルチプラットフォーム（Web / iOS / Android / Flutter すべて対応）
```

### SQL との対応

| SQL | Firestore |
|-----|-----------|
| テーブル | コレクション |
| 行（Row） | ドキュメント |
| 列（Column） | フィールド |
| JOIN | サブコレクション or 参照 |
| WHERE | `where()` |
| ORDER BY | `orderBy()` |
| LIMIT | `limit()` |

> ⚠️ **重要**: Firestore は **JOIN ができません**。関連データを取得するには複数回クエリするか、データを非正規化（重複して保存）します。

---

## 2. データモデルの理解

Firestore のデータ構造は **コレクション → ドキュメント → サブコレクション** の階層になっています。

```
Firestore
├── users（コレクション）
│   ├── uid_001（ドキュメント）
│   │   ├── name: "山田 太郎"
│   │   ├── email: "yamada@example.com"
│   │   └── createdAt: Timestamp
│   └── uid_002（ドキュメント）
│       └── ...
└── posts（コレクション）
    ├── post_001（ドキュメント）
    │   ├── title: "初めての投稿"
    │   ├── content: "本文..."
    │   ├── authorId: "uid_001"   ← 参照（JOIN の代わり）
    │   ├── published: false
    │   ├── tags: ["react", "firebase"]
    │   ├── likeCount: 0
    │   └── comments（サブコレクション）
    │       └── comment_001
    │           └── body: "素晴らしい！"
    └── post_002（ドキュメント）
        └── ...
```

### ドキュメントのデータ型

| データ型 | 例 |
|---------|-----|
| `string` | `"山田太郎"` |
| `number` | `28`, `1500.5` |
| `boolean` | `true`, `false` |
| `timestamp` | `serverTimestamp()` |
| `array` | `["tag1", "tag2"]` |
| `map`（オブジェクト） | `{ prefecture: "東京", city: "渋谷" }` |
| `null` | `null` |
| `reference` | 他ドキュメントへの参照 |

> 💡 **初心者向けポイント**  
> ドキュメントは「JSON ファイル 1 枚」のイメージ。各ドキュメントは **最大 1MB** まで保存できます。

---

## 3. データの読み取り（Read）

```typescript
import {
  collection,
  doc,
  getDoc,
  getDocs,
  query,
  where,
  orderBy,
  limit,
} from 'firebase/firestore'
import { db } from '@/lib/firebase/config'

// --- 1 件取得（ドキュメント ID で指定） ---
async function getUser(userId: string) {
  const docRef = doc(db, 'users', userId)
  const docSnap = await getDoc(docRef)

  if (docSnap.exists()) {
    return { id: docSnap.id, ...docSnap.data() }
  } else {
    return null // ドキュメントが存在しない
  }
}

// --- コレクション全件取得 ---
async function getAllPosts() {
  const querySnapshot = await getDocs(collection(db, 'posts'))
  return querySnapshot.docs.map((doc) => ({
    id: doc.id,
    ...doc.data(),
  }))
}

// --- 条件付きで取得 ---
async function getPublishedPosts() {
  const q = query(
    collection(db, 'posts'),
    where('published', '==', true),
    orderBy('createdAt', 'desc'),
    limit(10)
  )
  const querySnapshot = await getDocs(q)
  return querySnapshot.docs.map((doc) => ({ id: doc.id, ...doc.data() }))
}
```

### React での使用例（useEffect + useState）

```typescript
'use client'

import { useEffect, useState } from 'react'
import { collection, getDocs } from 'firebase/firestore'
import { db } from '@/lib/firebase/config'

type Post = { id: string; title: string; content: string }

export function PostList() {
  const [posts, setPosts] = useState<Post[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchPosts = async () => {
      const snapshot = await getDocs(collection(db, 'posts'))
      const data = snapshot.docs.map((doc) => ({
        id: doc.id,
        ...(doc.data() as Omit<Post, 'id'>),
      }))
      setPosts(data)
      setLoading(false)
    }
    fetchPosts()
  }, [])

  if (loading) return <p>読み込み中...</p>
  return (
    <ul>
      {posts.map((post) => (
        <li key={post.id}>{post.title}</li>
      ))}
    </ul>
  )
}
```

---

## 4. データの書き込み（Create）

```typescript
import {
  addDoc,
  setDoc,
  doc,
  collection,
  serverTimestamp,
} from 'firebase/firestore'
import { db } from '@/lib/firebase/config'

// --- ID を自動生成して追加（addDoc） ---
async function createPost(title: string, content: string, authorId: string) {
  const docRef = await addDoc(collection(db, 'posts'), {
    title,
    content,
    authorId,
    published: false,
    createdAt: serverTimestamp(), // サーバー側のタイムスタンプを使用（推奨）
    updatedAt: serverTimestamp(),
  })
  console.log('✅ 作成された ID:', docRef.id)
  return docRef.id
}

// --- ID を指定して作成・上書き（setDoc） ---
// ユーザープロフィールのような「UID = ドキュメント ID」のケースに使う
async function setUserProfile(userId: string, name: string, avatarUrl?: string) {
  await setDoc(
    doc(db, 'users', userId),
    {
      name,
      avatarUrl: avatarUrl ?? null,
      createdAt: serverTimestamp(),
    },
    { merge: true } // merge: true にすると既存フィールドを保持する（部分更新）
  )
}
```

> 💡 **`setDoc` vs `addDoc` の違い**  
> - `addDoc`：ID を Firebase が自動生成（`posts` コレクション等）  
> - `setDoc`：ID を自分で指定（`users/{uid}` のようにユーザー情報を UID で管理する場合）

---

## 5. データの更新（Update）

```typescript
import {
  updateDoc,
  doc,
  arrayUnion,
  arrayRemove,
  increment,
  serverTimestamp,
  deleteField,
} from 'firebase/firestore'
import { db } from '@/lib/firebase/config'

// --- フィールドの部分更新（updateDoc） ---
async function publishPost(postId: string) {
  await updateDoc(doc(db, 'posts', postId), {
    published: true,
    updatedAt: serverTimestamp(),
  })
}

// --- 配列フィールドへの追加・削除（アトミック操作） ---
async function addTag(postId: string, tag: string) {
  await updateDoc(doc(db, 'posts', postId), {
    tags: arrayUnion(tag),  // 重複なしで追加
  })
}

async function removeTag(postId: string, tag: string) {
  await updateDoc(doc(db, 'posts', postId), {
    tags: arrayRemove(tag), // 配列から削除
  })
}

// --- 数値のインクリメント（いいね数など）---
// increment を使うことで、複数クライアントが同時に更新しても競合しない
async function likePost(postId: string) {
  await updateDoc(doc(db, 'posts', postId), {
    likeCount: increment(1),
  })
}

// --- 特定フィールドのみ削除 ---
async function removeField(userId: string) {
  await updateDoc(doc(db, 'users', userId), {
    age: deleteField(), // age フィールドのみ削除
  })
}
```

---

## 6. データの削除（Delete）

```typescript
import { deleteDoc, doc } from 'firebase/firestore'
import { db } from '@/lib/firebase/config'

async function deletePost(postId: string) {
  await deleteDoc(doc(db, 'posts', postId))
  console.log('✅ 削除完了')
}
```

---

## 7. クエリ（絞り込み・並び替え）

### 使えるフィルタ演算子

```typescript
import { query, collection, where } from 'firebase/firestore'

where('status', '==', 'active')           // 等値
where('status', '!=', 'deleted')          // 不等値
where('price', '<', 1000)                 // 比較（<, <=, >, >= も同様）
where('tags', 'array-contains', 'react')  // 配列に値が含まれる
where('tags', 'array-contains-any', ['react', 'vue']) // いずれかを含む
where('category', 'in', ['tech', 'design'])           // IN
where('category', 'not-in', ['spam', 'deleted'])      // NOT IN
```

### ページネーション

```typescript
import {
  query, collection, where, orderBy, limit,
  startAfter, getDocs, type QueryDocumentSnapshot,
} from 'firebase/firestore'

async function getPostsPage(lastDoc?: QueryDocumentSnapshot, pageSize = 10) {
  let q = query(
    collection(db, 'posts'),
    where('published', '==', true),
    orderBy('createdAt', 'desc'),
    limit(pageSize)
  )

  // 前ページの最後のドキュメントを起点にする
  if (lastDoc) {
    q = query(q, startAfter(lastDoc))
  }

  const snapshot = await getDocs(q)
  const posts = snapshot.docs.map((doc) => ({ id: doc.id, ...doc.data() }))
  const lastVisible = snapshot.docs[snapshot.docs.length - 1]

  return { posts, lastVisible, hasMore: snapshot.docs.length === pageSize }
}
```

> ⚠️ **複合クエリのインデックス**  
> `where` と `orderBy` を組み合わせると **複合インデックスの作成** が必要です。  
> エラーメッセージに表示される URL をクリックすると Firebase Console で自動作成できます。

---

## 8. リアルタイム同期

`onSnapshot` を使うと、データの変更をリアルタイムで受け取れます。

```typescript
'use client'

import { useEffect, useState } from 'react'
import { onSnapshot, collection, query, where, orderBy, limit } from 'firebase/firestore'
import { db } from '@/lib/firebase/config'

type Post = { id: string; title: string; content: string; createdAt: unknown }

export function RealtimePosts() {
  const [posts, setPosts] = useState<Post[]>([])

  useEffect(() => {
    const q = query(
      collection(db, 'posts'),
      where('published', '==', true),
      orderBy('createdAt', 'desc'),
      limit(20)
    )

    // 変更を監視（戻り値は監視を停止する関数）
    const unsubscribe = onSnapshot(q, (snapshot) => {
      const updatedPosts = snapshot.docs.map((doc) => ({
        id: doc.id,
        ...doc.data(),
      })) as Post[]

      setPosts(updatedPosts)
    })

    // クリーンアップ（コンポーネントのアンマウント時に監視を停止）
    return () => unsubscribe()
  }, [])

  return (
    <ul>
      {posts.map((post) => (
        <li key={post.id}>{post.title}</li>
      ))}
    </ul>
  )
}
```

---

## 9. セキュリティルール

Firebase Console → Firestore Database → **「ルール」** タブで設定します。

### 基本構文

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {

    // すべてのドキュメントをデフォルトで拒否
    match /{document=**} {
      allow read, write: if false;
    }

    // users コレクション: 本人のみ読み書き可能
    match /users/{userId} {
      allow read, write: if request.auth != null
                         && request.auth.uid == userId;
    }

    // posts コレクション
    match /posts/{postId} {
      // 公開投稿は誰でも読める。自分の未公開投稿も読める
      allow read: if resource.data.published == true
                  || (request.auth != null && request.auth.uid == resource.data.authorId);

      // 認証済みユーザーが自分の投稿を作成できる
      allow create: if request.auth != null
                    && request.resource.data.authorId == request.auth.uid;

      // 自分の投稿のみ更新・削除できる
      allow update, delete: if request.auth != null
                             && resource.data.authorId == request.auth.uid;
    }

  }
}
```

> 💡 **主なルール変数**  
> - `request.auth`：現在のユーザー情報（未ログインなら `null`）  
> - `request.auth.uid`：現在のユーザーの ID  
> - `resource.data`：既存のドキュメントのデータ（読み取り・更新前）  
> - `request.resource.data`：書き込もうとしているデータ

> ⚠️ **開発中によくあるミス**:  
> `allow read, write: if true;` は全データを公開してしまいます。  
> 本番デプロイ前に必ずルールをレビューしてください。

---

## 10. Realtime Database との比較

Firebase には **Firestore** と **Realtime Database** の 2 種類の DB があります。

| 項目 | Firestore | Realtime Database |
|------|-----------|-------------------|
| **データ構造** | コレクション / ドキュメント | JSON ツリー |
| **クエリ** | 豊富（複合クエリ・並び替えなど） | 限定的 |
| **スケーラビリティ** | 非常に高い | 中程度 |
| **レイテンシ** | 低い | 超低い（超高頻度更新向け） |
| **料金体系** | 読み取り・書き込み回数 | データ転送量 |
| **推奨度** | ✅ **新規開発はこちら** | 超低レイテンシが必要な場合のみ |

---

## 11. よくあるミスとベストプラクティス

### ❌ よくあるミス

```typescript
// ❌ NG: onSnapshot の unsubscribe を忘れる（メモリリーク・余計な課金の原因）
useEffect(() => {
  onSnapshot(...) // return しない NG！
}, [])

// ❌ NG: 1 ドキュメントに大量データを詰め込む（最大 1MB 制限）
await setDoc(doc(db, 'users', userId), {
  messages: [...メッセージを追加し続ける], // NG！サブコレクションに分割する
})

// ❌ NG: 数値のカウントアップに通常の updateDoc を使う（同時更新で競合する）
const current = (await getDoc(...)).data()?.likeCount ?? 0
await updateDoc(..., { likeCount: current + 1 }) // NG！
```

### ✅ ベストプラクティス

```typescript
// ✅ OK: onSnapshot は必ず unsubscribe を return する
useEffect(() => {
  const unsubscribe = onSnapshot(...)
  return () => unsubscribe() // ← 必須
}, [])

// ✅ OK: 大量データはサブコレクションに分割する
await addDoc(collection(db, 'users', userId, 'messages'), {
  text: 'こんにちは',
  createdAt: serverTimestamp(),
})

// ✅ OK: 数値のカウントアップは increment を使う（競合なし）
await updateDoc(doc(db, 'posts', postId), {
  likeCount: increment(1),
})

// ✅ OK: タイムスタンプはサーバー側を使う（クライアント時計のズレを防ぐ）
await addDoc(collection(db, 'posts'), {
  text: '投稿',
  createdAt: serverTimestamp(), // ← Timestamp.now() より推奨
})
```

---

## 📌 まとめ

| 操作 | 関数 |
|------|------|
| 1 件取得 | `getDoc(doc(db, 'col', 'id'))` |
| 全件取得 | `getDocs(collection(db, 'col'))` |
| 条件取得 | `getDocs(query(collection, where(...)))` |
| ID 自動で追加 | `addDoc(collection(db, 'col'), data)` |
| ID 指定で作成 | `setDoc(doc(db, 'col', 'id'), data)` |
| 部分更新 | `updateDoc(doc(db, 'col', 'id'), data)` |
| 配列操作 | `arrayUnion(value)` / `arrayRemove(value)` |
| カウンター操作 | `increment(n)` |
| 削除 | `deleteDoc(doc(db, 'col', 'id'))` |
| リアルタイム監視 | `onSnapshot(query, callback)` |

---

## 次のステップ

- [Cloud Storage（ストレージ）ガイド](05_Cloud_Storage（ストレージ）ガイド.md) → ファイルのアップロード・管理
