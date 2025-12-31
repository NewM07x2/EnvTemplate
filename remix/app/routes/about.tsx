import type { MetaFunction } from "@remix-run/node";

export const meta: MetaFunction = () => {
  return [
    { title: "About - Remix Template" },
    { name: "description", content: "About Remix Template" },
  ];
};

export default function About() {
  return (
    <div className="about">
      <h1>📘 About</h1>

      <section className="section">
        <h2>テンプレート概要</h2>
        <p>
          このテンプレートは、Remix（React Router v7ベース）を使用した
          最新のフルスタックWebアプリケーション開発環境です。
        </p>
        <p>
          Prisma ORMによる型安全なデータベースアクセス、Vitestによるテスト環境、
          Dockerによるコンテナ化が含まれています。
        </p>
      </section>

      <section className="section">
        <h2>技術スタック</h2>
        <ul className="tech-list">
          <li>
            <strong>Remix 2</strong> - React Router v7ベースのフルスタックフレームワーク
          </li>
          <li>
            <strong>React 18</strong> - 最新のReactライブラリ
          </li>
          <li>
            <strong>Prisma 6</strong> - 次世代TypeScript ORM
          </li>
          <li>
            <strong>PostgreSQL 16</strong> - リレーショナルデータベース
          </li>
          <li>
            <strong>Vitest 2</strong> - 高速テストランナー
          </li>
          <li>
            <strong>TypeScript 5</strong> - 型安全な開発環境
          </li>
          <li>
            <strong>Vite</strong> - 高速ビルドツール
          </li>
          <li>
            <strong>Docker Compose</strong> - コンテナオーケストレーション
          </li>
        </ul>
      </section>

      <section className="section">
        <h2>主な機能</h2>
        <ul className="features-list">
          <li>✅ SSR (Server-Side Rendering)</li>
          <li>✅ ファイルベースルーティング</li>
          <li>✅ Loader/Action パターン</li>
          <li>✅ Progressive Enhancement</li>
          <li>✅ Optimistic UI</li>
          <li>✅ Nested Routes</li>
          <li>✅ Error Boundary</li>
          <li>✅ Prisma ORM統合</li>
          <li>✅ TypeScript完全対応</li>
          <li>✅ Vitest + Testing Library</li>
          <li>✅ Docker開発環境</li>
        </ul>
      </section>

      <section className="section">
        <h2>始め方</h2>
        <div className="code-block">
          <pre>
            <code>
              {`# 依存関係のインストール
npm install

# 開発サーバー起動
npm run dev

# Dockerで起動
docker-compose up`}
            </code>
          </pre>
        </div>
      </section>

      <section className="section">
        <h2>参考リンク</h2>
        <ul className="links">
          <li>
            <a href="https://remix.run/" target="_blank" rel="noreferrer">
              Remix公式ドキュメント
            </a>
          </li>
          <li>
            <a href="https://reactrouter.com/" target="_blank" rel="noreferrer">
              React Router公式ドキュメント
            </a>
          </li>
          <li>
            <a href="https://www.prisma.io/" target="_blank" rel="noreferrer">
              Prisma公式ドキュメント
            </a>
          </li>
          <li>
            <a href="https://vitest.dev/" target="_blank" rel="noreferrer">
              Vitest公式ドキュメント
            </a>
          </li>
        </ul>
      </section>
    </div>
  );
}
