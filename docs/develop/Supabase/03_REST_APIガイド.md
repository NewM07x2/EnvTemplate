# REST API ガイド：フロントエンドからのデータ取得

> **所要時間**: 約 40 分  
> **対象レベル**: 初心者～中級者（レベル 2）  
> **前提**: [クイックスタート](01_クイックスタート.md) と [認証ガイド](02_認証ガイド.md) を完了していること

---

## 📋 このガイドでやること

1. REST API の基礎理解
2. SELECT（データ取得）
3. INSERT（データ作成）
4. UPDATE（データ更新）
5. DELETE（データ削除）
6. フィルタリング・ソート・ページネーション
7. リアルタイム同期（Subscriptions）

---

## REST API とは

Supabase は DB テーブルから **自動的に REST API を生成** します。

```
テーブル: users

REST API が自動生成:
GET    /rest/v1/users           → 全ユーザー取得
GET    /rest/v1/users?id=eq.1   → 特定ユーザー取得
POST   /rest/v1/users           → ユーザー作成
PATCH  /rest/v1/users?id=eq.1   → ユーザー更新
DELETE /rest/v1/users?id=eq.1   → ユーザー削除
```

JavaScript SDK（`@supabase/supabase-js`）を使うことで、HTTP リクエストを直接書く必要はありません。

---

## ステップ 1: SELECT（データ取得）

### 1-1. すべてのデータを取得

```typescript
import { supabase } from '@/lib/supabase'

async function getAllUsers() {
  const { data, error } = await supabase
    .from('users')
    .select('*')

  if (error) {
    console.error('エラー:', error)
    return null
  }

  console.log('ユーザー:', data)
  return data
}
```

**期待される出力:**
```json
[
  {
    "id": "uuid-1",
    "email": "user1@example.com",
    "name": "山田太郎",
    "created_at": "2026-02-28T10:00:00Z"
  },
  {
    "id": "uuid-2",
    "email": "user2@example.com",
    "name": "佐藤花子",
    "created_at": "2026-02-28T11:00:00Z"
  }
]
```

### 1-2. 特定のカラムのみ取得

```typescript
// email と name だけ取得
const { data, error } = await supabase
  .from('users')
  .select('email, name')

// 結果: [{ email: "...", name: "..." }, ...]
```

### 1-3. 特定の行を取得

```typescript
// ID が uuid-1 のユーザーを取得
const { data, error } = await supabase
  .from('users')
  .select('*')
  .eq('id', 'uuid-1')

// 結果: [{ id: "uuid-1", ... }]
```

### 1-4. 1 件だけ取得

```typescript
// 1 件だけ取得したい場合（期待される結果が 1 件の場合）
const { data, error } = await supabase
  .from('users')
  .select('*')
  .eq('id', 'uuid-1')
  .single()  // 1 件だけを返す

// 結果: { id: "uuid-1", ... } (配列ではなくオブジェクト)
```

### React Hook 例

```typescript
import { useEffect, useState } from 'react'
import { supabase } from '@/lib/supabase'

export function useUsers() {
  const [users, setUsers] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    const fetchUsers = async () => {
      const { data, error } = await supabase
        .from('users')
        .select('*')

      if (error) {
        setError(error.message)
      } else {
        setUsers(data || [])
      }

      setLoading(false)
    }

    fetchUsers()
  }, [])

  return { users, loading, error }
}

// 使用例
export function UsersList() {
  const { users, loading, error } = useUsers()

  if (loading) return <div>読み込み中...</div>
  if (error) return <div>エラー: {error}</div>

  return (
    <ul>
      {users.map((user) => (
        <li key={user.id}>
          {user.name} ({user.email})
        </li>
      ))}
    </ul>
  )
}
```

---

## ステップ 2: INSERT（データ作成）

### 2-1. 1 件のデータを挿入

```typescript
async function createUser(email: string, name: string) {
  const { data, error } = await supabase
    .from('users')
    .insert([
      {
        email,
        name
      }
    ])
    .select()  // 挿入後、新規データを返す

  if (error) {
    console.error('挿入エラー:', error)
    return null
  }

  console.log('✅ ユーザー作成:', data)
  return data
}
```

### 2-2. 複数のデータを一度に挿入

```typescript
async function createMultipleUsers() {
  const { data, error } = await supabase
    .from('users')
    .insert([
      { email: 'user1@example.com', name: '太郎' },
      { email: 'user2@example.com', name: '花子' },
      { email: 'user3@example.com', name: '次郎' }
    ])
    .select()

  return data
}
```

### 2-3. リレーション先のデータも一緒に作成

posts テーブルにデータを作成するときに、関連するユーザーも指定：

```typescript
async function createPost(userId: string, title: string, content: string) {
  const { data, error } = await supabase
    .from('posts')
    .insert([
      {
        user_id: userId,
        title,
        content
      }
    ])
    .select()

  return data
}
```

---

## ステップ 3: UPDATE（データ更新）

### 3-1. 特定の行を更新

```typescript
async function updateUser(userId: string, name: string) {
  const { data, error } = await supabase
    .from('users')
    .update({ name })
    .eq('id', userId)
    .select()

  if (error) {
    console.error('更新エラー:', error)
    return null
  }

  console.log('✅ ユーザー更新:', data)
  return data
}
```

### 3-2. 複数の行を一度に更新

```typescript
// すべてのユーザーの name を更新
const { data, error } = await supabase
  .from('users')
  .update({ updated_at: new Date() })
  .gt('id', 'uuid')  // id が "uuid" より大きい行
  .select()
```

---

## ステップ 4: DELETE（データ削除）

### 4-1. 特定の行を削除

```typescript
async function deleteUser(userId: string) {
  const { error } = await supabase
    .from('users')
    .delete()
    .eq('id', userId)

  if (error) {
    console.error('削除エラー:', error)
    return false
  }

  console.log('✅ ユーザー削除完了')
  return true
}
```

### 4-2. 複数の行を削除

```typescript
// 作成日が 2025 年の行を削除
const { error } = await supabase
  .from('posts')
  .delete()
  .lt('created_at', '2026-01-01')
```

---

## ステップ 5: フィルタリング・ソート・ページネーション

### 5-1. フィルタリング（条件検索）

```typescript
// メールアドレスが "example.com" を含むユーザーを検索
const { data } = await supabase
  .from('users')
  .select('*')
  .ilike('email', '%example.com%')

// 複数の条件
const { data } = await supabase
  .from('users')
  .select('*')
  .eq('name', '山田太郎')
  .gte('created_at', '2026-01-01')  // 2026-01-01 以降
```

### 比較演算子の一覧

| 演算子 | 説明 | 例 |
|--------|------|-----|
| `eq` | 等しい | `.eq('status', 'active')` |
| `neq` | 等しくない | `.neq('status', 'inactive')` |
| `gt` | より大きい | `.gt('age', 18)` |
| `gte` | 以上 | `.gte('created_at', '2026-01-01')` |
| `lt` | より小さい | `.lt('age', 65)` |
| `lte` | 以下 | `.lte('price', 1000)` |
| `like` | 部分一致（大文字小文字区別） | `.like('email', '%example.com')` |
| `ilike` | 部分一致（大文字小文字区別なし） | `.ilike('email', '%example.com')` |
| `in` | リストに含まれる | `.in('status', ['active', 'pending'])` |
| `contains` | 配列に含まれる | `.contains('tags', ['javascript'])` |

### 5-2. ソート（並び替え）

```typescript
// 作成日が新しい順にソート
const { data } = await supabase
  .from('posts')
  .select('*')
  .order('created_at', { ascending: false })

// 複数のカラムでソート
const { data } = await supabase
  .from('posts')
  .select('*')
  .order('user_id', { ascending: true })
  .order('created_at', { ascending: false })
```

### 5-3. ページネーション（ページ分割）

```typescript
// 1 ページあたり 10 件、ページ 1（0～9 番目）
const { data, count } = await supabase
  .from('users')
  .select('*', { count: 'exact' })
  .range(0, 9)  // 0 から 9 番目（0 ベース）

// ページ 2（10～19 番目）
const { data } = await supabase
  .from('users')
  .select('*')
  .range(10, 19)
```

### React での実装例

```typescript
export function UsersPagination() {
  const [page, setPage] = useState(1)
  const [users, setUsers] = useState([])
  const pageSize = 10

  useEffect(() => {
    const fetchUsers = async () => {
      const from = (page - 1) * pageSize
      const to = from + pageSize - 1

      const { data } = await supabase
        .from('users')
        .select('*')
        .range(from, to)
        .order('created_at', { ascending: false })

      setUsers(data || [])
    }

    fetchUsers()
  }, [page])

  return (
    <div>
      <ul>
        {users.map((user) => (
          <li key={user.id}>{user.name}</li>
        ))}
      </ul>
      <button onClick={() => setPage(page - 1)} disabled={page === 1}>
        ← 前へ
      </button>
      <span>ページ {page}</span>
      <button onClick={() => setPage(page + 1)}>
        次へ →
      </button>
    </div>
  )
}
```

---

## ステップ 6: リレーション・JOIN

posts テーブルでユーザー情報も一緒に取得：

```typescript
// 投稿とユーザー情報を一緒に取得
const { data } = await supabase
  .from('posts')
  .select(`
    id,
    title,
    content,
    created_at,
    users(email, name)
  `)

// 結果:
// [
//   {
//     id: "post-1",
//     title: "...",
//     content: "...",
//     created_at: "...",
//     users: {
//       email: "user@example.com",
//       name: "山田太郎"
//     }
//   }
// ]
```

---

## ステップ 7: リアルタイム同期（Subscriptions）

DB のデータが変更されたとき、リアルタイムでクライアント側に通知：

### 7-1. 新規投稿が追加されたとき

```typescript
import { useEffect } from 'react'
import { supabase } from '@/lib/supabase'

export function usePostsRealtime() {
  useEffect(() => {
    // posts テーブルの INSERT イベントを監視
    const subscription = supabase
      .channel('posts')
      .on(
        'postgres_changes',
        { event: 'INSERT', schema: 'public', table: 'posts' },
        (payload) => {
          console.log('新しい投稿:', payload.new)
          // UI を更新
        }
      )
      .subscribe()

    // クリーンアップ
    return () => {
      subscription.unsubscribe()
    }
  }, [])
}
```

### 7-2. 特定の行の変更を監視

```typescript
// user_id が "uuid-1" の投稿の変更を監視
const subscription = supabase
  .channel('posts-user-1')
  .on(
    'postgres_changes',
    {
      event: '*',  // INSERT, UPDATE, DELETE すべてを監視
      schema: 'public',
      table: 'posts',
      filter: `user_id=eq.uuid-1`
    },
    (payload) => {
      console.log('変更内容:', payload)
    }
  )
  .subscribe()
```

---

## curl での直接リクエスト（参考）

JavaScript SDK を使わずに REST API を直接呼び出す場合：

```bash
# すべてのユーザーを取得
curl -H "apikey: YOUR_ANON_KEY" \
  https://xxxxx.supabase.co/rest/v1/users

# フィルタリング
curl -H "apikey: YOUR_ANON_KEY" \
  "https://xxxxx.supabase.co/rest/v1/users?email=like.%25example.com%25"

# 新規作成
curl -X POST \
  -H "apikey: YOUR_ANON_KEY" \
  -H "Content-Type: application/json" \
  -d '{"email":"new@example.com","name":"新規ユーザー"}' \
  https://xxxxx.supabase.co/rest/v1/users
```

---

## 🎉 ここまで完了！

REST API の主要な操作をマスターしました。

次のステップ：
- 👉 [RLS ガイド](04_RLSガイド.md) — セキュリティ強化

---

## 🆘 よくあるエラー

### Q: 「401 Unauthorized」エラー

**答え**: API キーが間違っているか、JWT トークンが無効です。以下を確認：
- 環境変数が正しく設定されているか
- ログインしているか

### Q: 「403 Forbidden」エラー

**答え**: RLS ポリシーで制限されています。次のガイド（RLS）を参照してください。

### Q: レスポンスが空配列 `[]` で返される

**答え**: フィルタリング条件に該当するデータがないか、RLS ポリシーで非表示になっています。

---

**次は RLS でセキュリティを強化します！**
