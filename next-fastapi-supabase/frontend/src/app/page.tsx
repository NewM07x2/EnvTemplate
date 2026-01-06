export default function Home() {
  return (
    <div className="space-y-12">
      {/* Hero Section */}
      <section className="text-center py-12">
        <h1 className="text-5xl font-bold text-gray-900 mb-4">
          🚀 Next.js + FastAPI + Supabase
        </h1>
        <p className="text-xl text-gray-600 mb-8">
          フルスタックWebアプリケーションテンプレート
        </p>
        <div className="flex justify-center space-x-4">
          <a
            href="/register"
            className="px-6 py-3 bg-supabase-green text-white rounded-lg hover:bg-green-600 font-semibold"
          >
            Get Started
          </a>
          <a
            href="http://localhost:8000/docs"
            target="_blank"
            rel="noopener noreferrer"
            className="px-6 py-3 bg-gray-800 text-white rounded-lg hover:bg-gray-700 font-semibold"
          >
            API Docs
          </a>
        </div>
      </section>

      {/* Features Section */}
      <section>
        <h2 className="text-3xl font-bold text-center mb-8">主な機能</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <FeatureCard
            icon="⚡"
            title="Next.js 15"
            description="最新のApp RouterとServer Componentsで高速なSSR"
          />
          <FeatureCard
            icon="🐍"
            title="FastAPI"
            description="Pythonの高速非同期フレームワーク"
          />
          <FeatureCard
            icon="🗄️"
            title="Supabase"
            description="PostgreSQLベースのBaaS（Backend as a Service）"
          />
          <FeatureCard
            icon="🔐"
            title="JWT認証"
            description="セキュアなトークンベース認証システム"
          />
          <FeatureCard
            icon="🐳"
            title="Docker"
            description="完全なコンテナ化された開発環境"
          />
          <FeatureCard
            icon="📘"
            title="TypeScript"
            description="型安全なフロントエンド開発"
          />
        </div>
      </section>

      {/* Tech Stack Section */}
      <section className="bg-white rounded-lg shadow-lg p-8">
        <h2 className="text-3xl font-bold text-center mb-6">技術スタック</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h3 className="text-xl font-semibold mb-4 text-supabase-green">
              Frontend
            </h3>
            <ul className="space-y-2 text-gray-700">
              <li>✓ Next.js 15（App Router）</li>
              <li>✓ React 19</li>
              <li>✓ TypeScript 5</li>
              <li>✓ Tailwind CSS</li>
              <li>✓ Supabase Client</li>
              <li>✓ Axios</li>
            </ul>
          </div>
          <div>
            <h3 className="text-xl font-semibold mb-4 text-supabase-green">
              Backend
            </h3>
            <ul className="space-y-2 text-gray-700">
              <li>✓ FastAPI</li>
              <li>✓ Python 3.12</li>
              <li>✓ Supabase PostgreSQL</li>
              <li>✓ SQLAlchemy</li>
              <li>✓ JWT認証</li>
              <li>✓ Uvicorn</li>
            </ul>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="bg-supabase-green text-white rounded-lg p-12 text-center">
        <h2 className="text-3xl font-bold mb-4">始めましょう</h2>
        <p className="text-lg mb-6">
          このテンプレートを使って、すぐにフルスタックアプリケーションの開発を始められます
        </p>
        <div className="flex justify-center space-x-4">
          <a
            href="/users"
            className="px-6 py-3 bg-white text-supabase-green rounded-lg hover:bg-gray-100 font-semibold"
          >
            ユーザー管理
          </a>
          <a
            href="/posts"
            className="px-6 py-3 bg-gray-800 text-white rounded-lg hover:bg-gray-700 font-semibold"
          >
            投稿管理
          </a>
        </div>
      </section>
    </div>
  );
}

function FeatureCard({
  icon,
  title,
  description,
}: {
  icon: string;
  title: string;
  description: string;
}) {
  return (
    <div className="bg-white rounded-lg shadow-md p-6 hover:shadow-xl transition-shadow">
      <div className="text-4xl mb-3">{icon}</div>
      <h3 className="text-xl font-semibold mb-2 text-gray-900">{title}</h3>
      <p className="text-gray-600">{description}</p>
    </div>
  );
}
