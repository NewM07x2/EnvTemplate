import { describe, it, expect } from 'vitest'
import counterReducer, { increment, decrement, incrementByAmount } from './counterSlice'

describe('counterSlice', () => {
  const initialState = {
    value: 0,
  }

  it('初期状態を返す', () => {
    expect(counterReducer(undefined, { type: 'unknown' })).toEqual({
      value: 0,
    })
  })

  it('incrementアクションで値が1増加する', () => {
    const actual = counterReducer(initialState, increment())
    expect(actual.value).toEqual(1)
  })

  it('decrementアクションで値が1減少する', () => {
    const actual = counterReducer(initialState, decrement())
    expect(actual.value).toEqual(-1)
  })

  it('incrementByAmountアクションで指定した値だけ増加する', () => {
    const actual = counterReducer(initialState, incrementByAmount(5))
    expect(actual.value).toEqual(5)
  })

  it('複数のアクションを連続して実行できる', () => {
    let state = counterReducer(initialState, increment())
    state = counterReducer(state, increment())
    state = counterReducer(state, incrementByAmount(3))
    expect(state.value).toEqual(5)
  })

  it('負の値でincrementByAmountを実行できる', () => {
    const actual = counterReducer(initialState, incrementByAmount(-10))
    expect(actual.value).toEqual(-10)
  })
})
