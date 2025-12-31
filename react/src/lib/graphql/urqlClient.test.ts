import { describe, it, expect } from 'vitest'
import { urqlClient } from './urqlClient'

describe('urqlClient', () => {
  it('urqlクライアントが正しく初期化される', () => {
    expect(urqlClient).toBeDefined()
  })

  it('urlプロパティが存在する', () => {
    expect(urqlClient.url).toBeDefined()
    expect(typeof urqlClient.url).toBe('string')
  })

  it('デフォルトURLまたは環境変数のURLが設定されている', () => {
    const expectedUrl = import.meta.env.VITE_GRAPHQL_ENDPOINT || 'http://localhost:8080/graphql'
    expect(urqlClient.url).toBe(expectedUrl)
  })
})
