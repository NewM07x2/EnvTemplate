# テスト入門ガイド（Vitest / Jest）

> **対象者**: フロントエンド・バックエンドのテストを始めたい開発者  
> **関連テンプレート**: 全テンプレート（各テンプレートに `vitest.config.ts` または `jest.config.js` が含まれる）  
> **所要時間**: 約 50 分

---

## 📚 目次

1. [テストの種類と目的](#1-テストの種類と目的)
2. [Vitest の基本（Next.js / Nuxt / Remix / SvelteKit）](#2-vitest-の基本nextjs--nuxt--remix--sveltekit)
3. [React コンポーネントのテスト](#3-react-コンポーネントのテスト)
4. [API / ユーティリティ関数のテスト](#4-api--ユーティリティ関数のテスト)
5. [モック（Mock）の使い方](#5-モックmockの使い方)
6. [Jest の基本（React Native）](#6-jest-の基本react-native)
7. [カバレッジの確認](#7-カバレッジの確認)
8. [GitHub Actions との連携](#8-github-actions-との連携)

---

## 1. テストの種類と目的

```
テストピラミッド:

           △  E2E テスト（少数・重要フロー）
          △△△  結合テスト（モジュール間の連携）
        △△△△△  単体テスト（関数・コンポーネント単体）← 最多
```

| 種類 | 対象 | ツール |
|------|------|--------|
| **単体テスト** | 関数・コンポーネント | Vitest / Jest |
| **結合テスト** | API エンドポイント・DB | Vitest + msw |
| **E2E テスト** | ブラウザでの一連の操作 | Playwright / Cypress |

---

## 2. Vitest の基本（Next.js / Nuxt / Remix / SvelteKit）

### セットアップの確認

```bash
# テストを実行
npm run test

# ウォッチモード（ファイル保存のたびに再実行）
npm run test -- --watch

# カバレッジ付きで実行
npm run test -- --coverage
```

### 基本的なテストの書き方

```typescript
// src/lib/utils.test.ts
import { describe, it, expect, beforeEach, afterEach } from 'vitest'
import { formatDate, calculateTotal } from '@/lib/utils'

// describe: テストのグループ化
describe('formatDate', () => {
  // it / test: 個別のテストケース
  it('日付を YYYY/MM/DD 形式にフォーマットする', () => {
    const date = new Date('2024-01-15')
    expect(formatDate(date)).toBe('2024/01/15')
  })

  it('無効な日付には空文字を返す', () => {
    expect(formatDate(null)).toBe('')
  })
})

describe('calculateTotal', () => {
  it('税込み合計を計算する', () => {
    const items = [{ price: 100 }, { price: 200 }]
    expect(calculateTotal(items, 0.1)).toBe(330)  // (100 + 200) * 1.1 = 330
  })

  it('空の配列の場合は 0 を返す', () => {
    expect(calculateTotal([], 0.1)).toBe(0)
  })
})
```

### よく使うマッチャー

```typescript
// 等値チェック
expect(value).toBe(42)             // 完全一致（プリミティブ型）
expect(obj).toEqual({ id: 1 })     // 深い等値チェック（オブジェクト）

// 真偽
expect(value).toBeTruthy()
expect(value).toBeFalsy()
expect(value).toBeNull()
expect(value).toBeUndefined()

// 数値
expect(value).toBeGreaterThan(0)
expect(value).toBeGreaterThanOrEqual(0)
expect(value).toBeLessThan(100)
expect(value).toBeCloseTo(0.3, 5)  // 浮動小数点の比較

// 文字列
expect(str).toContain('hello')
expect(str).toMatch(/pattern/)
expect(str).toHaveLength(5)

// 配列
expect(arr).toContain('item')
expect(arr).toHaveLength(3)
expect(arr).toEqual(expect.arrayContaining(['a', 'b']))

// エラー
expect(() => throwingFn()).toThrow()
expect(() => throwingFn()).toThrow('Error message')

// 非同期
await expect(asyncFn()).resolves.toBe('result')
await expect(asyncFn()).rejects.toThrow('Error')
```

---

## 3. React コンポーネントのテスト

### セットアップ（Next.js テンプレートの場合）

```typescript
// src/test/setup.ts
import '@testing-library/jest-dom'  // カスタムマッチャー追加
```

### コンポーネントのレンダリングテスト

```typescript
// src/components/Button.test.tsx
import { render, screen, fireEvent } from '@testing-library/react'
import { describe, it, expect, vi } from 'vitest'
import { Button } from '@/components/Button'

describe('Button', () => {
  it('テキストが正しく表示される', () => {
    render(<Button>送信</Button>)
    
    // テキストで要素を取得
    expect(screen.getByText('送信')).toBeInTheDocument()
  })

  it('クリック時にコールバックが呼ばれる', () => {
    const handleClick = vi.fn()  // モック関数
    render(<Button onClick={handleClick}>送信</Button>)
    
    fireEvent.click(screen.getByText('送信'))
    
    expect(handleClick).toHaveBeenCalledTimes(1)
  })

  it('disabled の場合はクリックできない', () => {
    const handleClick = vi.fn()
    render(<Button disabled onClick={handleClick}>送信</Button>)
    
    fireEvent.click(screen.getByText('送信'))
    
    expect(handleClick).not.toHaveBeenCalled()
    expect(screen.getByText('送信')).toBeDisabled()
  })
})
```

### フォームのテスト

```typescript
// src/components/LoginForm.test.tsx
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'

describe('LoginForm', () => {
  it('フォーム送信でログイン関数が呼ばれる', async () => {
    const user = userEvent.setup()
    const mockLogin = vi.fn().mockResolvedValue({ success: true })
    
    render(<LoginForm onLogin={mockLogin} />)
    
    // 入力
    await user.type(screen.getByLabelText('メールアドレス'), 'alice@example.com')
    await user.type(screen.getByLabelText('パスワード'), 'password123')
    
    // 送信
    await user.click(screen.getByRole('button', { name: 'ログイン' }))
    
    await waitFor(() => {
      expect(mockLogin).toHaveBeenCalledWith({
        email: 'alice@example.com',
        password: 'password123',
      })
    })
  })

  it('メールアドレスが未入力の場合にエラーを表示する', async () => {
    const user = userEvent.setup()
    render(<LoginForm onLogin={vi.fn()} />)
    
    await user.click(screen.getByRole('button', { name: 'ログイン' }))
    
    expect(screen.getByText('メールアドレスは必須です')).toBeInTheDocument()
  })
})
```

### 要素の取得方法

```typescript
// 推奨順（アクセシビリティを意識した順）
screen.getByRole('button', { name: '送信' })       // WAI-ARIA ロール（最推奨）
screen.getByLabelText('メールアドレス')              // label に紐づく input
screen.getByPlaceholderText('入力してください')      // placeholder
screen.getByText('テキスト')                        // テキスト内容
screen.getByTestId('submit-button')                // data-testid（最終手段）

// 存在確認（なければ null を返す）
screen.queryByText('エラー')

// 非同期で現れる要素を待つ
await screen.findByText('ロード完了')
```

---

## 4. API / ユーティリティ関数のテスト

### 純粋な関数のテスト

```typescript
// src/lib/validators.test.ts
import { isValidEmail, isValidPassword } from '@/lib/validators'

describe('isValidEmail', () => {
  it.each([
    ['alice@example.com', true],
    ['user@domain.co.jp', true],
    ['invalid-email', false],
    ['', false],
    ['@example.com', false],
  ])('"%s" → %s', (email, expected) => {
    expect(isValidEmail(email)).toBe(expected)
  })
})
```

### 非同期関数のテスト

```typescript
// src/lib/api.test.ts
import { describe, it, expect, vi, beforeEach } from 'vitest'
import { fetchUser } from '@/lib/api'

// fetch をモック
global.fetch = vi.fn()

describe('fetchUser', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('正常なレスポンスをパースして返す', async () => {
    const mockUser = { id: '1', name: 'Alice' }
    vi.mocked(fetch).mockResolvedValue({
      ok: true,
      json: async () => mockUser,
    } as Response)

    const user = await fetchUser('1')
    expect(user).toEqual(mockUser)
    expect(fetch).toHaveBeenCalledWith('/api/users/1')
  })

  it('404 の場合は null を返す', async () => {
    vi.mocked(fetch).mockResolvedValue({
      ok: false,
      status: 404,
    } as Response)

    const user = await fetchUser('999')
    expect(user).toBeNull()
  })
})
```

---

## 5. モック（Mock）の使い方

### 関数のモック

```typescript
import { vi } from 'vitest'

// モック関数を作成
const mockFn = vi.fn()

// 戻り値を設定
mockFn.mockReturnValue(42)
mockFn.mockResolvedValue({ data: 'result' })  // 非同期

// 呼び出し確認
expect(mockFn).toHaveBeenCalled()
expect(mockFn).toHaveBeenCalledTimes(2)
expect(mockFn).toHaveBeenCalledWith('arg1', 'arg2')
expect(mockFn).toHaveBeenLastCalledWith('last-arg')

// モックをリセット
vi.clearAllMocks()   // 呼び出し履歴のみリセット
vi.resetAllMocks()   // 戻り値設定もリセット
```

### モジュールのモック

```typescript
// モジュール全体をモック
vi.mock('@/lib/supabase/client', () => ({
  createClient: vi.fn(() => ({
    from: vi.fn(() => ({
      select: vi.fn().mockResolvedValue({ data: [], error: null }),
      insert: vi.fn().mockResolvedValue({ data: null, error: null }),
    })),
  })),
}))

// 特定の関数だけモック
vi.mock('@/lib/auth', async (importOriginal) => {
  const original = await importOriginal()
  return {
    ...original,
    getCurrentUser: vi.fn().mockResolvedValue({ id: 'user-1', email: 'test@example.com' }),
  }
})
```

---

## 6. Jest の基本（React Native）

### セットアップ

```bash
cd react-native

# テストを実行
npm test

# カバレッジ付き
npm test -- --coverage
```

### React Native コンポーネントのテスト

```typescript
// __tests__/HomeScreen.test.tsx
import React from 'react'
import { render, screen, fireEvent } from '@testing-library/react-native'
import { HomeScreen } from '@/app/HomeScreen'

describe('HomeScreen', () => {
  it('タイトルが表示される', () => {
    render(<HomeScreen />)
    expect(screen.getByText('ホーム')).toBeTruthy()
  })

  it('ボタンタップでナビゲーションが呼ばれる', () => {
    const mockNavigation = { navigate: jest.fn() }
    render(<HomeScreen navigation={mockNavigation} />)
    
    fireEvent.press(screen.getByText('詳細へ'))
    expect(mockNavigation.navigate).toHaveBeenCalledWith('Detail')
  })
})
```

---

## 7. カバレッジの確認

```bash
# カバレッジレポートを生成
npm run test -- --coverage

# HTML レポートをブラウザで確認
# → coverage/index.html
```

### カバレッジの目安

| カバレッジ | 評価 |
|-----------|------|
| 80% 以上 | 良好 ✅ |
| 60〜80% | 改善の余地あり |
| 60% 未満 | テストが不足している |

> **注意**: カバレッジが高くてもテストの品質が低い場合があります。  
> 「正常系」だけでなく「異常系」「エッジケース」もテストすることが重要です。

---

## 8. GitHub Actions との連携

```yaml
# .github/workflows/test.yml
name: Test

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - run: npm ci

      - name: 型チェック
        run: npx tsc --noEmit

      - name: テスト（カバレッジ付き）
        run: npm run test -- --coverage

      # カバレッジが閾値を下回ったらエラー
      - name: カバレッジチェック
        run: npm run test -- --coverage --coverage.thresholds.lines=80
```

---

## 📌 まとめ

### テストの命名規則

```typescript
// 「〇〇 のとき ×× する」という形式が読みやすい
it('ユーザーが存在しないとき 404 を返す', ...)
it('メールアドレスが空のとき エラーメッセージを表示する', ...)
it('ログイン成功のとき ホームにリダイレクトする', ...)
```

### 最低限テストすべきもの

| 優先度 | テスト対象 |
|--------|---------|
| 🔴 最高 | ビジネスロジック（計算・バリデーション） |
| 🟠 高い | API エンドポイント・データ変換 |
| 🟡 中 | UI コンポーネントの動作（クリック・入力） |
| 🟢 低い | UI の見た目（スナップショット） |

```bash
# よく使うコマンド
npm run test               # テスト実行
npm run test -- --watch    # ウォッチモード
npm run test -- --coverage # カバレッジ付き
npm run test -- Button     # 特定ファイルのみ
```
