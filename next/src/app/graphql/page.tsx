'use client'
import { useQuery } from 'urql';
import Link from 'next/link';

// サンプルGraphQLクエリ (実際のエンドポイントに合わせて変更してください)
const SAMPLE_QUERY = `
  query {
    # ここにGraphQLクエリを記述
    # 例: users { id name email }
  }
`;

export default function GraphqlPage() {
  // urqlを使用したGraphQLクエリの例
  // const [result] = useQuery({ query: SAMPLE_QUERY });

  return (
    <div className="p-8">
      <h1 className="text-4xl font-bold mb-6">GraphQL サンプルページ (CSR)</h1>
      <div className="space-y-4">
        <p className="text-gray-600">
          このページはクライアントサイドレンダリング(CSR)でGraphQLを使用する例です。
        </p>
        <div className="bg-blue-50 p-4 rounded">
          <h2 className="font-semibold mb-2">urql使用例:</h2>
          <pre className="bg-gray-800 text-white p-4 rounded overflow-x-auto">
{`const [result] = useQuery({ query: SAMPLE_QUERY });

if (result.fetching) return <div>Loading...</div>;
if (result.error) return <div>Error: {result.error.message}</div>;

return <div>{JSON.stringify(result.data)}</div>;`}
          </pre>
        </div>
        <Link 
          href="/graphql/get-api" 
          className="inline-block bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
        >
          REST API サンプルへ
        </Link>
      </div>
    </div>
  );
}
