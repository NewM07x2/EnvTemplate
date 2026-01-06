export default function AboutPage() {
  return (
    <div className="max-w-4xl mx-auto">
      <h1 className="text-4xl font-bold text-gray-900 mb-8">
        📘 テンプレート概要
      </h1>

      <section className="bg-white rounded-lg shadow-md p-8 mb-8">
        <h2 className="text-2xl font-semibold text-supabase-green mb-4">
          このテンプレートについて
        </h2>
        <p className="text-gray-700 mb-4 leading-relaxed">
          Next.js + FastAPI + Supabase
          を組み合わせた、モダンなフルスタックWebアプリケーションの開発テンプレートです。
        </p>
        <p className="text-gray-700 leading-relaxed">
          Supabase PostgreSQLをバックエンドデータベースとして使用し、FastAPIでREST
          APIを構築、Next.jsでフロントエンドを実装しています。Docker
          Composeによる完全なコンテナ化で、開発環境のセットアップが簡単です。
        </p>
      </section>

      <section className="bg-white rounded-lg shadow-md p-8 mb-8">
        <h2 className="text-2xl font-semibold text-supabase-green mb-4">
          技術スタック
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h3 className="font-semibold text-lg mb-3">Frontend</h3>
            <ul className="space-y-2 text-gray-700">
              <li>
                <strong>Next.js 15</strong> - App Router、Server Components
              </li>
              <li>
                <strong>React 19</strong> - 最新のReactライブラリ
              </li>
              <li>
                <strong>TypeScript 5</strong> - 型安全な開発
              </li>
              <li>
                <strong>Tailwind CSS</strong> - ユーティリティファーストCSS
              </li>
              <li>
                <strong>Supabase JS</strong> - Supabaseクライアント
              </li>
              <li>
                <strong>Axios</strong> - HTTP通信ライブラリ
              </li>
            </ul>
          </div>
          <div>
            <h3 className="font-semibold text-lg mb-3">Backend</h3>
            <ul className="space-y-2 text-gray-700">
              <li>
                <strong>FastAPI</strong> - 高速なPython Webフレームワーク
              </li>
              <li>
                <strong>Python 3.12</strong> - 最新のPython
              </li>
              <li>
                <strong>Supabase PostgreSQL</strong> - データベース
              </li>
              <li>
                <strong>SQLAlchemy</strong> - PythonのORM
              </li>
              <li>
                <strong>JWT認証</strong> - トークンベース認証
              </li>
              <li>
                <strong>Uvicorn</strong> - ASGIサーバー
              </li>
            </ul>
          </div>
        </div>
      </section>

      <section className="bg-white rounded-lg shadow-md p-8 mb-8">
        <h2 className="text-2xl font-semibold text-supabase-green mb-4">
          主な機能
        </h2>
        <ul className="space-y-3 text-gray-700">
          <li className="flex items-start">
            <span className="text-supabase-green mr-2">✓</span>
            <span>
              <strong>JWT認証システム</strong> -
              ユーザー登録、ログイン、ログアウト
            </span>
          </li>
          <li className="flex items-start">
            <span className="text-supabase-green mr-2">✓</span>
            <span>
              <strong>CRUD API</strong> - ユーザーと投稿の完全な管理機能
            </span>
          </li>
          <li className="flex items-start">
            <span className="text-supabase-green mr-2">✓</span>
            <span>
              <strong>Supabase統合</strong> -
              PostgreSQLデータベースとSupabase機能
            </span>
          </li>
          <li className="flex items-start">
            <span className="text-supabase-green mr-2">✓</span>
            <span>
              <strong>Docker環境</strong> - 完全にコンテナ化された開発環境
            </span>
          </li>
          <li className="flex items-start">
            <span className="text-supabase-green mr-2">✓</span>
            <span>
              <strong>自動API文書</strong> - FastAPIによる自動生成ドキュメント
            </span>
          </li>
          <li className="flex items-start">
            <span className="text-supabase-green mr-2">✓</span>
            <span>
              <strong>テスト環境</strong> - VitestによるE2Eテスト
            </span>
          </li>
        </ul>
      </section>

      <section className="bg-white rounded-lg shadow-md p-8 mb-8">
        <h2 className="text-2xl font-semibold text-supabase-green mb-4">
          クイックスタート
        </h2>
        <div className="bg-gray-900 text-gray-100 rounded-lg p-6 font-mono text-sm overflow-x-auto">
          <pre>{`# リポジトリをクローン
git clone <repository>

# 環境変数を設定
cp .env.example .env

# Dockerで起動
docker-compose up

# アクセス
Frontend: http://localhost:3000
Backend API: http://localhost:8000
API Docs: http://localhost:8000/docs
Supabase Studio: http://localhost:3010`}</pre>
        </div>
      </section>

      <section className="bg-white rounded-lg shadow-md p-8">
        <h2 className="text-2xl font-semibold text-supabase-green mb-4">
          参考リンク
        </h2>
        <ul className="space-y-2">
          <li>
            <a
              href="https://nextjs.org/"
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-600 hover:underline"
            >
              Next.js公式ドキュメント
            </a>
          </li>
          <li>
            <a
              href="https://fastapi.tiangolo.com/"
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-600 hover:underline"
            >
              FastAPI公式ドキュメント
            </a>
          </li>
          <li>
            <a
              href="https://supabase.com/docs"
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-600 hover:underline"
            >
              Supabase公式ドキュメント
            </a>
          </li>
          <li>
            <a
              href="http://localhost:8000/docs"
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-600 hover:underline"
            >
              API Documentation（ローカル）
            </a>
          </li>
        </ul>
      </section>
    </div>
  );
}
