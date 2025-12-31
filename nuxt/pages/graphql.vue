<template>
  <div class="max-w-4xl mx-auto">
    <h1 class="text-4xl font-bold text-gray-900 mb-8">GraphQL (CSR) - urql</h1>

    <div class="bg-white p-8 rounded-lg shadow-md mb-8">
      <h2 class="text-2xl font-semibold text-gray-900 mb-4">🔄 クライアントサイドレンダリング</h2>
      <p class="text-gray-600 mb-4">
        urqlを使用したGraphQLクエリの例です。クライアントサイドでデータを取得します。
      </p>

      <!-- データ取得状態の表示 -->
      <div v-if="fetching" class="text-center py-8">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-green-600 mx-auto"></div>
        <p class="text-gray-600 mt-4">Loading...</p>
      </div>

      <div v-else-if="error" class="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
        <p class="font-semibold">エラーが発生しました:</p>
        <p>{{ error.message }}</p>
      </div>

      <div v-else class="space-y-4">
        <div class="bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded">
          <p>GraphQLエンドポイント: {{ config.public.graphqlEndpoint }}</p>
          <p class="text-sm mt-2">※ サンプルクエリです。実際のGraphQL APIに接続してください。</p>
        </div>
      </div>
    </div>

    <div class="bg-blue-50 p-6 rounded-lg">
      <h3 class="font-semibold mb-2">urql使用例:</h3>
      <pre class="bg-gray-800 text-white p-4 rounded overflow-x-auto text-sm"><code>// composables/useGraphQL.ts
import { useQuery } from '@urql/vue'

export const useUsers = () => {
  const query = `
    query {
      users {
        id
        username
        email
      }
    }
  `
  
  return useQuery({ query })
}</code></pre>
    </div>

    <div class="mt-8 text-center">
      <NuxtLink to="/" class="text-green-600 hover:underline">← ホームに戻る</NuxtLink>
    </div>
  </div>
</template>

<script setup lang="ts">
const config = useRuntimeConfig()

// サンプルクエリ（実際のエンドポイントに接続する場合はコメントを外す）
const SAMPLE_QUERY = `
  query {
    # ここにGraphQLクエリを記述
    # 例: users { id username email }
  }
`

// urql使用例（実際に使用する場合）
// const { data, fetching, error } = await useQuery({ query: SAMPLE_QUERY })

// デモ用のダミーデータ
const fetching = ref(false)
const error = ref(null)
const data = ref(null)

useHead({
  title: 'GraphQL - Nuxt テンプレート',
  meta: [
    { name: 'description', content: 'urqlを使用したGraphQLクエリの例' }
  ]
})
</script>
