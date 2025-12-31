import { describe, it, expect } from 'vitest'
import counterReducer, {
  increment,
  decrement,
  incrementByAmount,
} from './counterSlice'

describe('counterSlice', () => {
  const initialState = { value: 0 }

  it('初期状態が正しく設定される', () => {
    expect(counterReducer(undefined, { type: 'unknown' })).toEqual({
      value: 0,
    })
  })

  it('incrementアクションで値が増加する', () => {
    const actual = counterReducer(initialState, increment(5))
    expect(actual.value).toBe(5)
  })

  it('decrementアクションで値が減少する', () => {
    const previousState = { value: 10 }
    const actual = counterReducer(previousState, decrement())
    expect(actual.value).toBe(9)
  })

  it('incrementByAmountアクションで指定された値だけ増加する', () => {
    const actual = counterReducer(initialState, incrementByAmount(10))
    expect(actual.value).toBe(10)
  })

  it('連続したアクションが正しく動作する', () => {
    let state = counterReducer(initialState, increment(5))
    state = counterReducer(state, increment(3))
    state = counterReducer(state, decrement())
    expect(state.value).toBe(7)
  })
})
