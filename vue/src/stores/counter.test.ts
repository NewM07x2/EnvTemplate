import { describe, it, expect } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useCounterStore } from './counter'

describe('Counter Store', () => {
  it('初期状態を返す', () => {
    setActivePinia(createPinia())
    const store = useCounterStore()
    expect(store.count).toBe(0)
  })

  it('incrementで値が1増加する', () => {
    setActivePinia(createPinia())
    const store = useCounterStore()
    store.increment()
    expect(store.count).toBe(1)
  })

  it('decrementで値が1減少する', () => {
    setActivePinia(createPinia())
    const store = useCounterStore()
    store.decrement()
    expect(store.count).toBe(-1)
  })

  it('incrementByAmountで指定した値だけ増加する', () => {
    setActivePinia(createPinia())
    const store = useCounterStore()
    store.incrementByAmount(5)
    expect(store.count).toBe(5)
  })

  it('doubleCountが正しく計算される', () => {
    setActivePinia(createPinia())
    const store = useCounterStore()
    store.incrementByAmount(3)
    expect(store.doubleCount).toBe(6)
  })

  it('複数のアクションを連続して実行できる', () => {
    setActivePinia(createPinia())
    const store = useCounterStore()
    store.increment()
    store.increment()
    store.incrementByAmount(3)
    expect(store.count).toBe(5)
  })
})
