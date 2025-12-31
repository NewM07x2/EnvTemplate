# GraphQL データ取得ガイド (Vue)

このドキュメントでは、Vue アプリケーションでの**CSR (Client-Side Rendering)** における urql の使用方法と、
API エンドポイント経由での**Prisma**の使用方法について説明します。

## 📡 CSR: urql を使用した GraphQL データ取得

### 概要

- **用途**: クライアントサイドでの GraphQL データ取得
- **レンダリング**: CSR (Client-Side Rendering)
- **エンドポイント**: `http://localhost:8080/graphql` (環境変数で変更可能)

### 設定

`src/lib/graphql/urqlClient.ts`:

```typescript
import { createClient, fetchExchange } from '@urql/core'

const GRAPHQL_ENDPOINT =
  import.meta.env.VITE_GRAPHQL_ENDPOINT || 'http://localhost:8080/graphql'

export const urqlClient = createClient({
  url: GRAPHQL_ENDPOINT,
  exchanges: [fetchExchange]
})
```

### 使用例

```vue
<template>
  <div>
    <div v-if="fetching">読み込み中...</div>
    <div v-else-if="error">エラー: {{ error.message }}</div>
    <ul v-else>
      <li v-for="user in data.users" :key="user.id">
        {{ user.username }}
      </li>
    </ul>
  </div>
</template>

<script setup lang="ts">
import { useQuery } from '@urql/vue'

const USERS_QUERY = `
  query {
    users {
      id
      username
      email
    }
  }
`

const { data, fetching, error } = useQuery({ query: USERS_QUERY })
</script>
```

### Mutation の例

```vue
<template>
  <form @submit.prevent="handleSubmit">
    <input v-model="username" placeholder="ユーザー名" />
    <input v-model="email" placeholder="メール" />
    <button type="submit" :disabled="fetching">作成</button>
  </form>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useMutation } from '@urql/vue'

const username = ref('')
const email = ref('')

const CREATE_USER_MUTATION = `
  mutation CreateUser($username: String!, $email: String!) {
    createUser(input: { username: $username, email: $email }) {
      id
      username
      email
    }
  }
`

const { executeMutation, fetching } = useMutation(CREATE_USER_MUTATION)

const handleSubmit = async () => {
  const result = await executeMutation({
    username: username.value,
    email: email.value
  })

  if (result.data) {
    username.value = ''
    email.value = ''
  }
}
</script>
```

## 🗄️ Prisma を使用した API 経由のデータ取得

### 概要

Vue は純粋なクライアントサイドフレームワークのため、完全な SSR はサポートしていません。
しかし、Express 等のバックエンド API 経由で Prisma を使用することで、サーバーサイドのデータアクセスを実現できます。

### アーキテクチャ

```
Vue (Frontend) → Axios → Express API (Backend) → Prisma → PostgreSQL
```

### フロントエンド実装例

```vue
<template>
  <div>
    <div v-if="loading">読み込み中...</div>
    <ul v-else>
      <li v-for="user in users" :key="user.id">
        {{ user.username }}
      </li>
    </ul>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import axios from 'axios'

interface User {
  id: number
  username: string
  email: string
}

const users = ref<User[]>([])
const loading = ref(true)

onMounted(async () => {
  const response = await axios.get('/api/users')
  users.value = response.data
  loading.value = false
})
</script>
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

- **Nuxt.js** - Vue 製 SSR フレームワーク (推奨)
- **Quasar** - Vue 製フルスタックフレームワーク

### セキュリティ

- フロントエンドに機密情報を含めないこと
- API 認証・認可を適切に実装すること
- 環境変数を使用して設定を管理すること

## 🔗 参考リンク

- [urql 公式ドキュメント](https://formidable.com/open-source/urql/docs/)
- [Prisma 公式ドキュメント](https://www.prisma.io/docs)
- [Vue Composition API](https://vuejs.org/guide/extras/composition-api-faq.html)
