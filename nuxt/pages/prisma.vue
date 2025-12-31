<template>
  <div class="max-w-4xl mx-auto">
    <h1 class="text-4xl font-bold text-gray-900 mb-8">Prisma (SSR) - データベースアクセス</h1>

    <div class="bg-white p-8 rounded-lg shadow-md mb-8">
      <h2 class="text-2xl font-semibold text-gray-900 mb-4">🗄️ サーバーサイドレンダリング</h2>
      <p class="text-gray-600 mb-4">
        Prismaを使用したデータベースアクセスの例です。サーバーサイドでデータを取得します。
      </p>

      <div v-if="pending" class="text-center py-8">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-green-600 mx-auto"></div>
        <p class="text-gray-600 mt-4">Loading...</p>
      </div>

      <div v-else-if="error" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
        <p class="font-semibold">エラーが発生しました:</p>
        <p>{{ error.message }}</p>
      </div>

      <div v-else class="space-y-4">
        <div class="bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded">
          <p>データベース接続: OK</p>
          <p class="text-sm mt-2">※ 実際のデータベースに接続する場合は、マイグレーションを実行してください。</p>
        </div>

        <div v-if="data && data.users">
          <h3 class="font-semibold mb-2">ユーザー一覧:</h3>
          <ul class="space-y-2">
            <li v-for="user in data.users" :key="user.id" class="bg-white p-4 rounded border">
              <p class="font-semibold">{{ user.username }}</p>
              <p class="text-sm text-gray-600">{{ user.email }}</p>
            </li>
          </ul>
        </div>
      </div>
    </div>

    <div class="bg-blue-50 p-6 rounded-lg">
      <h3 class="font-semibold mb-2">Prisma使用例（SSR）:</h3>
      <pre class="bg-gray-800 text-white p-4 rounded overflow-x-auto text-sm"><code>// server/api/users.get.ts
import { prisma } from '~/lib/prisma/client'

export default defineEventHandler(async (event) => {
  const users = await prisma.user.findMany()
  return { users }
})

// pages/prisma.vue
const { data, pending, error } = await useFetch('/api/users')</code></pre>
    </div>

    <div class="mt-8 text-center">
      <NuxtLink to="/" class="text-green-600 hover:underline">← ホームに戻る</NuxtLink>
    </div>
  </div>
</template>

<script setup lang="ts">
// Nuxt 3のuseFetchを使用してAPIルートを呼び出す
// サーバーサイドで実行され、結果がハイドレーションされる
const { data, pending, error } = await useFetch('/api/users')

useHead({
  title: 'Prisma - Nuxt テンプレート',
  meta: [
    { name: 'description', content: 'Prismaを使用したデータベースアクセスの例' }
  ]
})
</script>
