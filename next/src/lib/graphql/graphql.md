# GraphQL 設定ガイド

このプロジェクトでは、GraphQLを以下のように使い分けます:

## CSR (Client-Side Rendering) - urql使用

クライアントサイドでのGraphQLクエリには**urql**を使用します。

### 設定ファイル
- `src/lib/graphql/urqlClient.ts` - urqlクライアントの設定

### 使用例
```typescript
'use client'
import { useQuery } from 'urql';

const QUERY = `
  query {
    users {
      id
      name
      email
    }
  }
`;

export default function UsersPage() {
  const [result] = useQuery({ query: QUERY });
  
  if (result.fetching) return <div>Loading...</div>;
  if (result.error) return <div>Error: {result.error.message}</div>;
  
  return (
    <div>
      {result.data.users.map(user => (
        <div key={user.id}>{user.name}</div>
      ))}
    </div>
  );
}
```

## SSR (Server-Side Rendering) - Prisma使用

サーバーサイドでのデータ取得には**Prisma**を使用します。

### 設定ファイル
- `src/lib/prisma/schema.prisma` - Prismaスキーマ定義
- `src/lib/prisma/client.ts` - Prismaクライアント

### 使用例
```typescript
import { prisma } from '@/lib/prisma/client';

export default async function UsersPage() {
  const users = await prisma.user.findMany();
  
  return (
    <div>
      {users.map(user => (
        <div key={user.id}>{user.name}</div>
      ))}
    </div>
  );
}
```

## GraphQL エンドポイント

CSR用のGraphQLエンドポイントは環境変数で設定します:
```
NEXT_PUBLIC_GRAPHQL_ENDPOINT=http://localhost:4000/graphql
```
