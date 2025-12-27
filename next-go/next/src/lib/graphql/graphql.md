# GraphQL・データ取得 設定ガイド

このプロジェクトでは、レンダリング方法によってデータ取得方法を使い分けます。

## CSR (Client-Side Rendering) - urql使用

クライアントサイドでデータを取得する場合は**urql**を使用してGo APIのGraphQLエンドポイントにアクセスします。

### 設定ファイル
- src/lib/graphql/urqlClient.ts - urqlクライアントの設定

### 使用例
\\\	ypescript
'use client'
import { useQuery } from 'urql';

const USERS_QUERY = \
  query {
    users {
      id
      username
      email
    }
  }
\;

export default function UsersPage() {
  const [result] = useQuery({ query: USERS_QUERY });
  
  if (result.fetching) return <div>Loading...</div>;
  if (result.error) return <div>Error: {result.error.message}</div>;
  
  return (
    <div>
      {result.data.users.map(user => (
        <div key={user.id}>{user.username}</div>
      ))}
    </div>
  );
}
\\\

### GraphQL エンドポイント
Go Echo APIが提供するGraphQLエンドポイント:
\\\
http://localhost:8080/graphql
\\\

環境変数で設定:
\\\
NEXT_PUBLIC_GRAPHQL_ENDPOINT=http://localhost:8080/graphql
\\\

## SSR (Server-Side Rendering) - Prisma使用

サーバーコンポーネントでデータを取得する場合は**Prisma**を使用してPostgreSQLに直接アクセスします。

### 設定ファイル
- src/lib/prisma/client.ts - Prismaクライアント設定
- src/lib/prisma/schema.prisma - DBスキーマ定義

### 使用例
\\\	ypescript
// 'use client'ディレクティブなし（Server Component）
import { prisma } from '@/lib/prisma/client';

export default async function UsersPage() {
  const users = await prisma.user.findMany({
    include: {
      posts: true
    }
  });
  
  return (
    <div>
      {users.map(user => (
        <div key={user.id}>
          <h2>{user.username}</h2>
          <p>{user.email}</p>
          <p>投稿数: {user.posts.length}</p>
        </div>
      ))}
    </div>
  );
}
\\\

### データベース接続
環境変数で設定:
\\\
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/nextgo_db?schema=public
\\\

## 使い分けの基準

### CSR (urql) を使用する場合
- リアルタイム更新が必要
- ユーザーインタラクション後のデータ取得
- 認証トークンを含むリクエスト
- Go APIの既存GraphQLエンドポイントを活用

### SSR (Prisma) を使用する場合
- 初期ページロード時のデータ取得
- SEOが重要なページ
- データベースへの直接アクセスが効率的
- サーバー側でのデータ加工・集計
