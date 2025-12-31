# Next.js テストガイド

このドキュメントでは、Next.js + Vitest + React Testing Library を使用したテストの書き方について説明します。

## 目次

- [テスト環境の概要](#テスト環境の概要)
- [テストの実行方法](#テストの実行方法)
- [テストの基本](#テストの基本)
- [コンポーネントのテスト](#コンポーネントのテスト)
- [Redux Store のテスト](#redux-storeのテスト)
- [urql クライアントのテスト](#urqlクライアントのテスト)
- [非同期処理のテスト](#非同期処理のテスト)
- [モックの使い方](#モックの使い方)
- [カバレッジレポート](#カバレッジレポート)
- [ベストプラクティス](#ベストプラクティス)

## テスト環境の概要

### 使用ツール

- **Vitest**: 高速な Vite ベースのテストフレームワーク
- **React Testing Library**: React コンポーネントのテスト
- **jsdom**: ブラウザ環境のシミュレーション
- **@testing-library/jest-dom**: 便利なマッチャー
- **@testing-library/user-event**: ユーザーインタラクションのシミュレーション

### ディレクトリ構造

```
src/
├── test/
│   ├── setup.ts           # テストセットアップファイル
│   ├── example.test.ts    # サンプルテスト
│   └── testing-guide.md   # このドキュメント
├── app/
│   ├── page.test.tsx      # ページコンポーネントのテスト
│   └── graphql/
│       └── page.test.tsx  # GraphQLページのテスト
├── store/
│   └── slices/
│       └── counterSlice.test.ts  # Reduxスライスのテスト
└── lib/
    └── graphql/
        └── urqlClient.test.ts    # urqlクライアントのテスト
```

## テストの実行方法

### 基本コマンド

```bash
# すべてのテストを実行
npm run test

# ウォッチモードで実行（ファイル変更時に自動実行）
npm run test -- --watch

# UIモードで実行（ブラウザでテスト結果表示）
npm run test:ui

# カバレッジレポートを生成
npm run test:coverage
```

### Docker コンテナ内での実行

```bash
# コンテナに入る
docker-compose exec frontend sh

# テスト実行
npm run test

# カバレッジ生成
npm run test:coverage
```

### 特定のテストファイルを実行

```bash
# パターンマッチでフィルタリング
npm run test -- counterSlice

# 特定のファイルを実行
npm run test -- src/app/page.test.tsx
```

## テストの基本

### 基本的なテストの構造

```typescript
import { describe, it, expect } from 'vitest'

describe('テストスイート名', () => {
  it('テストケース名', () => {
    // Arrange: テストデータの準備
    const input = 1 + 1

    // Act: テスト対象の実行
    const result = input

    // Assert: 結果の検証
    expect(result).toBe(2)
  })
})
```

### よく使うマッチャー

```typescript
// 基本的な比較
expect(value).toBe(2) // 厳密等価 (===)
expect(value).toEqual({ name: 'test' }) // オブジェクト比較
expect(value).not.toBe(3) // 否定

// 真偽値
expect(value).toBeTruthy()
expect(value).toBeFalsy()
expect(value).toBeNull()
expect(value).toBeUndefined()
expect(value).toBeDefined()

// 数値
expect(value).toBeGreaterThan(10)
expect(value).toBeLessThan(100)
expect(value).toBeCloseTo(0.3) // 浮動小数点

// 配列・文字列
expect(array).toContain('item')
expect(array).toHaveLength(3)
expect(string).toMatch(/pattern/)
```

## コンポーネントのテスト

### 基本的なコンポーネントテスト

```typescript
import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import MyComponent from './MyComponent'

describe('MyComponent', () => {
  it('正しくレンダリングされる', () => {
    render(<MyComponent />)

    // テキストで検索
    expect(screen.getByText('Hello World')).toBeInTheDocument()

    // ロールで検索
    expect(screen.getByRole('button')).toBeInTheDocument()

    // ラベルで検索
    expect(screen.getByLabelText('Username')).toBeInTheDocument()
  })
})
```

### Props を使用したテスト

```typescript
it('Propsが正しく表示される', () => {
  render(<MyComponent title='Test Title' count={5} />)

  expect(screen.getByText('Test Title')).toBeInTheDocument()
  expect(screen.getByText('5')).toBeInTheDocument()
})
```

### ユーザーインタラクションのテスト

```typescript
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'

it('ボタンクリックで状態が変更される', async () => {
  const user = userEvent.setup()
  render(<Counter />)

  const button = screen.getByRole('button', { name: /increment/i })

  // クリック前
  expect(screen.getByText('Count: 0')).toBeInTheDocument()

  // クリック
  await user.click(button)

  // クリック後
  expect(screen.getByText('Count: 1')).toBeInTheDocument()
})
```

### フォーム入力のテスト

```typescript
it('フォーム入力が動作する', async () => {
  const user = userEvent.setup()
  render(<LoginForm />)

  const usernameInput = screen.getByLabelText('Username')
  const passwordInput = screen.getByLabelText('Password')
  const submitButton = screen.getByRole('button', { name: /submit/i })

  // 入力
  await user.type(usernameInput, 'testuser')
  await user.type(passwordInput, 'password123')
  await user.click(submitButton)

  // 検証
  expect(screen.getByText('Login Successful')).toBeInTheDocument()
})
```

## Redux Store のテスト

### スライスのテスト

```typescript
import { describe, it, expect } from 'vitest'
import counterReducer, { increment, decrement } from './counterSlice'

describe('counterSlice', () => {
  const initialState = { value: 0 }

  it('初期状態が正しく設定される', () => {
    expect(counterReducer(undefined, { type: 'unknown' })).toEqual({
      value: 0
    })
  })

  it('incrementアクションで値が増加する', () => {
    const actual = counterReducer(initialState, increment(5))
    expect(actual.value).toBe(5)
  })

  it('decrementアクションで値が減少する', () => {
    const previousState = { value: 10 }
    const actual = counterReducer(previousState, decrement())
    expect(actual.value).toBe(9)
  })
})
```

### Redux 連携コンポーネントのテスト

```typescript
import { render, screen } from '@testing-library/react'
import { Provider } from 'react-redux'
import { configureStore } from '@reduxjs/toolkit'
import counterReducer from '@/store/slices/counterSlice'

// テスト用ストアの作成
const createTestStore = (initialState = {}) => {
  return configureStore({
    reducer: {
      counter: counterReducer
    },
    preloadedState: initialState
  })
}

it('Reduxストアの値が表示される', () => {
  const store = createTestStore({
    counter: { value: 42 }
  })

  render(
    <Provider store={store}>
      <CounterDisplay />
    </Provider>
  )

  expect(screen.getByText('42')).toBeInTheDocument()
})
```

## urql クライアントのテスト

### クライアント初期化のテスト

```typescript
import { describe, it, expect } from 'vitest'
import { urqlClient } from './urqlClient'

describe('urqlClient', () => {
  it('urqlクライアントが正しく初期化される', () => {
    expect(urqlClient).toBeDefined()
  })

  it('正しいURLが設定されている', () => {
    // @ts-expect-error - urlプロパティはprivateだがテストのためアクセス
    const url = urqlClient.url
    expect(url).toBeDefined()
    expect(typeof url).toBe('string')
  })
})
```

### GraphQL クエリを使用するコンポーネントのテスト

```typescript
import { render, screen } from '@testing-library/react'
import { Provider } from 'urql'
import { fromValue } from 'wonka'

// モッククライアントの作成
const mockClient = {
  executeQuery: vi.fn(() =>
    fromValue({
      data: {
        users: [
          { id: '1', name: 'User 1' },
          { id: '2', name: 'User 2' }
        ]
      }
    })
  )
}

it('GraphQLクエリの結果が表示される', async () => {
  render(
    <Provider value={mockClient}>
      <UserList />
    </Provider>
  )

  expect(await screen.findByText('User 1')).toBeInTheDocument()
  expect(await screen.findByText('User 2')).toBeInTheDocument()
})
```

## 非同期処理のテスト

### async/await を使用したテスト

```typescript
it('非同期データの取得が成功する', async () => {
  render(<AsyncComponent />)

  // ローディング状態の確認
  expect(screen.getByText('Loading...')).toBeInTheDocument()

  // データが表示されるまで待機
  expect(await screen.findByText('Data Loaded')).toBeInTheDocument()
})
```

### waitFor を使用した待機

```typescript
import { waitFor } from '@testing-library/react'

it('状態の変更を待機する', async () => {
  const { rerender } = render(<MyComponent status='pending' />)

  rerender(<MyComponent status='success' />)

  await waitFor(() => {
    expect(screen.getByText('Success!')).toBeInTheDocument()
  })
})
```

## モックの使い方

### 関数のモック

```typescript
import { vi } from 'vitest'

it('コールバック関数が呼ばれる', async () => {
  const handleClick = vi.fn()
  const user = userEvent.setup()

  render(<Button onClick={handleClick}>Click me</Button>)

  await user.click(screen.getByRole('button'))

  expect(handleClick).toHaveBeenCalledTimes(1)
})
```

### モジュールのモック

```typescript
// Next.js Linkのモック
vi.mock('next/link', () => ({
  default: ({ children, href }: any) => <a href={href}>{children}</a>
}))

// コンポーネントのモック
vi.mock('./MyComponent', () => ({
  MyComponent: () => <div>Mocked Component</div>
}))
```

### 環境変数のモック

```typescript
import { beforeEach, afterEach } from 'vitest'

describe('環境変数を使用するテスト', () => {
  const originalEnv = process.env

  beforeEach(() => {
    process.env = {
      ...originalEnv,
      NEXT_PUBLIC_API_URL: 'https://test.api.com'
    }
  })

  afterEach(() => {
    process.env = originalEnv
  })

  it('環境変数が使用される', () => {
    expect(process.env.NEXT_PUBLIC_API_URL).toBe('https://test.api.com')
  })
})
```

## カバレッジレポート

### カバレッジの確認

```bash
# カバレッジレポートを生成
npm run test:coverage

# レポートはcoverageディレクトリに生成されます
# coverage/index.htmlをブラウザで開いて確認
```

### カバレッジの指標

- **Statements**: 実行された文の割合
- **Branches**: 実行された分岐の割合
- **Functions**: 実行された関数の割合
- **Lines**: 実行された行の割合

### カバレッジ設定のカスタマイズ

`vitest.config.ts`で設定を変更できます：

```typescript
export default defineConfig({
  test: {
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
      exclude: [
        'node_modules/',
        'src/test/',
        '**/*.d.ts',
        '**/*.config.*',
        'dist/',
        '.next/'
      ],
      // カバレッジの閾値を設定
      thresholds: {
        lines: 80,
        functions: 80,
        branches: 80,
        statements: 80
      }
    }
  }
})
```

## ベストプラクティス

### 1. テストは独立させる

```typescript
// ❌ 悪い例: テスト間で状態を共有
let sharedCounter = 0

it('テスト1', () => {
  sharedCounter++
  expect(sharedCounter).toBe(1)
})

it('テスト2', () => {
  // テスト1の影響を受ける
  expect(sharedCounter).toBe(0) // 失敗する
})

// ✅ 良い例: 各テストで初期化
it('テスト1', () => {
  let counter = 0
  counter++
  expect(counter).toBe(1)
})

it('テスト2', () => {
  let counter = 0
  expect(counter).toBe(0)
})
```

### 2. 実装の詳細ではなく、動作をテストする

```typescript
// ❌ 悪い例: 内部実装に依存
it('counterSliceのreducerが正しく動作する', () => {
  const state = { value: 0 }
  const newState = counterSlice.reducer(state, { type: 'INCREMENT' })
  expect(newState).toEqual({ value: 1 })
})

// ✅ 良い例: 公開APIを使用
it('incrementアクションで値が増加する', () => {
  const actual = counterReducer(initialState, increment(1))
  expect(actual.value).toBe(1)
})
```

### 3. わかりやすいテスト名をつける

```typescript
// ❌ 悪い例
it('works', () => { ... })
it('test1', () => { ... })

// ✅ 良い例
it('ボタンクリックでカウンターが1増加する', () => { ... })
it('無効な入力で適切なエラーメッセージが表示される', () => { ... })
```

### 4. Arrange-Act-Assert パターンを使用

```typescript
it('ユーザー登録が成功する', async () => {
  // Arrange: テストデータの準備
  const user = userEvent.setup()
  render(<RegisterForm />)

  // Act: テスト対象の実行
  await user.type(screen.getByLabelText('Email'), 'test@example.com')
  await user.type(screen.getByLabelText('Password'), 'password123')
  await user.click(screen.getByRole('button', { name: /register/i }))

  // Assert: 結果の検証
  expect(screen.getByText('Registration Successful')).toBeInTheDocument()
})
```

### 5. テストデータは明示的に定義する

```typescript
// ❌ 悪い例: マジックナンバー
it('割引計算が正しい', () => {
  expect(calculateDiscount(100, 0.1)).toBe(90)
})

// ✅ 良い例: 意味のある変数名
it('10%割引が正しく計算される', () => {
  const price = 100
  const discountRate = 0.1
  const expectedPrice = 90

  expect(calculateDiscount(price, discountRate)).toBe(expectedPrice)
})
```

### 6. エッジケースをテストする

```typescript
describe('divide関数', () => {
  it('正常な除算ができる', () => {
    expect(divide(10, 2)).toBe(5)
  })

  it('ゼロ除算でエラーをスローする', () => {
    expect(() => divide(10, 0)).toThrow('Division by zero')
  })

  it('負の数でも動作する', () => {
    expect(divide(-10, 2)).toBe(-5)
  })

  it('小数でも動作する', () => {
    expect(divide(10, 3)).toBeCloseTo(3.33, 2)
  })
})
```

### 7. 適切なクエリメソッドを使用する

```typescript
// 優先順位（推奨順）

// 1. アクセシブルなクエリ（推奨）
screen.getByRole('button', { name: /submit/i })
screen.getByLabelText('Username')
screen.getByPlaceholderText('Enter your name')
screen.getByText('Welcome')

// 2. セマンティックなクエリ
screen.getByAltText('Profile picture')
screen.getByTitle('Close')

// 3. テストID（最終手段）
screen.getByTestId('custom-element')
```

## トラブルシューティング

### テストが失敗する場合

1. **エラーメッセージを確認する**: Vitest は詳細なエラー情報を提供します
2. **screen.debug()を使用する**: 現在の DOM 状態を出力します
3. **ウォッチモードで実行する**: `--watch`オプションでリアルタイムに確認

```typescript
it('デバッグ例', () => {
  render(<MyComponent />)

  // 現在のDOMを出力
  screen.debug()

  // 特定の要素を出力
  screen.debug(screen.getByRole('button'))
})
```

### 非同期テストのタイムアウト

```typescript
it('時間のかかる処理', async () => {
  render(<SlowComponent />)

  // タイムアウトを延長
  expect(
    await screen.findByText('Loaded', {}, { timeout: 5000 })
  ).toBeInTheDocument()
}, 10000) // テスト全体のタイムアウトも延長
```

## 参考リンク

- [Vitest 公式ドキュメント](https://vitest.dev/)
- [React Testing Library 公式ドキュメント](https://testing-library.com/react)
- [Testing Library クエリガイド](https://testing-library.com/docs/queries/about)
- [Jest DOM Matchers](https://github.com/testing-library/jest-dom)

---

テストについて質問があれば、プロジェクトの issue を作成してください。
