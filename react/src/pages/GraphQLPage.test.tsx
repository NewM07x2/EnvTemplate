import { describe, it, expect, vi } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import { Provider } from 'urql'
import { BrowserRouter } from 'react-router-dom'
import { fromValue, never } from 'wonka'
import GraphQLPage from './GraphQLPage'

// urqlのモッククライアント作成ヘルパー
const createMockClient = (executeQueryResult: any) => {
  return {
    executeQuery: vi.fn(() => executeQueryResult),
    executeMutation: vi.fn(),
    executeSubscription: vi.fn(),
  } as any
}

describe('GraphQLPage', () => {
  it('読み込み中の状態が表示される', () => {
    const mockClient = createMockClient(never)
    
    render(
      <BrowserRouter>
        <Provider value={mockClient}>
          <GraphQLPage />
        </Provider>
      </BrowserRouter>
    )
    
    expect(screen.getByText('読み込み中...')).toBeInTheDocument()
  })

  it('エラーが正しく表示される', async () => {
    const mockClient = createMockClient(
      fromValue({
        error: new Error('GraphQL Error'),
      })
    )
    
    render(
      <BrowserRouter>
        <Provider value={mockClient}>
          <GraphQLPage />
        </Provider>
      </BrowserRouter>
    )
    
    await waitFor(() => {
      expect(screen.getByText(/エラー:/)).toBeInTheDocument()
    })
  })

  it('ユーザーデータが正しく表示される', async () => {
    const mockClient = createMockClient(
      fromValue({
        data: {
          users: [
            { id: 1, username: 'testuser1', email: 'test1@example.com' },
            { id: 2, username: 'testuser2', email: 'test2@example.com' },
          ],
        },
      })
    )
    
    render(
      <BrowserRouter>
        <Provider value={mockClient}>
          <GraphQLPage />
        </Provider>
      </BrowserRouter>
    )
    
    await waitFor(() => {
      expect(screen.getByText('testuser1')).toBeInTheDocument()
      expect(screen.getByText('testuser2')).toBeInTheDocument()
    })
  })

  it('データがない場合のメッセージが表示される', async () => {
    const mockClient = createMockClient(
      fromValue({
        data: {
          users: [],
        },
      })
    )
    
    render(
      <BrowserRouter>
        <Provider value={mockClient}>
          <GraphQLPage />
        </Provider>
      </BrowserRouter>
    )
    
    await waitFor(() => {
      expect(screen.getByText('データがありません')).toBeInTheDocument()
    })
  })

  it('ページタイトルが正しく表示される', async () => {
    const mockClient = createMockClient(
      fromValue({
        data: {
          users: [],
        },
      })
    )
    
    render(
      <BrowserRouter>
        <Provider value={mockClient}>
          <GraphQLPage />
        </Provider>
      </BrowserRouter>
    )
    
    await waitFor(() => {
      expect(screen.getByText('GraphQL (CSR) - urql')).toBeInTheDocument()
    })
  })
})
