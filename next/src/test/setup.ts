import '@testing-library/jest-dom'
import { cleanup } from '@testing-library/react'
import { afterEach } from 'vitest'

// テスト後のクリーンアップ
afterEach(() => {
  cleanup()
})

// 環境変数のモック
process.env.NEXT_PUBLIC_GRAPHQL_ENDPOINT = 'http://localhost:8080/graphql'
