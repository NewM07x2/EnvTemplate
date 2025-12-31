<div class="about">
	<h1>📘 About</h1>

	<section>
		<h2>テンプレート概要</h2>
		<p>
			このテンプレートは、Svelte 5とSvelteKitを使用した最新のWebアプリケーション開発環境です。
		</p>
		<p>
			Prisma ORMによる型安全なデータベースアクセス、Vitestによるテスト環境、
			Dockerによるコンテナ化が含まれています。
		</p>
	</section>

	<section>
		<h2>技術スタック</h2>
		<ul class="tech-list">
			<li><strong>Svelte 5</strong> - 最新のRunes APIを搭載したUIフレームワーク</li>
			<li><strong>SvelteKit 2</strong> - ファイルベースルーティングとSSR/SSG</li>
			<li><strong>Prisma 6</strong> - 次世代TypeScript ORM</li>
			<li><strong>PostgreSQL 16</strong> - リレーショナルデータベース</li>
			<li><strong>Vitest 2</strong> - 高速テストランナー</li>
			<li><strong>TypeScript 5</strong> - 型安全な開発環境</li>
			<li><strong>Docker Compose</strong> - コンテナオーケストレーション</li>
		</ul>
	</section>

	<section>
		<h2>主な機能</h2>
		<ul class="features-list">
			<li>✅ SSR (Server-Side Rendering)</li>
			<li>✅ SSG (Static Site Generation)</li>
			<li>✅ ファイルベースルーティング</li>
			<li>✅ API Routes (+server.ts)</li>
			<li>✅ Svelte 5 Runes ($state, $derived, $effect)</li>
			<li>✅ Prisma ORM統合</li>
			<li>✅ TypeScript完全対応</li>
			<li>✅ Vitest + Testing Library</li>
			<li>✅ Docker開発環境</li>
		</ul>
	</section>

	<section>
		<h2>始め方</h2>
		<div class="code-block">
			<pre><code># 依存関係のインストール
npm install

# 開発サーバー起動
npm run dev

# Dockerで起動
docker-compose up</code></pre>
		</div>
	</section>

	<section>
		<h2>参考リンク</h2>
		<ul class="links">
			<li><a href="https://svelte.dev/" target="_blank">Svelte公式ドキュメント</a></li>
			<li><a href="https://kit.svelte.dev/" target="_blank">SvelteKit公式ドキュメント</a></li>
			<li><a href="https://www.prisma.io/" target="_blank">Prisma公式ドキュメント</a></li>
			<li><a href="https://vitest.dev/" target="_blank">Vitest公式ドキュメント</a></li>
		</ul>
	</section>
</div>

<style>
	.about {
		max-width: 800px;
		margin: 0 auto;
	}

	h1 {
		font-size: 2.5rem;
		margin-bottom: 2rem;
		color: #333;
	}

	section {
		margin-bottom: 2.5rem;
		background: white;
		padding: 2rem;
		border-radius: 8px;
		box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
	}

	h2 {
		font-size: 1.8rem;
		margin-bottom: 1rem;
		color: #4075a6;
	}

	p {
		color: #666;
		line-height: 1.8;
		margin-bottom: 1rem;
	}

	.tech-list,
	.features-list {
		list-style: none;
		padding: 0;
	}

	.tech-list li,
	.features-list li {
		padding: 0.5rem 0;
		color: #666;
	}

	.tech-list strong {
		color: #4075a6;
	}

	.code-block {
		background: #f5f5f5;
		border-radius: 4px;
		overflow-x: auto;
	}

	.code-block pre {
		margin: 0;
		padding: 1rem;
	}

	.code-block code {
		font-family: 'Courier New', monospace;
		font-size: 0.9rem;
		color: #333;
	}

	.links {
		list-style: none;
		padding: 0;
	}

	.links li {
		margin-bottom: 0.75rem;
	}

	.links a {
		color: #4075a6;
		text-decoration: none;
		font-weight: 500;
		transition: color 0.2s;
	}

	.links a:hover {
		color: #2d5a7b;
		text-decoration: underline;
	}
</style>
