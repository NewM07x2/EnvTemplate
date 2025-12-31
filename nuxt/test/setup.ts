import { afterEach } from 'vitest'
import { cleanup } from '@testing-library/vue'

// テスト後のクリーンアップ
afterEach(() => {
  cleanup()
})

// 環境変数のモック
process.env.NUXT_PUBLIC_GRAPHQL_ENDPOINT = 'http://localhost:8080/graphql'
process.env.DATABASE_URL = 'postgresql://postgres:postgres@localhost:5432/nuxt_db?schema=public'
