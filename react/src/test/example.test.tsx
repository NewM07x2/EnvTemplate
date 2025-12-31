import { describe, it, expect, beforeEach } from 'vitest'
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'

/**
 * 基本的なコンポーネントテストのサンプル
 */

// サンプルコンポーネント
function Button({ onClick, children }: { onClick: () => void; children: React.ReactNode }) {
  return <button onClick={onClick}>{children}</button>
}

describe('サンプルテスト - Button', () => {
  it('ボタンが正しくレンダリングされる', () => {
    render(<Button onClick={() => {}}>クリック</Button>)
    expect(screen.getByRole('button', { name: 'クリック' })).toBeInTheDocument()
  })

  it('クリックイベントが正しく発火する', async () => {
    const user = userEvent.setup()
    let clicked = false
    const handleClick = () => {
      clicked = true
    }

    render(<Button onClick={handleClick}>クリック</Button>)
    
    await user.click(screen.getByRole('button'))
    expect(clicked).toBe(true)
  })
})

/**
 * 複数のテストケースをまとめる例
 */
describe('算術演算のテスト', () => {
  it('足し算が正しく動作する', () => {
    expect(1 + 1).toBe(2)
    expect(5 + 3).toBe(8)
  })

  it('引き算が正しく動作する', () => {
    expect(5 - 3).toBe(2)
    expect(10 - 1).toBe(9)
  })

  it('掛け算が正しく動作する', () => {
    expect(3 * 4).toBe(12)
    expect(7 * 8).toBe(56)
  })
})

/**
 * beforeEachを使用したテストのセットアップ例
 */
describe('テストのセットアップ例', () => {
  let testValue: number

  beforeEach(() => {
    // 各テストの前に実行される
    testValue = 0
  })

  it('初期値は0', () => {
    expect(testValue).toBe(0)
  })

  it('値を変更できる', () => {
    testValue = 10
    expect(testValue).toBe(10)
  })

  it('各テストは独立している', () => {
    // beforeEachで初期化されるため、前のテストの影響を受けない
    expect(testValue).toBe(0)
  })
})
