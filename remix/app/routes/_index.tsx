import type { MetaFunction } from "@remix-run/node";
import Counter from "~/components/Counter";

export const meta: MetaFunction = () => {
  return [
    { title: "Remix Template" },
    { name: "description", content: "Remix + React Router v7 + Prisma" },
  ];
};

export default function Index() {
  return (
    <div className="home">
      <h1>🚀 Remix Template</h1>
      <p className="subtitle">
        Remix + React Router v7 + Prisma + TypeScript
      </p>

      <section className="features">
        <h2>主な機能</h2>
        <div className="grid">
          <div className="card">
            <h3>⚡ Remix</h3>
            <p>React Router v7ベースの高速フルスタックフレームワーク</p>
          </div>
          <div className="card">
            <h3>🚀 React 18</h3>
            <p>最新のReactとServer Components対応</p>
          </div>
          <div className="card">
            <h3>🗄️ Prisma ORM</h3>
            <p>型安全なデータベースアクセス</p>
          </div>
          <div className="card">
            <h3>📘 TypeScript</h3>
            <p>完全な型安全性</p>
          </div>
          <div className="card">
            <h3>🧪 Vitest</h3>
            <p>高速テストランナー</p>
          </div>
          <div className="card">
            <h3>🐳 Docker</h3>
            <p>コンテナ化された開発環境</p>
          </div>
        </div>
      </section>

      <section className="demo">
        <h2>React State デモ</h2>
        <Counter />
      </section>

      <section className="pages">
        <h2>📂 ページ構成</h2>
        <ul>
          <li>
            <strong>Home</strong> - このページ
          </li>
          <li>
            <strong>Users</strong> - Prismaを使用したユーザー一覧 (SSR)
          </li>
          <li>
            <strong>Counter</strong> - Reactカウンター
          </li>
          <li>
            <strong>About</strong> - テンプレート情報
          </li>
        </ul>
      </section>
    </div>
  );
}
