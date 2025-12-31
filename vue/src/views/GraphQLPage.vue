<template>
  <div>
    <h1>GraphQL (CSR) - urql</h1>
    
    <div v-if="fetching" class="loading">読み込み中...</div>
    
    <div v-else-if="error" class="error">
      エラー: {{ error.message }}
      <p style="margin-top: 1rem; font-size: 0.9rem;">
        GraphQL APIサーバーが起動していることを確認してください。
      </p>
    </div>
    
    <template v-else>
      <div class="card">
        <h2>📡 urqlを使用したデータ取得</h2>
        <p>
          このページでは、<code>urql</code>を使用してGraphQL APIからデータを取得します。
          クライアントサイドレンダリング (CSR) で動作します。
        </p>
      </div>

      <div class="card">
        <h2>👥 ユーザー一覧</h2>
        <ul v-if="data?.users?.length > 0" style="list-style: none; padding: 0;">
          <li v-for="user in data.users" :key="user.id" style="margin-bottom: 0.5rem;">
            <strong>{{ user.username }}</strong> - {{ user.email }}
          </li>
        </ul>
        <p v-else>データがありません</p>
      </div>

      <div class="card">
        <h2>💻 コード例</h2>
        <pre>{{ codeExample }}</pre>
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
import { useQuery } from '@urql/vue'

const USERS_QUERY = `
  query {
    users {
      id
      username
      email
    }
  }
`

const { data, fetching, error } = useQuery({ query: USERS_QUERY })

const codeExample = `import { useQuery } from '@urql/vue'

const USERS_QUERY = \`
  query {
    users {
      id
      username
      email
    }
  }
\`

const { data, fetching, error } = useQuery({ query: USERS_QUERY })`
</script>
