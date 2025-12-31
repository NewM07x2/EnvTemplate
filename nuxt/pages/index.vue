<template>
  <div class="max-w-4xl mx-auto">
    <!-- ヒーローセクション -->
    <section class="text-center mb-16">
      <h1 class="text-5xl font-bold text-gray-900 mb-4">
        Welcome to <span class="text-green-600">Nuxt 3</span>
      </h1>
      <p class="text-xl text-gray-600 mb-8">
        Vue 3の完全なSSRフレームワーク
      </p>
      <div class="flex gap-4 justify-center">
        <a
          href="https://nuxt.com"
          target="_blank"
          class="bg-green-600 text-white px-6 py-3 rounded-lg hover:bg-green-700 transition"
        >
          ドキュメント
        </a>
        <a
          href="https://github.com/nuxt/nuxt"
          target="_blank"
          class="bg-gray-200 text-gray-800 px-6 py-3 rounded-lg hover:bg-gray-300 transition"
        >
          GitHub
        </a>
      </div>
    </section>

    <!-- 技術スタック -->
    <section class="mb-16">
      <h2 class="text-3xl font-bold text-gray-900 mb-6">🛠️ 技術スタック</h2>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div class="bg-white p-6 rounded-lg shadow-md">
          <h3 class="text-xl font-semibold text-green-600 mb-2">Nuxt 3.15</h3>
          <p class="text-gray-600">Vue 3の完全なSSRフレームワーク</p>
        </div>
        <div class="bg-white p-6 rounded-lg shadow-md">
          <h3 class="text-xl font-semibold text-green-600 mb-2">Vue 3.5</h3>
          <p class="text-gray-600">プログレッシブJavaScriptフレームワーク</p>
        </div>
        <div class="bg-white p-6 rounded-lg shadow-md">
          <h3 class="text-xl font-semibold text-green-600 mb-2">Pinia 2.3</h3>
          <p class="text-gray-600">公式状態管理ライブラリ</p>
        </div>
        <div class="bg-white p-6 rounded-lg shadow-md">
          <h3 class="text-xl font-semibold text-green-600 mb-2">urql 1.3</h3>
          <p class="text-gray-600">軽量GraphQLクライアント</p>
        </div>
        <div class="bg-white p-6 rounded-lg shadow-md">
          <h3 class="text-xl font-semibold text-green-600 mb-2">Prisma 6.4</h3>
          <p class="text-gray-600">次世代ORM</p>
        </div>
        <div class="bg-white p-6 rounded-lg shadow-md">
          <h3 class="text-xl font-semibold text-green-600 mb-2">Vitest 2.1</h3>
          <p class="text-gray-600">高速テストフレームワーク</p>
        </div>
      </div>
    </section>

    <!-- カウンター例 -->
    <section class="mb-16">
      <h2 class="text-3xl font-bold text-gray-900 mb-6">🎯 状態管理の例</h2>
      <div class="bg-white p-8 rounded-lg shadow-md">
        <Counter />
      </div>
    </section>

    <!-- 特徴 -->
    <section>
      <h2 class="text-3xl font-bold text-gray-900 mb-6">✨ 特徴</h2>
      <ul class="space-y-4">
        <li class="flex items-start">
          <span class="text-green-600 mr-2">•</span>
          <div>
            <strong>完全なSSR:</strong> サーバーサイドレンダリング対応
          </div>
        </li>
        <li class="flex items-start">
          <span class="text-green-600 mr-2">•</span>
          <div>
            <strong>自動インポート:</strong> コンポーネントやComposablesを自動的にインポート
          </div>
        </li>
        <li class="flex items-start">
          <span class="text-green-600 mr-2">•</span>
          <div>
            <strong>ファイルベースルーティング:</strong> pagesディレクトリから自動生成
          </div>
        </li>
        <li class="flex items-start">
          <span class="text-green-600 mr-2">•</span>
          <div>
            <strong>Data Fetching:</strong> useFetch、useAsyncDataなど便利なComposables
          </div>
        </li>
        <li class="flex items-start">
          <span class="text-green-600 mr-2">•</span>
          <div>
            <strong>TypeScript:</strong> 完全なTypeScriptサポート
          </div>
        </li>
      </ul>
    </section>
  </div>
</template>

<script setup lang="ts">
useHead({
  title: 'Nuxt テンプレート - ホーム',
  meta: [
    { name: 'description', content: 'Nuxt 3 + TypeScript + Prisma テンプレート' }
  ]
})
</script>
