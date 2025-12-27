# GraphQL 設定ガイド

## CSR (Client-Side Rendering) - urql 使用

Go Echo API の GraphQL エンドポイント (`http://localhost:8080/graphql`) にアクセスするために **urql** を使用します。

### 設定ファイル

- `src/lib/graphql/urqlClient.ts` - urql クライアントの設定

### 使用例

```typescript
'use client'
import { useQuery } from 'urql'

const USERS_QUERY = `
  query {
    users {
      id
      name
      email
    }
  }
`

export default function UsersPage() {
  const [result] = useQuery({ query: USERS_QUERY })

  if (result.fetching) return <div>Loading...</div>
  if (result.error) return <div>Error: {result.error.message}</div>

  return (
    <div>
      {result.data.users.map((user) => (
        <div key={user.id}>{user.name}</div>
      ))}
    </div>
  )
}
```

## GraphQL エンドポイント

Go Echo API が提供する GraphQL エンドポイント:

```
http://localhost:8080/graphql
```

環境変数で設定:

```
NEXT_PUBLIC_GRAPHQL_ENDPOINT=http://localhost:8080/graphql
```
