import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import Home from './page'

// コンポーネントのモック
vi.mock('../components/sample/List', () => ({
  List: () => <div>List Component</div>,
}))

vi.mock('../components/sample/Title', () => ({
  Title: () => <div>Title Component</div>,
}))

vi.mock('../components/sample/Count', () => ({
  Count: ({ title }: { title: string }) => <div>Count {title}</div>,
}))

vi.mock('../components/sample/Event', () => ({
  Event: () => <div>Event Component</div>,
}))

vi.mock('../components/sample/Array', () => ({
  Array: () => <div>Array Component</div>,
}))

describe('Home Page', () => {
  it('ホームページが正しくレンダリングされる', () => {
    render(<Home />)
    expect(screen.getByText(/Count A/i)).toBeInTheDocument()
  })

  it('toggleボタンが存在する', () => {
    render(<Home />)
    const toggleButton = screen.getByRole('button', { name: /toggle/i })
    expect(toggleButton).toBeInTheDocument()
  })
})
