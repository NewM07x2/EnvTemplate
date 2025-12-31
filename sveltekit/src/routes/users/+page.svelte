<script lang="ts">
	import type { PageData } from './$types';

	let { data }: { data: PageData } = $props();
</script>

<div class="users">
	<h1>👥 ユーザー一覧</h1>
	<p class="description">
		Prisma ORMを使用してPostgreSQLからデータを取得しています (SSR)
	</p>

	{#if data.users.length === 0}
		<div class="empty">
			<p>ユーザーが登録されていません。</p>
			<p class="hint">データベースにサンプルデータを追加してください。</p>
		</div>
	{:else}
		<div class="grid">
			{#each data.users as user (user.id)}
				<div class="user-card">
					<div class="user-header">
						<div class="avatar">
							{user.username.charAt(0).toUpperCase()}
						</div>
						<div class="user-info">
							<h3>{user.username}</h3>
							<p class="email">{user.email}</p>
						</div>
					</div>
					<div class="user-meta">
						<p class="date">
							登録日: {new Date(user.createdAt).toLocaleDateString('ja-JP')}
						</p>
						{#if user.posts.length > 0}
							<p class="posts-count">
								投稿: {user.posts.length}件
							</p>
						{/if}
					</div>
				</div>
			{/each}
		</div>
	{/if}
</div>

<style>
	.users {
		max-width: 1000px;
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

	.empty {
		text-align: center;
		padding: 3rem;
		background: #f9f9f9;
		border-radius: 8px;
	}

	.empty p {
		font-size: 1.1rem;
		color: #666;
		margin-bottom: 0.5rem;
	}

	.hint {
		font-size: 0.9rem;
		color: #999;
	}

	.grid {
		display: grid;
		grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
		gap: 1.5rem;
	}

	.user-card {
		background: white;
		padding: 1.5rem;
		border-radius: 12px;
		box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
		transition: transform 0.2s, box-shadow 0.2s;
	}

	.user-card:hover {
		transform: translateY(-4px);
		box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
	}

	.user-header {
		display: flex;
		align-items: center;
		gap: 1rem;
		margin-bottom: 1rem;
	}

	.avatar {
		width: 60px;
		height: 60px;
		border-radius: 50%;
		background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
		display: flex;
		align-items: center;
		justify-content: center;
		color: white;
		font-size: 1.5rem;
		font-weight: bold;
	}

	.user-info h3 {
		margin: 0 0 0.25rem 0;
		font-size: 1.3rem;
		color: #333;
	}

	.email {
		margin: 0;
		color: #666;
		font-size: 0.9rem;
	}

	.user-meta {
		padding-top: 1rem;
		border-top: 1px solid #eee;
	}

	.user-meta p {
		margin: 0.25rem 0;
		font-size: 0.9rem;
		color: #999;
	}

	.posts-count {
		color: #4075a6 !important;
		font-weight: 500;
	}
</style>
