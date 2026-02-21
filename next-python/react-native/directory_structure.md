# React Native ディレクトリ構造

```
react-native/
├── app/                           # Expo Routerアプリディレクトリ (ファイルベースルーティング)
│   ├── _layout.tsx                # ルートレイアウト (全画面で共通)
│   │                              # - Reduxプロバイダー設定
│   │                              # - グローバルスタイル・テーマ
│   │
│   └── (app)/                     # アプリグループ (認証後画面)
│       ├── index.tsx              # Stackナビゲーション設定
│       │
│       └── (tabs)/                # タブナビゲーショングループ
│           ├── _layout.tsx        # タブレイアウト定義
│           │                      # - 4つのタブ: ホーム、カウンター、ユーザー、設定
│           │                      # - タブアイコン・ラベル設定
│           │
│           ├── index.tsx          # ホーム画面 (/)
│           │                      # - アプリ紹介
│           │                      # - 技術スタック表示
│           │                      # - 機能一覧
│           │
│           ├── counter.tsx        # カウンター画面 (/counter)
│           │                      # - Redux Toolkit状態管理デモ
│           │                      # - increment/decrement/reset
│           │
│           ├── users.tsx          # ユーザー一覧画面 (/users)
│           │                      # - FlatList 使用
│           │                      # - API連携 (Axios)
│           │                      # - Pull-to-Refresh
│           │                      # - ローディング・エラー処理
│           │
│           └── settings.tsx       # 設定画面 (/settings)
│                                  # - アプリ情報表示
│                                  # - バージョン情報
│                                  # - 技術スタック一覧
│
├── store/                         # Redux Toolkit状態管理
│   ├── store.ts                   # ストア設定
│   │                              # - counterReducer
│   │                              # - userReducer
│   │                              # - RootState/AppDispatch型エクスポート
│   │
│   └── slices/                    # スライス (状態の単位)
│       ├── counterSlice.ts        # カウンタースライス
│       │                          # - value: number
│       │                          # - increment/decrement/incrementByAmount/reset
│       │
│       └── userSlice.ts           # ユーザースライス
│                                  # - currentUser: User | null
│                                  # - isLoading: boolean
│                                  # - error: string | null
│                                  # - setUser/clearUser/setLoading/setError
│
├── hooks/                         # カスタムフック
│   └── useRedux.ts                # 型付きReduxフック
│                                  # - useAppDispatch: () => AppDispatch
│                                  # - useAppSelector: TypedUseSelectorHook<RootState>
│
├── lib/                           # ライブラリ・ユーティリティ
│   └── api/
│       ├── client.ts              # Axiosクライアント設定
│       │                          # - baseURL: EXPO_PUBLIC_API_URL
│       │                          # - リクエスト/レスポンスインターセプター
│       │                          # - 認証トークン処理
│       │
│       └── users.ts               # ユーザーAPI関数
│                                  # - getUsers(): Promise<User[]>
│                                  # - getUser(id): Promise<User>
│                                  # - createUser(data): Promise<User>
│                                  # - updateUser(id, data): Promise<User>
│                                  # - deleteUser(id): Promise<void>
│
├── __tests__/                     # テストファイル
│   └── store.test.ts              # Reduxストアテスト
│                                  # - 初期状態確認
│                                  # - アクション動作確認
│
├── assets/                        # 静的アセット (画像・フォント)
│   ├── icon.png                   # アプリアイコン (1024x1024)
│   ├── splash-icon.png            # スプラッシュ画面 (1284x2778)
│   ├── adaptive-icon.png          # Androidアダプティブアイコン (1024x1024)
│   └── favicon.png                # Webファビコン
│
├── app.json                       # Expo設定ファイル
│                                  # - アプリ名・スラッグ・バージョン
│                                  # - iOS/Android固有設定
│                                  # - スプラッシュ画面設定
│                                  # - プラグイン設定 (expo-router)
│
├── package.json                   # 依存関係・スクリプト
│                                  # - start: Expo開発サーバー
│                                  # - ios/android/web: プラットフォーム別実行
│                                  # - test: Jest実行
│
├── tsconfig.json                  # TypeScript設定
│                                  # - expo/tsconfig.base 継承
│                                  # - パスエイリアス: @/*
│
├── babel.config.js                # Babel設定
│                                  # - babel-preset-expo
│                                  # - react-native-reanimated/plugin
│
├── jest.config.js                 # Jest設定
│                                  # - jest-expo preset
│                                  # - transformIgnorePatterns
│                                  # - カバレッジ設定
│
├── jest.setup.js                  # Jestセットアップ
│                                  # - @testing-library/jest-native
│                                  # - Expoモジュールモック
│
└── .eslintrc.js                   # ESLint設定
                                   # - expo config
                                   # - prettier統合
```

## ルーティング構造

Expo Router はファイルベースルーティング:

```
app/
├── _layout.tsx           → 全画面共通レイアウト
└── (app)/                → /app グループ (パスに含まれない)
    └── (tabs)/           → /tabs グループ (パスに含まれない)
        ├── index.tsx     → /          (ホーム)
        ├── counter.tsx   → /counter   (カウンター)
        ├── users.tsx     → /users     (ユーザー)
        └── settings.tsx  → /settings  (設定)
```

### グループ命名規則

- `(name)`: パスに含まれないグループ
- `_layout.tsx`: グループ内共通レイアウト

## アーキテクチャ特徴

### Expo Router (ファイルベースナビゲーション)

- **自動ルーティング**: ファイル構造がそのままルートになる
- **型安全**: TypeScript 型定義が自動生成される
- **ディープリンク**: URL スキームが自動設定される
- **Web サポート**: 同じコードが Web でも動作

### Redux Toolkit (状態管理)

- **Slices**: 機能ごとに状態を分割
- **Immer 統合**: ミュータブルな書き方で不変更新
- **TypeScript**: 完全な型推論
- **DevTools**: Redux DevTools で状態デバッグ

### コンポーネント構成

#### プレゼンテーショナルコンポーネント

見た目のみを担当:

```typescript
// 純粋なUIコンポーネント
const UserCard = ({ user }: { user: User }) => (
  <View>
    <Text>{user.name}</Text>
  </View>
)
```

#### コンテナコンポーネント

ロジック・状態管理を担当:

```typescript
// Redux/APIと連携
const UsersScreen = () => {
  const dispatch = useAppDispatch()
  const users = useAppSelector((state) => state.user.users)
  // ...
}
```

## データフロー

```
ユーザー操作
    ↓
コンポーネント
    ↓
dispatch(action) → Redux Store
    ↓              ↓
API Call       状態更新
    ↓              ↓
レスポンス     useSelector
    ↓              ↓
dispatch ────→ 再レンダリング
```

## スタイリング戦略

### StyleSheet API

React Native 標準:

```typescript
const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5'
  }
})
```

### レスポンシブデザイン

```typescript
import { Dimensions } from 'react-native'

const { width, height } = Dimensions.get('window')

const styles = StyleSheet.create({
  container: {
    width: width > 768 ? '50%' : '100%'
  }
})
```

## パフォーマンス最適化

### FlatList 最適化

```typescript
<FlatList
  data={users}
  renderItem={renderUser}
  keyExtractor={(item) => item.id}
  // パフォーマンス設定
  removeClippedSubviews={true}
  maxToRenderPerBatch={10}
  windowSize={5}
  initialNumToRender={10}
  // メモ化
  getItemLayout={(data, index) => ({
    length: ITEM_HEIGHT,
    offset: ITEM_HEIGHT * index,
    index
  })}
/>
```

### React.memo

```typescript
const UserCard = React.memo(
  ({ user }: Props) => {
    // ...
  },
  (prevProps, nextProps) => {
    return prevProps.user.id === nextProps.user.id
  }
)
```

## テスト戦略

### ユニットテスト (Redux)

```typescript
test('increment action', () => {
  const state = counterReducer(undefined, increment())
  expect(state.value).toBe(1)
})
```

### コンポーネントテスト

```typescript
test('renders user name', () => {
  const { getByText } = render(<UserCard user={{ id: '1', name: 'Alice' }} />)
  expect(getByText('Alice')).toBeTruthy()
})
```

### インテグレーションテスト

```typescript
test('fetches and displays users', async () => {
  const { getByText } = render(<UsersScreen />)

  await waitFor(() => {
    expect(getByText('Alice')).toBeTruthy()
  })
})
```

このアーキテクチャにより、スケーラブルでメンテナンス性の高いモバイルアプリを構築できます。
