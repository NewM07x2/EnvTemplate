<template>
  <div class="min-h-screen bg-gray-50">
    <!-- ヘッダー -->
    <header class="bg-white shadow-sm">
      <nav class="container mx-auto px-4 py-4">
        <div class="flex items-center justify-between">
          <NuxtLink to="/" class="text-2xl font-bold text-green-600">
            Nuxt Template
          </NuxtLink>
          <div class="flex gap-4">
            <NuxtLink to="/" class="text-gray-600 hover:text-green-600">
              ホーム
            </NuxtLink>
            <NuxtLink to="/graphql" class="text-gray-600 hover:text-green-600">
              GraphQL
            </NuxtLink>
            <NuxtLink to="/prisma" class="text-gray-600 hover:text-green-600">
              Prisma
            </NuxtLink>
            <NuxtLink to="/about" class="text-gray-600 hover:text-green-600">
              About
            </NuxtLink>
          </div>
        </div>
      </nav>
    </header>

    <!-- メインコンテンツ -->
    <main class="container mx-auto px-4 py-8">
      <slot />
    </main>

    <!-- フッター -->
    <footer class="bg-gray-900 text-white py-8 mt-16">
      <div class="container mx-auto px-4 text-center">
        <p>&copy; 2026 Nuxt Template. All rights reserved.</p>
      </div>
    </footer>
  </div>
</template>
