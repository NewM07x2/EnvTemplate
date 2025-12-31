<script lang="ts">
	import Counter from '$components/Counter.svelte';
</script>

<div class="counter-page">
	<h1>🔢 Counter</h1>
	<p class="description">
		Svelte 5の新しいRunes API ($state, $derived, $effect) を使用したリアクティブなカウンター
	</p>

	<Counter />

	<section class="explanation">
		<h2>Svelte 5 Runes について</h2>
		
		<div class="rune-card">
			<h3>$state</h3>
			<p>リアクティブな状態を作成</p>
			<pre><code>let count = $state(0);</code></pre>
		</div>

		<div class="rune-card">
			<h3>$derived</h3>
			<p>他の状態から派生する値を計算</p>
			<pre><code>let doubled = $derived(count * 2);</code></pre>
		</div>

		<div class="rune-card">
			<h3>$effect</h3>
			<p>状態変化時に副作用を実行</p>
			<pre><code>$effect(() =&gt; console.log(count));</code></pre>
		</div>
	</section>
</div>

<style>
	.counter-page {
		max-width: 800px;
		margin: 0 auto;
	}

	h1 {
		font-size: 2.5rem;
		margin-bottom: 0.5rem;
		color: #333;
	}

	.description {
		color: #666;
		margin-bottom: 2rem;
		font-size: 1.1rem;
	}

	.explanation {
		margin-top: 3rem;
	}

	h2 {
		font-size: 2rem;
		margin-bottom: 1.5rem;
		color: #333;
	}

	.rune-card {
		background: white;
		padding: 1.5rem;
		border-radius: 8px;
		box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
		margin-bottom: 1rem;
	}

	.rune-card h3 {
		color: #4075a6;
		margin-bottom: 0.5rem;
	}

	.rune-card p {
		color: #666;
		margin-bottom: 0.75rem;
	}

	.rune-card pre {
		background: #f5f5f5;
		padding: 0.75rem;
		border-radius: 4px;
		overflow-x: auto;
	}

	.rune-card code {
		font-family: 'Courier New', monospace;
		font-size: 0.9rem;
		color: #d63384;
	}
</style>
