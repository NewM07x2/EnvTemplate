# Jest テストガイド

このプロジェクトでは Jest と React Testing Library を使用してテストを実施します。

## セットアップ

### 1. 依存関係のインストール

```bash
npm install
```

以下のパッケージがインストールされます：
- `jest` - テストフレームワーク
- `@testing-library/react` - React コンポーネントテストライブラリ
- `@testing-library/jest-dom` - Jest マッチャーの拡張
- `@testing-library/user-event` - ユーザーイベントのシミュレーション
- `jest-environment-jsdom` - DOM 環境でのテスト実行

### 2. テスト実行

```bash
# すべてのテストを実行
npm test

# ファイルの変更を監視してテストを実行
npm run test:watch

# カバレッジレポートを生成
npm run test:coverage
```

## テストファイル配置

テストファイルは `__tests__` ディレクトリに配置します：

```
__tests__/
├── page.test.tsx              # ページコンポーネントのテスト
├── components.test.example.tsx # コンポーネントテストのテンプレート
├── api.test.example.ts        # API テストのテンプレート
└── hooks/
    └── useExample.test.ts     # カスタムフックのテスト
```

## テスト記述ガイド

### 1. コンポーネントテスト

```typescript
import { render, screen } from '@testing-library/react'
import MyComponent from '@/components/MyComponent'

describe('MyComponent', () => {
  it('should render correctly', () => {
    render(<MyComponent />)
    expect(screen.getByText(/hello/i)).toBeInTheDocument()
  })

  it('should handle click events', async () => {
    render(<MyComponent />)
    const button = screen.getByRole('button', { name: /click/i })
    await userEvent.click(button)
    expect(screen.getByText(/clicked/i)).toBeInTheDocument()
  })
})
```

### 2. ユーザーイベント（v14 推奨）

```typescript
import userEvent from '@testing-library/user-event'

it('should handle input', async () => {
  const user = userEvent.setup()
  render(<MyComponent />)
  
  const input = screen.getByRole('textbox')
  await user.type(input, 'test text')
  
  expect(input).toHaveValue('test text')
})
```

### 3. Redux を使用するコンポーネント

```typescript
import { render, screen } from '@testing-library/react'
import { Provider } from 'react-redux'
import { configureStore } from '@reduxjs/toolkit'
import MyComponent from '@/components/MyComponent'
import counterSlice from '@/store/slices/counterSlice'

it('should render with Redux store', () => {
  const store = configureStore({
    reducer: {
      counter: counterSlice,
    },
  })

  render(
    <Provider store={store}>
      <MyComponent />
    </Provider>
  )

  expect(screen.getByText(/count/i)).toBeInTheDocument()
})
```

### 4. カスタムフック

```typescript
import { renderHook, act } from '@testing-library/react'
import { useCounter } from '@/hooks/useCounter'

it('should increment counter', () => {
  const { result } = renderHook(() => useCounter())

  act(() => {
    result.current.increment()
  })

  expect(result.current.count).toBe(1)
})
```

### 5. GraphQL クエリのモック

```typescript
import { render, screen } from '@testing-library/react'
import { createClient, gql } from 'urql'
import { mockDeep, mockResolvedValue } from 'jest-mock-extended'
import MyComponent from '@/components/MyComponent'

it('should render GraphQL data', async () => {
  const mockClient = mockDeep()
  mockClient.query.mockResolvedValue({
    data: { users: [{ id: 1, name: 'Test' }] },
  })

  // GraphQL クライアントのモックをセット
  render(<MyComponent />)

  expect(await screen.findByText('Test')).toBeInTheDocument()
})
```

## よく使う React Testing Library メソッド

### クエリ

```typescript
// 単一要素を取得（見つからない場合はエラー）
screen.getByRole('button', { name: /click/i })
screen.getByText('Hello')
screen.getByPlaceholderText('Enter name')
screen.getByLabelText('Username')
screen.getByTestId('submit-button')

// 複数要素を取得
screen.getAllByRole('listitem')

// 見つからない場合は null を返す
screen.queryByText('Not found')

// 非同期で待機
await screen.findByText('Loaded')
```

### アサーション

```typescript
// DOM 内に存在
expect(element).toBeInTheDocument()

// 表示状態
expect(element).toBeVisible()
expect(element).toBeHidden()

// 属性
expect(button).toHaveAttribute('disabled')
expect(input).toHaveValue('text')
expect(link).toHaveClass('active')

// テキスト
expect(element).toHaveTextContent('Hello')
expect(element).toHaveDisplayValue('value')

// 関数呼び出し
expect(mockFn).toHaveBeenCalled()
expect(mockFn).toHaveBeenCalledWith('arg')
expect(mockFn).toHaveBeenCalledTimes(1)
```

## テストコード例

### 例 1: 単純なコンポーネント

```typescript
// src/components/Button.test.tsx
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import Button from '@/components/Button'

describe('Button Component', () => {
  it('renders button with label', () => {
    render(<Button>Click me</Button>)
    expect(screen.getByRole('button', { name: /click me/i })).toBeInTheDocument()
  })

  it('calls onClick handler when clicked', async () => {
    const mockClick = jest.fn()
    render(<Button onClick={mockClick}>Click me</Button>)

    await userEvent.click(screen.getByRole('button'))
    expect(mockClick).toHaveBeenCalledTimes(1)
  })

  it('is disabled when disabled prop is true', () => {
    render(<Button disabled>Click me</Button>)
    expect(screen.getByRole('button')).toBeDisabled()
  })
})
```

### 例 2: Redux を使用するコンポーネント

```typescript
// src/components/Counter.test.tsx
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { Provider } from 'react-redux'
import { configureStore } from '@reduxjs/toolkit'
import Counter from '@/components/Counter'
import counterSlice from '@/store/slices/counterSlice'

const createTestStore = () =>
  configureStore({
    reducer: { counter: counterSlice },
  })

describe('Counter Component', () => {
  it('displays initial count', () => {
    const store = createTestStore()
    render(
      <Provider store={store}>
        <Counter />
      </Provider>
    )
    expect(screen.getByText(/count: 0/i)).toBeInTheDocument()
  })

  it('increments count when button is clicked', async () => {
    const user = userEvent.setup()
    const store = createTestStore()
    
    render(
      <Provider store={store}>
        <Counter />
      </Provider>
    )

    const incrementBtn = screen.getByRole('button', { name: /increment/i })
    await user.click(incrementBtn)

    expect(screen.getByText(/count: 1/i)).toBeInTheDocument()
  })
})
```

## モックファイル

### API モック

```typescript
// __mocks__/api.ts
export const mockFetch = jest.fn()

global.fetch = mockFetch

export const setupFetchMock = (data: any, status = 200) => {
  mockFetch.mockResolvedValueOnce({
    ok: status >= 200 && status < 300,
    status,
    json: jest.fn().mockResolvedValueOnce(data),
  })
}
```

### GraphQL モック

```typescript
// __mocks__/graphql.ts
import { createClient } from 'urql'

export const mockGraphQLClient = createClient({
  url: 'http://localhost:8000/graphql',
})

export const mockQuery = jest.fn()
```

## ベストプラクティス

1. **ユーザー視点でテスト** - 実装ではなくユーザーの行動に基づいてテストを書く
2. **意味のあるテスト名** - テストが何をテストしているかが明確であること
3. **DRY 原則** - 共通の setUp をファクトリ関数で実装
4. **Mock を適切に使用** - 外部依存は必ずモック化
5. **カバレッジ目標** - 最低 80% を目指す

## トラブルシューティング

### モジュールが見つからないエラー

```javascript
// jest.config.js の moduleNameMapper を確認
moduleNameMapper: {
  '^@/(.*)$': '<rootDir>/src/$1',
}
```

### Next.js コンポーネントがレンダリングできない

```typescript
// jest.setup.js で Next.js モジュールをモック
jest.mock('next/router', () => ({
  useRouter: () => ({
    pathname: '/',
    query: {},
  }),
}))
```

### Redux がエラーになる

```typescript
// テストコンポーネントを Provider でラップ
render(
  <Provider store={store}>
    <Component />
  </Provider>
)
```

## 参考リンク

- [Jest ドキュメント](https://jestjs.io/)
- [React Testing Library](https://testing-library.com/react)
- [Testing Library でのベストプラクティス](https://testing-library.com/docs/queries/about)
- [Next.js テスト](https://nextjs.org/docs/testing)
