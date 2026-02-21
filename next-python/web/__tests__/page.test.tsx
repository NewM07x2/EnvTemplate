import { render, screen } from '@testing-library/react'
import Home from '@/app/page'

describe('Home Page', () => {
  it('should render the home page', () => {
    render(<Home />)
    
    expect(screen.getByText(/Next.js \+ GraphQL \+ Prisma テンプレート/i)).toBeInTheDocument()
  })

  it('should display setup instructions', () => {
    render(<Home />)
    
    expect(screen.getByText(/セットアップ手順/i)).toBeInTheDocument()
  })
})
