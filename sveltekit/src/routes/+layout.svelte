<script lang="ts">
	import { page } from '$app/stores';
	import '../app.css';

	let { children } = $props();
</script>

<svelte:head>
	<title>SvelteKit Template</title>
	<meta name="description" content="SvelteKit + Prisma + TypeScript Template" />
</svelte:head>

<div class="app">
	<header>
		<nav>
			<ul>
				<li>
					<a href="/" class:active={$page.url.pathname === '/'}>Home</a>
				</li>
				<li>
					<a href="/users" class:active={$page.url.pathname === '/users'}>Users</a>
				</li>
				<li>
					<a href="/counter" class:active={$page.url.pathname === '/counter'}>Counter</a>
				</li>
				<li>
					<a href="/about" class:active={$page.url.pathname === '/about'}>About</a>
				</li>
			</ul>
		</nav>
	</header>

	<main>
		{@render children()}
	</main>

	<footer>
		<p>&copy; 2026 SvelteKit Template</p>
	</footer>
</div>

<style>
	.app {
		display: flex;
		flex-direction: column;
		min-height: 100vh;
	}

	header {
		background: #4075a6;
		color: white;
		padding: 1rem 2rem;
		box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
	}

	nav ul {
		display: flex;
		gap: 2rem;
		list-style: none;
		margin: 0;
		padding: 0;
	}

	nav a {
		color: white;
		text-decoration: none;
		font-weight: 500;
		padding: 0.5rem 1rem;
		border-radius: 4px;
		transition: background 0.2s;
	}

	nav a:hover {
		background: rgba(255, 255, 255, 0.1);
	}

	nav a.active {
		background: rgba(255, 255, 255, 0.2);
	}

	main {
		flex: 1;
		padding: 2rem;
		max-width: 1200px;
		margin: 0 auto;
		width: 100%;
	}

	footer {
		background: #f5f5f5;
		padding: 1rem;
		text-align: center;
		color: #666;
		border-top: 1px solid #ddd;
	}
</style>
