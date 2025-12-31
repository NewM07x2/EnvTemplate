import { describe, it, expect } from 'vitest'

describe('サンプルテスト', () => {
  it('基本的な演算が正しく動作する', () => {
    expect(1 + 1).toBe(2)
  })

  it('配列操作が正しく動作する', () => {
    const array = [1, 2, 3]
    expect(array).toHaveLength(3)
    expect(array).toContain(2)
  })

  it('オブジェクト比較が正しく動作する', () => {
    const obj = { name: 'test', value: 100 }
    expect(obj).toEqual({ name: 'test', value: 100 })
  })
})
