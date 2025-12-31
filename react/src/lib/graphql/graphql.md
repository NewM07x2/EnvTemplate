# GraphQL データ取得ガイド (React)

このドキュメントでは、React アプリケーションでの**CSR (Client-Side Rendering)** における urql の使用方法と、
API エンドポイント経由での**Prisma**の使用方法について説明します。

## 📡 CSR: urql を使用した GraphQL データ取得

### 概要

- **用途**: クライアントサイドでの GraphQL データ取得
- **レンダリング**: CSR (Client-Side Rendering)
- **エンドポイント**: `http://localhost:8080/graphql` (環境変数で変更可能)

### 設定

`src/lib/graphql/urqlClient.ts`:

```typescript
import { createClient, fetchExchange } from 'urql'

const GRAPHQL_ENDPOINT =
  import.meta.env.VITE_GRAPHQL_ENDPOINT || 'http://localhost:8080/graphql'

export const urqlClient = createClient({
  url: GRAPHQL_ENDPOINT,
  exchanges: [fetchExchange]
})
```

### 使用例

```typescript
import { useQuery } from 'urql'

const USERS_QUERY = `
  query {
    users {
      id
      username
      email
    }
  }
`

function UsersComponent() {
  const [result] = useQuery({ query: USERS_QUERY })

  if (result.fetching) return <div>読み込み中...</div>
  if (result.error) return <div>エラー: {result.error.message}</div>

  return (
    <ul>
      {result.data.users.map((user) => (
        <li key={user.id}>{user.username}</li>
      ))}
    </ul>
  )
}
```

### Mutation の例

```typescript
import { useMutation } from 'urql'

const CREATE_USER_MUTATION = `
  mutation CreateUser($username: String!, $email: String!) {
    createUser(input: { username: $username, email: $email }) {
      id
      username
      email
    }
  }
`

function CreateUserForm() {
  const [result, createUser] = useMutation(CREATE_USER_MUTATION)

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    createUser({ username: 'newuser', email: 'user@example.com' })
  }

  return <form onSubmit={handleSubmit}>...</form>
}
```

## 🗄️ Prisma を使用した API 経由のデータ取得

### 概要

React は純粋なクライアントサイドフレームワークのため、完全な SSR はサポートしていません。
しかし、Express 等のバックエンド API 経由で Prisma を使用することで、サーバーサイドのデータアクセスを実現できます。

### アーキテクチャ

```
React (Frontend) → Axios → Express API (Backend) → Prisma → PostgreSQL
```

### フロントエンド実装例

```typescript
import { useEffect, useState } from 'react'
import axios from 'axios'

function UsersComponent() {
  const [users, setUsers] = useState([])

  useEffect(() => {
    const fetchUsers = async () => {
      const response = await axios.get('/api/users')
      setUsers(response.data)
    }
    fetchUsers()
  }, [])

  return (
    <ul>
      {users.map((user) => (
        <li key={user.id}>{user.username}</li>
      ))}
    </ul>
  )
}
```

### バックエンド実装例 (Express + Prisma)

バックエンド API サーバーが必要です。以下は実装例です:

```typescript
// server.ts
import express from 'express'
import { PrismaClient } from '@prisma/client'

const app = express()
const prisma = new PrismaClient()

app.get('/api/users', async (req, res) => {
  const users = await prisma.user.findMany()
  res.json(users)
})

app.post('/api/users', async (req, res) => {
  const user = await prisma.user.create({
    data: req.body
  })
  res.json(user)
})

app.listen(3001, () => {
  console.log('API server running on http://localhost:3001')
})
```

## 🔄 使い分けの基準

### urql (CSR) を使う場合

- リアルタイム更新が必要なとき
- ユーザーインタラクション後のデータ取得
- GraphQL API が既に存在する場合
- クライアントサイドのみで完結する機能

### Prisma (API 経由) を使う場合

- データベースへの直接アクセスが効率的な場合
- 複雑なデータベースクエリが必要なとき
- トランザクション処理が必要なとき
- セキュアなデータアクセスが必要な場合

## 📝 注意事項

### SSR について

完全な SSR (Server-Side Rendering) を実現するには、以下のフレームワークの使用を検討してください:

- **Next.js** - React 製 SSR フレームワーク (推奨)
- **Remix** - React 製フルスタックフレームワーク
- **Gatsby** - React 製静的サイトジェネレーター

### セキュリティ

- フロントエンドに機密情報を含めないこと
- API 認証・認可を適切に実装すること
- 環境変数を使用して設定を管理すること

## 🔗 参考リンク

- [urql 公式ドキュメント](https://formidable.com/open-source/urql/docs/)
- [Prisma 公式ドキュメント](https://www.prisma.io/docs)
- [React Router](https://reactrouter.com/)
