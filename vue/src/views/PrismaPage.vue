<template>
  <div>
    <h1>Prisma (SSR相当) - API経由</h1>
    
    <div v-if="loading" class="loading">読み込み中...</div>
    
    <div v-else-if="errorMsg" class="error">
      {{ errorMsg }}
      <p style="margin-top: 1rem; font-size: 0.9rem;">
        Prisma APIエンドポイントを実装する必要があります。
      </p>
    </div>
    
    <template v-else>
      <div class="card">
        <h2>🗄️ Prismaを使用したデータ取得</h2>
        <p>
          このページでは、バックエンドAPI経由で<code>Prisma</code>を使用してPostgreSQLから
          データを取得します。Vueのみの環境では完全なSSRはできませんが、
          APIエンドポイント経由でサーバーサイドのデータアクセスを実現できます。
        </p>
      </div>

      <div class="card">
        <h2>👥 ユーザー一覧</h2>
        <ul v-if="users.length > 0" style="list-style: none; padding: 0;">
          <li v-for="user in users" :key="user.id" style="margin-bottom: 0.5rem;">
            <strong>{{ user.username }}</strong> - {{ user.email }}
          </li>
        </ul>
        <p v-else>データがありません</p>
      </div>

      <div class="card">
        <h2>💻 コード例</h2>
        <pre>{{ codeExample }}</pre>
      </div>

      <div class="card">
        <h2>📝 注意</h2>
        <p>
          完全なSSR (サーバーサイドレンダリング) を実現するには、Nuxt.jsなどのフレームワークが必要です。
          このVueテンプレートでは、APIエンドポイント経由でのデータ取得を実装することで、
          Prismaの使用例を示しています。
        </p>
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import axios from 'axios'

interface User {
  id: number
  username: string
  email: string
}

const users = ref<User[]>([])
const loading = ref(true)
const errorMsg = ref<string | null>(null)

onMounted(async () => {
  try {
    const response = await axios.get('/api/users')
    users.value = response.data
  } catch (err) {
    errorMsg.value = 'データの取得に失敗しました'
    console.error(err)
  } finally {
    loading.value = false
  }
})

const codeExample = `// フロントエンド (Vue)
const response = await axios.get('/api/users')
users.value = response.data

// バックエンド (Express + Prisma)
app.get('/api/users', async (req, res) => {
  const users = await prisma.user.findMany()
  res.json(users)
})`
</script>
