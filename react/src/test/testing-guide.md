# テストガイド

このドキュメントでは、React アプリケーションでのテストの書き方と実行方法について説明します。

## 🧪 テスト環境

### 使用技術

- **Vitest** - Vite 対応の高速テストフレームワーク
- **React Testing Library** - React コンポーネントのテスト
- **jsdom** - ブラウザ環境のシミュレーション
- **@testing-library/jest-dom** - カスタムマッチャー
- **@testing-library/user-event** - ユーザーインタラクションのシミュレーション

## 📝 テストの書き方

### 基本的なコンポーネントテスト

```typescript
import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import MyComponent from './MyComponent'

describe('MyComponent', () => {
  it('正しくレンダリングされる', () => {
    render(<MyComponent />)
    expect(screen.getByText('Hello')).toBeInTheDocument()
  })
})
```

### React Router を使用するコンポーネント

```typescript
import { BrowserRouter } from 'react-router-dom'

render(
  <BrowserRouter>
    <MyComponent />
  </BrowserRouter>
)
```

### Redux を使用するコンポーネント

```typescript
import { Provider } from 'react-redux'
import { store } from '@/store/store'

render(
  <Provider store={store}>
    <MyComponent />
  </Provider>
)
```

### urql (GraphQL) を使用するコンポーネント

```typescript
import { Provider } from 'urql'
import { fromValue } from 'wonka'
import { vi } from 'vitest'

const createMockClient = (data: any) => {
  return {
    executeQuery: vi.fn(() => fromValue({ data })),
    executeMutation: vi.fn(),
    executeSubscription: vi.fn()
  } as any
}

const mockClient = createMockClient({
  users: [{ id: 1, username: 'test' }]
})

render(
  <Provider value={mockClient}>
    <MyComponent />
  </Provider>
)
```

### ユーザーインタラクションのテスト

```typescript
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'

it('ボタンクリックが動作する', async () => {
  const user = userEvent.setup()
  render(<MyComponent />)

  const button = screen.getByRole('button', { name: 'クリック' })
  await user.click(button)

  expect(screen.getByText('クリックされました')).toBeInTheDocument()
})
```

### 非同期処理のテスト

```typescript
import { waitFor } from '@testing-library/react'

it('非同期データが表示される', async () => {
  render(<MyComponent />)

  await waitFor(() => {
    expect(screen.getByText('データ読み込み完了')).toBeInTheDocument()
  })
})
```

## 🚀 テストコマンド

### 基本コマンド

```bash
# すべてのテストを実行
npm run test

# ウォッチモードで実行（変更を監視）
npm run test -- --watch

# 特定のファイルのみテスト
npm run test src/components/MyComponent.test.tsx

# UIモードで実行（ブラウザでテスト結果を表示）
npm run test:ui

# カバレッジレポートを生成
npm run test:coverage
```

### Docker コンテナ内でテスト実行

```bash
# コンテナに入る
docker-compose exec frontend sh

# テスト実行
npm run test

# カバレッジ生成
npm run test:coverage
```

## 📊 カバレッジ

カバレッジレポートは `coverage/` ディレクトリに生成されます。

```bash
# カバレッジ生成
npm run test:coverage

# HTMLレポートを確認
# coverage/index.html をブラウザで開く
```

### カバレッジの除外設定

`vite.config.ts` で以下を除外しています:

- `node_modules/`
- `src/test/`
- `**/*.d.ts`
- `**/*.config.*`
- `**/mockData`

## 🎯 テストの種類

### 1. コンポーネントテスト

UI コンポーネントが正しくレンダリングされるかをテスト

```typescript
// src/components/Button.test.tsx
describe('Button', () => {
  it('ラベルが表示される', () => {
    render(<Button label='送信' />)
    expect(screen.getByText('送信')).toBeInTheDocument()
  })
})
```

### 2. 統合テスト

複数のコンポーネントが連携して動作するかをテスト

```typescript
// src/pages/HomePage.test.tsx
describe('HomePage', () => {
  it('ページ全体が正しく表示される', () => {
    render(<HomePage />)
    expect(screen.getByText('ホーム')).toBeInTheDocument()
  })
})
```

### 3. ロジックテスト

Redux slice やユーティリティ関数のテスト

```typescript
// src/store/slices/counterSlice.test.ts
describe('counterSlice', () => {
  it('incrementで値が増加する', () => {
    const state = counterReducer(initialState, increment())
    expect(state.value).toBe(1)
  })
})
```

## 🔍 テストのベストプラクティス

### 1. テストの構造

```typescript
describe('コンポーネント名/機能名', () => {
  it('何をテストするかを明確に記述', () => {
    // Arrange (準備)
    const props = { ... }

    // Act (実行)
    render(<MyComponent {...props} />)

    // Assert (検証)
    expect(screen.getByText('...')).toBeInTheDocument()
  })
})
```

### 2. 適切なクエリの使用

優先順位（上から順に推奨）:

1. `getByRole` - アクセシビリティ重視
2. `getByLabelText` - フォーム要素
3. `getByPlaceholderText` - 入力フィールド
4. `getByText` - テキストコンテンツ
5. `getByTestId` - 最後の手段

```typescript
// 推奨
screen.getByRole('button', { name: '送信' })

// 避けるべき
screen.getByTestId('submit-button')
```

### 3. テストの独立性

各テストは他のテストに依存せず、独立して実行できるようにする

```typescript
describe('Counter', () => {
  it('初期値は0', () => {
    // このテストは他のテストに影響されない
  })

  it('incrementで1増加', () => {
    // このテストも独立している
  })
})
```

### 4. 意味のあるテスト名

```typescript
// ❌ 悪い例
it('test1', () => { ... })

// ✅ 良い例
it('ユーザー名が空の場合にエラーメッセージが表示される', () => { ... })
```

## 🐛 トラブルシューティング

### テストが失敗する場合

```bash
# キャッシュをクリア
npm run test -- --clearCache

# node_modulesを再インストール
rm -rf node_modules
npm install
```

### 特定のテストをスキップ

```typescript
// テストをスキップ
it.skip('このテストはスキップされる', () => {
  // ...
})

// 特定のテストのみ実行
it.only('このテストのみ実行される', () => {
  // ...
})
```

### デバッグ

```typescript
import { screen, debug } from '@testing-library/react'

it('デバッグ例', () => {
  render(<MyComponent />)

  // 現在のDOMツリーを出力
  screen.debug()

  // 特定の要素を出力
  const element = screen.getByText('Hello')
  debug(element)
})
```

## 📚 参考リンク

- [Vitest 公式ドキュメント](https://vitest.dev/)
- [React Testing Library 公式ドキュメント](https://testing-library.com/docs/react-testing-library/intro/)
- [Testing Library クエリ優先順位](https://testing-library.com/docs/queries/about/#priority)
- [Common mistakes with React Testing Library](https://kentcdodds.com/blog/common-mistakes-with-react-testing-library)

## 💡 テストの例

プロジェクト内には以下のテストファイルが含まれています:

- `src/App.test.tsx` - メインアプリケーションのテスト
- `src/pages/HomePage.test.tsx` - ホームページのテスト
- `src/pages/GraphQLPage.test.tsx` - GraphQL ページのテスト
- `src/pages/PrismaPage.test.tsx` - Prisma ページのテスト
- `src/store/slices/counterSlice.test.ts` - Redux slice のテスト
- `src/lib/graphql/urqlClient.test.ts` - urql クライアントのテスト

これらを参考に、新しいテストを追加してください。
