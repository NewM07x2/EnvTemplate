import Link from 'next/link';
import Counter from '@/components/Counter';

export default function Home() {
  return (
    <div className="min-h-screen p-8 pb-20 gap-16 sm:p-20">
      <main className="flex flex-col gap-8 items-center">
        <h1 className="text-4xl font-bold text-center">
          🚀 Nest.js + Next.js テンプレート
        </h1>
        
        <p className="text-center text-gray-600 max-w-2xl">
          フルスタックTypeScriptアプリケーション開発のための統合テンプレート
        </p>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 w-full max-w-5xl">
          <div className="p-6 border rounded-lg bg-white shadow-sm">
            <h3 className="font-bold text-lg mb-2">🏗️ バックエンド</h3>
            <p className="text-sm text-gray-600 mb-2">NestJS 10</p>
            <ul className="text-sm text-gray-500 list-disc list-inside">
              <li>GraphQL API</li>
              <li>Prisma ORM</li>
              <li>JWT認証</li>
            </ul>
          </div>

          <div className="p-6 border rounded-lg bg-white shadow-sm">
            <h3 className="font-bold text-lg mb-2">⚡ フロントエンド</h3>
            <p className="text-sm text-gray-600 mb-2">Next.js 14</p>
            <ul className="text-sm text-gray-500 list-disc list-inside">
              <li>App Router</li>
              <li>Apollo Client</li>
              <li>Redux Toolkit</li>
            </ul>
          </div>

          <div className="p-6 border rounded-lg bg-white shadow-sm">
            <h3 className="font-bold text-lg mb-2">🎨 スタイリング</h3>
            <p className="text-sm text-gray-600 mb-2">Tailwind CSS</p>
            <ul className="text-sm text-gray-500 list-disc list-inside">
              <li>ユーティリティファースト</li>
              <li>レスポンシブ対応</li>
            </ul>
          </div>

          <div className="p-6 border rounded-lg bg-white shadow-sm">
            <h3 className="font-bold text-lg mb-2">🗄️ データベース</h3>
            <p className="text-sm text-gray-600 mb-2">PostgreSQL 16</p>
            <ul className="text-sm text-gray-500 list-disc list-inside">
              <li>Docker Compose</li>
              <li>マイグレーション対応</li>
            </ul>
          </div>

          <div className="p-6 border rounded-lg bg-white shadow-sm">
            <h3 className="font-bold text-lg mb-2">🧪 テスト</h3>
            <p className="text-sm text-gray-600 mb-2">Jest & Vitest</p>
            <ul className="text-sm text-gray-500 list-disc list-inside">
              <li>ユニットテスト</li>
              <li>E2Eテスト対応</li>
            </ul>
          </div>

          <div className="p-6 border rounded-lg bg-white shadow-sm">
            <h3 className="font-bold text-lg mb-2">📘 TypeScript</h3>
            <p className="text-sm text-gray-600 mb-2">完全型安全</p>
            <ul className="text-sm text-gray-500 list-disc list-inside">
              <li>フロント〜バックエンド統一</li>
              <li>型推論の活用</li>
            </ul>
          </div>
        </div>

        <div className="w-full max-w-md">
          <Counter />
        </div>

        <div className="flex gap-4 items-center flex-col sm:flex-row">
          <Link
            href="/graphql"
            className="rounded-full border border-solid border-transparent transition-colors flex items-center justify-center bg-foreground text-background gap-2 hover:bg-[#383838] dark:hover:bg-[#ccc] text-sm sm:text-base h-10 sm:h-12 px-4 sm:px-5"
          >
            GraphQL サンプル
          </Link>
          <Link
            href="/users"
            className="rounded-full border border-solid border-black/[.08] dark:border-white/[.145] transition-colors flex items-center justify-center hover:bg-[#f2f2f2] dark:hover:bg-[#1a1a1a] hover:border-transparent text-sm sm:text-base h-10 sm:h-12 px-4 sm:px-5 sm:min-w-44"
          >
            ユーザー一覧
          </Link>
        </div>
      </main>
    </div>
  );
}
