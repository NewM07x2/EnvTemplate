import { describe, it, expect } from 'vitest'
import { urqlClient } from './urqlClient'

describe('urqlClient', () => {
  it('urqlクライアントが正しく初期化される', () => {
    expect(urqlClient).toBeDefined()
  })

  it('正しいURLが設定されている', () => {
    // @ts-expect-error - urlプロパティはprivateだがテストのためアクセス
    const url = urqlClient.url
    expect(url).toBeDefined()
    expect(typeof url).toBe('string')
  })

  it('exchangesが設定されている', () => {
    // @ts-expect-error - exchangesプロパティはprivateだがテストのためアクセス
    const exchanges = urqlClient.exchanges
    expect(exchanges).toBeDefined()
    expect(Array.isArray(exchanges)).toBe(true)
  })
})
