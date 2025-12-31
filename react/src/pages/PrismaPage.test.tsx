import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import { BrowserRouter } from 'react-router-dom'
import PrismaPage from './PrismaPage'

describe('PrismaPage', () => {
  it('ページタイトルが正しく表示される', () => {
    render(
      <BrowserRouter>
        <PrismaPage />
      </BrowserRouter>
    )
    
    expect(screen.getByText('Prisma (SSR相当) - API経由')).toBeInTheDocument()
  })

  it('Prismaの説明が表示される', () => {
    render(
      <BrowserRouter>
        <PrismaPage />
      </BrowserRouter>
    )
    
    expect(screen.getByText('🗄️ Prismaを使用したデータ取得')).toBeInTheDocument()
    expect(screen.getByText(/バックエンドAPI経由/)).toBeInTheDocument()
  })

  it('注意セクションが表示される', () => {
    render(
      <BrowserRouter>
        <PrismaPage />
      </BrowserRouter>
    )
    
    expect(screen.getByText('📝 注意')).toBeInTheDocument()
    expect(screen.getByText(/Next\.js/)).toBeInTheDocument()
  })

  it('コード例セクションが表示される', () => {
    render(
      <BrowserRouter>
        <PrismaPage />
      </BrowserRouter>
    )
    
    expect(screen.getByText('💻 コード例')).toBeInTheDocument()
  })
})
