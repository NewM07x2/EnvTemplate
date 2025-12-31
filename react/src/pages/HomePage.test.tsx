import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import { BrowserRouter } from 'react-router-dom'
import HomePage from './HomePage'

describe('HomePage', () => {
  it('ホームページが正しくレンダリングされる', () => {
    render(
      <BrowserRouter>
        <HomePage />
      </BrowserRouter>
    )
    
    expect(screen.getByText('React + GraphQL + Prisma テンプレート')).toBeInTheDocument()
  })

  it('主な技術スタックセクションが表示される', () => {
    render(
      <BrowserRouter>
        <HomePage />
      </BrowserRouter>
    )
    
    expect(screen.getByText('📦 主な技術スタック')).toBeInTheDocument()
    expect(screen.getByText(/React 18/)).toBeInTheDocument()
    expect(screen.getByText(/TypeScript/)).toBeInTheDocument()
    expect(screen.getByText(/Vite/)).toBeInTheDocument()
  })

  it('使い方セクションが表示される', () => {
    render(
      <BrowserRouter>
        <HomePage />
      </BrowserRouter>
    )
    
    expect(screen.getByText('🚀 使い方')).toBeInTheDocument()
    expect(screen.getByText(/GraphQL \(CSR\)/)).toBeInTheDocument()
    expect(screen.getByText(/Prisma \(SSR\)/)).toBeInTheDocument()
  })

  it('cardクラスが適用されている', () => {
    const { container } = render(
      <BrowserRouter>
        <HomePage />
      </BrowserRouter>
    )
    
    const cards = container.querySelectorAll('.card')
    expect(cards.length).toBeGreaterThan(0)
  })
})
