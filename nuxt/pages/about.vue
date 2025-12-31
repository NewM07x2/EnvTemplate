<template>
  <div class="max-w-3xl mx-auto">
    <h1 class="text-4xl font-bold text-gray-900 mb-8">About このテンプレート</h1>
    
    <div class="bg-white p-8 rounded-lg shadow-md mb-8">
      <h2 class="text-2xl font-semibold text-gray-900 mb-4">🎯 概要</h2>
      <p class="text-gray-600 mb-4">
        このテンプレートは、Nuxt 3を使用したフルスタックアプリケーションのスターターキットです。
        SSR、CSR、SSGなど、様々なレンダリングモードに対応しています。
      </p>
    </div>

    <div class="bg-white p-8 rounded-lg shadow-md mb-8">
      <h2 class="text-2xl font-semibold text-gray-900 mb-4">🚀 使用方法</h2>
      <ol class="list-decimal list-inside space-y-2 text-gray-600">
        <li>このフォルダをコピー</li>
        <li>環境変数を設定（.env.example → .env）</li>
        <li><code class="bg-gray-100 px-2 py-1 rounded">docker-compose up</code> で起動</li>
        <li>http://localhost:3000 にアクセス</li>
      </ol>
    </div>

    <div class="bg-white p-8 rounded-lg shadow-md">
      <h2 class="text-2xl font-semibold text-gray-900 mb-4">📚 参考リンク</h2>
      <ul class="space-y-2">
        <li>
          <a href="https://nuxt.com" target="_blank" class="text-green-600 hover:underline">
            Nuxt公式ドキュメント
          </a>
        </li>
        <li>
          <a href="https://vuejs.org" target="_blank" class="text-green-600 hover:underline">
            Vue.js
          </a>
        </li>
        <li>
          <a href="https://pinia.vuejs.org" target="_blank" class="text-green-600 hover:underline">
            Pinia
          </a>
        </li>
        <li>
          <a href="https://www.prisma.io" target="_blank" class="text-green-600 hover:underline">
            Prisma
          </a>
        </li>
      </ul>
    </div>

    <div class="mt-8 text-center">
      <NuxtLink to="/" class="text-green-600 hover:underline">← ホームに戻る</NuxtLink>
    </div>
  </div>
</template>

<script setup lang="ts">
useHead({
  title: 'About - Nuxt テンプレート',
  meta: [
    { name: 'description', content: 'Nuxt テンプレートについて' }
  ]
})
</script>
