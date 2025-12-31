import type { MetaFunction } from "@remix-run/node";
import Counter from "~/components/Counter";

export const meta: MetaFunction = () => {
  return [
    { title: "Counter - Remix Template" },
    { name: "description", content: "React useState demo" },
  ];
};

export default function CounterPage() {
  return (
    <div className="counter-page">
      <h1>🔢 Counter</h1>
      <p className="description">
        Reactの<code>useState</code>フックを使用したカウンター
      </p>

      <Counter />

      <section className="explanation">
        <h2>Remixの特徴</h2>

        <div className="feature-card">
          <h3>🌐 Web Fetch API</h3>
          <p>標準のWeb APIを使用したデータ取得</p>
        </div>

        <div className="feature-card">
          <h3>📝 Form Actions</h3>
          <p>JavaScriptなしで動作するプログレッシブエンハンスメント</p>
        </div>

        <div className="feature-card">
          <h3>⚡ Optimistic UI</h3>
          <p>楽観的UIアップデートによる高速なユーザー体験</p>
        </div>

        <div className="feature-card">
          <h3>🔄 Nested Routes</h3>
          <p>ネストされたルーティングとレイアウト</p>
        </div>
      </section>
    </div>
  );
}
