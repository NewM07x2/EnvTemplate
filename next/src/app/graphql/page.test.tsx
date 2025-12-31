import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import GraphqlPage from './page'

// Next.js Linkのモック
vi.mock('next/link', () => ({
  default: ({ children, href }: { children: React.ReactNode; href: string }) => (
    <a href={href}>{children}</a>
  ),
}))

describe('GraphQL Page', () => {
  it('ページタイトルが正しく表示される', () => {
    render(<GraphqlPage />)
    expect(screen.getByText(/GraphQL サンプルページ \(CSR\)/i)).toBeInTheDocument()
  })

  it('説明文が表示される', () => {
    render(<GraphqlPage />)
    expect(
      screen.getByText(/このページはクライアントサイドレンダリング\(CSR\)でGraphQLを使用する例です/i)
    ).toBeInTheDocument()
  })

  it('urql使用例のコードが表示される', () => {
    render(<GraphqlPage />)
    expect(screen.getByText(/urql使用例:/i)).toBeInTheDocument()
  })

  it('REST APIサンプルへのリンクが存在する', () => {
    render(<GraphqlPage />)
    const link = screen.getByRole('link', { name: /REST API サンプルへ/i })
    expect(link).toBeInTheDocument()
    expect(link).toHaveAttribute('href', '/graphql/get-api')
  })
})
