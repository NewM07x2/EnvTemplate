export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-8">
        <h1 className="text-4xl font-bold text-gray-800 mb-4">
          Next.js + GraphQL + Prisma テンプレート
        </h1>
        <p className="text-lg text-gray-600 mb-8">
          このテンプレートは、GraphQLとPrismaをSSRで利用するNext.jsアプリケーション用です。
        </p>
        
        <div className="bg-white rounded-lg shadow-lg p-8">
          <h2 className="text-2xl font-semibold text-gray-800 mb-6">セットアップ手順</h2>
          
          <ol className="space-y-4 text-gray-700">
            <li className="flex items-start">
              <span className="flex items-center justify-center w-8 h-8 rounded-full bg-blue-500 text-white font-bold mr-4">1</span>
              <span>依存パッケージをインストール: <code className="bg-gray-100 px-2 py-1 rounded">npm install</code></span>
            </li>
            <li className="flex items-start">
              <span className="flex items-center justify-center w-8 h-8 rounded-full bg-blue-500 text-white font-bold mr-4">2</span>
              <span>環境変数を設定: <code className="bg-gray-100 px-2 py-1 rounded">.env.local</code>を作成</span>
            </li>
            <li className="flex items-start">
              <span className="flex items-center justify-center w-8 h-8 rounded-full bg-blue-500 text-white font-bold mr-4">3</span>
              <span>Prismaをセットアップ: <code className="bg-gray-100 px-2 py-1 rounded">npx prisma init</code></span>
            </li>
            <li className="flex items-start">
              <span className="flex items-center justify-center w-8 h-8 rounded-full bg-blue-500 text-white font-bold mr-4">4</span>
              <span>開発サーバーを起動: <code className="bg-gray-100 px-2 py-1 rounded">npm run dev</code></span>
            </li>
          </ol>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-8">
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-xl font-semibold text-blue-600 mb-2">📦 Next.js</h3>
            <p className="text-gray-600">v14.1.0 でモダンなWebアプリを構築</p>
          </div>
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-xl font-semibold text-purple-600 mb-2">🔗 GraphQL</h3>
            <p className="text-gray-600">urql/Next でSSR対応のAPI通信</p>
          </div>
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-xl font-semibold text-emerald-600 mb-2">🗄️ Prisma</h3>
            <p className="text-gray-600">型安全なデータベースアクセス</p>
          </div>
        </div>
      </div>
    </div>
  );
}