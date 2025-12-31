import { describe, it, expect, beforeEach } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useCounterStore } from './counter'

describe('counterStore', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('初期状態が正しく設定される', () => {
    const store = useCounterStore()
    expect(store.count).toBe(0)
  })

  it('incrementアクションで値が増加する', () => {
    const store = useCounterStore()
    store.increment()
    expect(store.count).toBe(1)
  })

  it('decrementアクションで値が減少する', () => {
    const store = useCounterStore()
    store.count = 10
    store.decrement()
    expect(store.count).toBe(9)
  })

  it('resetアクションで値が0に戻る', () => {
    const store = useCounterStore()
    store.count = 42
    store.reset()
    expect(store.count).toBe(0)
  })

  it('doubleCountゲッターが正しく動作する', () => {
    const store = useCounterStore()
    store.count = 5
    expect(store.doubleCount).toBe(10)
  })

  it('連続したアクションが正しく動作する', () => {
    const store = useCounterStore()
    store.increment()
    store.increment()
    store.increment()
    store.decrement()
    expect(store.count).toBe(2)
  })
})
