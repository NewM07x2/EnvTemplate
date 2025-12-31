'use client';

import Link from 'next/link';

export default function GraphQLPage() {
  const apiUrl = process.env.NEXT_PUBLIC_GRAPHQL_ENDPOINT || 'http://localhost:4000/graphql';

  return (
    <div className="min-h-screen p-8">
      <div className="max-w-4xl mx-auto">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold">GraphQL API</h1>
          <Link
            href="/"
            className="px-4 py-2 bg-gray-500 text-white rounded hover:bg-gray-600"
          >
            ホームに戻る
          </Link>
        </div>

        <div className="space-y-6">
          <div className="p-6 border rounded-lg bg-white shadow-sm">
            <h2 className="text-xl font-bold mb-4">🔗 GraphQL エンドポイント</h2>
            <p className="text-gray-700 mb-2">
              バックエンドのGraphQL APIは以下のエンドポイントで利用可能です:
            </p>
            <code className="block p-4 bg-gray-100 rounded text-sm">
              {apiUrl}
            </code>
            <a
              href={apiUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-block mt-4 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
            >
              GraphQL Playground を開く
            </a>
          </div>

          <div className="p-6 border rounded-lg bg-white shadow-sm">
            <h2 className="text-xl font-bold mb-4">📝 クエリ例</h2>
            
            <h3 className="font-semibold mt-4 mb-2">すべてのユーザーを取得:</h3>
            <pre className="p-4 bg-gray-100 rounded text-sm overflow-x-auto">
{`query {
  users {
    id
    email
    username
    createdAt
    posts {
      id
      title
      published
    }
  }
}`}
            </pre>

            <h3 className="font-semibold mt-4 mb-2">ユーザーを作成:</h3>
            <pre className="p-4 bg-gray-100 rounded text-sm overflow-x-auto">
{`mutation {
  createUser(
    email: "test@example.com"
    username: "testuser"
    password: "password123"
  ) {
    id
    email
    username
    createdAt
  }
}`}
            </pre>

            <h3 className="font-semibold mt-4 mb-2">すべての投稿を取得:</h3>
            <pre className="p-4 bg-gray-100 rounded text-sm overflow-x-auto">
{`query {
  posts {
    id
    title
    content
    published
    createdAt
    author {
      id
      username
    }
  }
}`}
            </pre>
          </div>

          <div className="p-6 border rounded-lg bg-white shadow-sm">
            <h2 className="text-xl font-bold mb-4">🛠️ Apollo Client の使用例</h2>
            <p className="text-gray-700 mb-2">
              このプロジェクトでは Apollo Client を使用してGraphQLクエリを実行しています。
            </p>
            <pre className="p-4 bg-gray-100 rounded text-sm overflow-x-auto">
{`import { useQuery } from '@apollo/client';
import { GET_USERS } from '@/lib/graphql/queries';

function MyComponent() {
  const { data, loading, error } = useQuery(GET_USERS);
  
  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error: {error.message}</p>;
  
  return (
    <div>
      {data.users.map(user => (
        <div key={user.id}>{user.username}</div>
      ))}
    </div>
  );
}`}
            </pre>
          </div>
        </div>
      </div>
    </div>
  );
}
