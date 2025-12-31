import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import Counter from './Counter'

describe('Counter', () => {
  it('初期値0で表示される', () => {
    render(<Counter />)
    expect(screen.getByText('0')).toBeInTheDocument()
  })

  it('ボタンが3つ存在する', () => {
    render(<Counter />)
    expect(screen.getByText('-1')).toBeInTheDocument()
    expect(screen.getByText('リセット')).toBeInTheDocument()
    expect(screen.getByText('+1')).toBeInTheDocument()
  })
})
