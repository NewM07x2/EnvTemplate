import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import { BrowserRouter } from 'react-router-dom'
import App from '../App'

describe('App', () => {
  it('アプリケーションが正しくレンダリングされる', () => {
    render(
      <BrowserRouter>
        <App />
      </BrowserRouter>
    )
    
    // ナビゲーションリンクが存在することを確認
    expect(screen.getByText('ホーム')).toBeInTheDocument()
    expect(screen.getByText('GraphQL (CSR)')).toBeInTheDocument()
    expect(screen.getByText('Prisma (SSR)')).toBeInTheDocument()
  })

  it('ナビゲーションリンクが正しく表示される', () => {
    render(
      <BrowserRouter>
        <App />
      </BrowserRouter>
    )
    
    const links = screen.getAllByRole('link')
    expect(links).toHaveLength(3)
  })
})
