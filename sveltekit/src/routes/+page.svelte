<script lang="ts">
	import Counter from '$components/Counter.svelte';
</script>

<div class="home">
	<h1>🚀 SvelteKit Template</h1>
	<p class="subtitle">Svelte 5 + SvelteKit + Prisma + TypeScript</p>

	<section class="features">
		<h2>主な機能</h2>
		<div class="grid">
			<div class="card">
				<h3>⚡ Svelte 5</h3>
				<p>最新のSvelte 5でRunes APIを活用した高速でリアクティブなUI</p>
			</div>
			<div class="card">
				<h3>🚀 SvelteKit</h3>
				<p>ファイルベースルーティングとSSR/SSG対応フレームワーク</p>
			</div>
			<div class="card">
				<h3>🗄️ Prisma ORM</h3>
				<p>型安全なデータベースアクセスとマイグレーション</p>
			</div>
			<div class="card">
				<h3>📘 TypeScript</h3>
				<p>完全な型安全性とIntelliSense</p>
			</div>
			<div class="card">
				<h3>🧪 Vitest</h3>
				<p>高速テストランナーとカバレッジ</p>
			</div>
			<div class="card">
				<h3>🐳 Docker</h3>
				<p>PostgreSQL + SvelteKitの完全なコンテナ化</p>
			</div>
		</div>
	</section>

	<section class="demo">
		<h2>Svelte 5 Runes デモ</h2>
		<Counter />
	</section>

	<section class="pages">
		<h2>📂 ページ構成</h2>
		<ul>
			<li><strong>Home</strong> - このページ</li>
			<li><strong>Users</strong> - Prismaを使用したユーザー一覧 (SSR)</li>
			<li><strong>Counter</strong> - Svelte 5 Runes ($state/$derived)</li>
			<li><strong>About</strong> - テンプレート情報</li>
		</ul>
	</section>
</div>

<style>
	.home {
		max-width: 900px;
		margin: 0 auto;
	}

	h1 {
		font-size: 3rem;
		text-align: center;
		color: #4075a6;
		margin-bottom: 0.5rem;
	}

	.subtitle {
		text-align: center;
		font-size: 1.2rem;
		color: #666;
		margin-bottom: 3rem;
	}

	section {
		margin-bottom: 3rem;
	}

	h2 {
		font-size: 2rem;
		margin-bottom: 1.5rem;
		color: #333;
	}

	.grid {
		display: grid;
		grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
		gap: 1.5rem;
	}

	.card {
		background: white;
		padding: 1.5rem;
		border-radius: 8px;
		box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
		transition: transform 0.2s, box-shadow 0.2s;
	}

	.card:hover {
		transform: translateY(-4px);
		box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
	}

	.card h3 {
		font-size: 1.3rem;
		margin-bottom: 0.5rem;
		color: #4075a6;
	}

	.card p {
		color: #666;
		line-height: 1.6;
	}

	.demo {
		background: #f9f9f9;
		padding: 2rem;
		border-radius: 8px;
	}

	.pages ul {
		list-style: none;
		padding: 0;
	}

	.pages li {
		padding: 0.75rem 0;
		border-bottom: 1px solid #eee;
	}

	.pages li:last-child {
		border-bottom: none;
	}

	.pages strong {
		color: #4075a6;
	}
</style>
