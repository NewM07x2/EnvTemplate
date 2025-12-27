import { prisma } from '@/lib/prisma/client';

// サーバーコンポーネントでPrismaを使用するサンプル
export default async function PrismaExamplePage() {
  // Prismaを使用してデータを取得 (SSR)
  // const users = await prisma.user.findMany();

  return (
    <div className="p-8">
      <h1 className="text-4xl font-bold mb-6">Prisma サンプルページ (SSR)</h1>
      <div className="space-y-4">
        <p className="text-gray-600">
          このページはサーバーサイドレンダリング(SSR)でPrismaを使用する例です。
        </p>
        <div className="bg-green-50 p-4 rounded">
          <h2 className="font-semibold mb-2">Prisma使用例:</h2>
          <pre className="bg-gray-800 text-white p-4 rounded overflow-x-auto">
{`// Server Component
import { prisma } from '@/lib/prisma/client';

export default async function Page() {
  const users = await prisma.user.findMany();
  
  return (
    <div>
      {users.map(user => (
        <div key={user.id}>{user.name}</div>
      ))}
    </div>
  );
}`}
          </pre>
        </div>
        <div className="bg-yellow-50 p-4 rounded">
          <h3 className="font-semibold mb-2">注意:</h3>
          <p className="text-sm">
            データベース接続を有効にするには、<code className="bg-gray-200 px-1 rounded">.env</code>ファイルに
            <code className="bg-gray-200 px-1 rounded">DATABASE_URL</code>を設定してください。
          </p>
        </div>
      </div>
    </div>
  );
}
