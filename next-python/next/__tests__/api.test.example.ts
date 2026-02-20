/**
 * API ルートテストのテンプレート例
 * 
 * 使用方法:
 * 1. このファイルをコピーして、テストする API ルート名に変更
 * 2. テストケースを追加
 */

// Note: API ルートのテストには別のセットアップが必要です
// Next.js 14 では API テストに jest-mock-extended や node-mocks-http を使用できます

describe('API Routes', () => {
  describe('GET /api/example', () => {
    it('should return 200 status', async () => {
      // const res = await fetch('http://localhost:3000/api/example')
      // expect(res.status).toBe(200)
    })

    it('should return correct data', async () => {
      // const res = await fetch('http://localhost:3000/api/example')
      // const data = await res.json()
      // expect(data).toHaveProperty('message')
    })
  })

  describe('POST /api/example', () => {
    it('should create and return 201 status', async () => {
      // const res = await fetch('http://localhost:3000/api/example', {
      //   method: 'POST',
      //   headers: { 'Content-Type': 'application/json' },
      //   body: JSON.stringify({ name: 'test' }),
      // })
      // expect(res.status).toBe(201)
    })
  })
})
