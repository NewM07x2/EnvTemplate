<script lang="ts">
	// Svelte 5 Runes API
	let count = $state(0);
	let doubled = $derived(count * 2);
	let isEven = $derived(count % 2 === 0);

	function increment() {
		count++;
	}

	function decrement() {
		count--;
	}

	function reset() {
		count = 0;
	}
</script>

<div class="counter">
	<h2>Svelte 5 Counter</h2>
	
	<div class="display">
		<div class="count-value">{count}</div>
		<div class="derived-info">
			<span>2倍: {doubled}</span>
			<span class="badge" class:even={isEven} class:odd={!isEven}>
				{isEven ? '偶数' : '奇数'}
			</span>
		</div>
	</div>

	<div class="buttons">
		<button onclick={decrement} class="btn btn-danger">-1</button>
		<button onclick={reset} class="btn btn-secondary">Reset</button>
		<button onclick={increment} class="btn btn-primary">+1</button>
	</div>

	<p class="info">
		Svelte 5の<code>$state</code>と<code>$derived</code>を使用しています
	</p>
</div>

<style>
	.counter {
		background: white;
		padding: 2rem;
		border-radius: 12px;
		box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
		max-width: 500px;
		margin: 2rem auto;
	}

	h2 {
		text-align: center;
		margin-bottom: 1.5rem;
		color: #333;
	}

	.display {
		text-align: center;
		margin-bottom: 2rem;
	}

	.count-value {
		font-size: 4rem;
		font-weight: bold;
		color: #4075a6;
		margin-bottom: 1rem;
	}

	.derived-info {
		display: flex;
		justify-content: center;
		gap: 1rem;
		font-size: 1.1rem;
		color: #666;
	}

	.badge {
		padding: 0.25rem 0.75rem;
		border-radius: 12px;
		font-weight: 600;
		font-size: 0.9rem;
	}

	.badge.even {
		background: #d4edda;
		color: #155724;
	}

	.badge.odd {
		background: #f8d7da;
		color: #721c24;
	}

	.buttons {
		display: flex;
		gap: 1rem;
		justify-content: center;
		margin-bottom: 1rem;
	}

	.btn {
		padding: 0.75rem 1.5rem;
		border: none;
		border-radius: 6px;
		font-size: 1rem;
		font-weight: 600;
		cursor: pointer;
		transition: transform 0.1s, box-shadow 0.2s;
	}

	.btn:hover {
		transform: translateY(-2px);
		box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
	}

	.btn:active {
		transform: translateY(0);
	}

	.btn-primary {
		background: #4075a6;
		color: white;
	}

	.btn-danger {
		background: #dc3545;
		color: white;
	}

	.btn-secondary {
		background: #6c757d;
		color: white;
	}

	.info {
		text-align: center;
		font-size: 0.9rem;
		color: #999;
		margin: 0;
	}

	code {
		background: #f5f5f5;
		padding: 0.2rem 0.4rem;
		border-radius: 3px;
		font-family: 'Courier New', monospace;
		color: #d63384;
	}
</style>
