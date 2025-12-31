function HomePage() {
  return (
    <div>
      <h1>React + GraphQL + Prisma テンプレート</h1>
      
      <div className="card">
        <h2>🎯 このテンプレートについて</h2>
        <p>
          このテンプレートは、React + TypeScript + Docker + GraphQL (urql) + Prisma (SSR)
          の環境を提供します。
        </p>
      </div>

      <div className="card">
        <h2>📦 主な技術スタック</h2>
        <ul>
          <li><strong>React 18</strong> - UIライブラリ</li>
          <li><strong>TypeScript</strong> - 型安全性</li>
          <li><strong>Vite</strong> - ビルドツール</li>
          <li><strong>urql</strong> - CSR用GraphQLクライアント</li>
          <li><strong>Prisma</strong> - SSR用ORM・データベースクライアント</li>
          <li><strong>Redux Toolkit</strong> - 状態管理</li>
          <li><strong>React Router</strong> - ルーティング</li>
          <li><strong>PostgreSQL</strong> - データベース</li>
          <li><strong>Docker</strong> - コンテナ化</li>
        </ul>
      </div>

      <div className="card">
        <h2>🚀 使い方</h2>
        <p>上のナビゲーションから各ページを確認してください：</p>
        <ul>
          <li><strong>GraphQL (CSR)</strong> - urqlを使用したクライアントサイドデータ取得</li>
          <li><strong>Prisma (SSR)</strong> - Prismaを使用したサーバーサイドデータ取得 (API経由)</li>
        </ul>
      </div>

      <div className="card">
        <h2>📚 ドキュメント</h2>
        <p>詳細は <code>README.md</code> を参照してください。</p>
      </div>
    </div>
  )
}

export default HomePage
