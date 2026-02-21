# React Native モバイルアプリテンプレート

Expo + React Native + Redux Toolkit + TypeScript を使用したクロスプラットフォームモバイルアプリケーション開発テンプレートです。

## 📋 目次

- [概要](#概要)
- [技術スタック](#技術スタック)
- [プロジェクト構成](#プロジェクト構成)
- [セットアップ](#セットアップ)
- [開発](#開発)
- [テスト](#テスト)
- [ビルド・デプロイ](#ビルドデプロイ)
- [主な機能](#主な機能)
- [トラブルシューティング](#トラブルシューティング)

## 概要

### 主な特徴

- **📱 クロスプラットフォーム**: iOS / Android / Web 対応
- **🗂️ Expo Router**: ファイルベースルーティング
- **🔄 Redux Toolkit**: グローバル状態管理
- **📘 TypeScript**: 完全型安全
- **🎨 Native UI**: iOS/Android ネイティブコンポーネント
- **🧪 Jest Testing**: ユニットテスト対応
- **🌐 API Client**: Axios による型安全な HTTP 通信

### ユースケース

- モバイルアプリ開発
- プロトタイプ作成
- iOS/Android 同時開発
- Web アプリのモバイル版

## 技術スタック

### コア

- **React Native 0.76**: クロスプラットフォーム UI フレームワーク
- **Expo 52**: 開発・ビルド・デプロイツールチェーン
- **TypeScript 5**: 型安全な開発環境

### ナビゲーション

- **Expo Router 4**: ファイルベースルーティング
- **React Navigation 7**: ネイティブナビゲーション

### 状態管理

- **Redux Toolkit 2**: 効率的な状態管理
- **React Redux 9**: React-Redux バインディング

### UI・アニメーション

- **React Native Reanimated 3**: 高性能アニメーション
- **React Native Gesture Handler 2**: ジェスチャー処理
- **Expo Vector Icons**: アイコンライブラリ

### API・データ

- **Axios 1**: HTTP クライアント
- **Expo Constants**: 環境変数管理

### テスト

- **Jest 29**: テストランナー
- **React Native Testing Library 12**: コンポーネントテスト
- **Jest Expo**: Expo 対応 Jest 設定

## プロジェクト構成

```
react-native/
├── app/                       # Expo Routerアプリディレクトリ
│   ├── _layout.tsx            # ルートレイアウト (Reduxプロバイダー)
│   └── (app)/                 # アプリグループ
│       ├── index.tsx          # Stackナビゲーション設定
│       └── (tabs)/            # タブナビゲーショングループ
│           ├── _layout.tsx    # タブレイアウト
│           ├── index.tsx      # ホーム画面
│           ├── counter.tsx    # カウンター画面 (Redux)
│           ├── users.tsx      # ユーザー一覧画面 (API)
│           └── settings.tsx   # 設定画面
│
├── store/                     # Redux状態管理
│   ├── store.ts               # ストア設定
│   └── slices/
│       ├── counterSlice.ts    # カウンタースライス
│       └── userSlice.ts       # ユーザースライス
│
├── hooks/                     # カスタムフック
│   └── useRedux.ts            # 型付きReduxフック
│
├── lib/                       # ライブラリ・ユーティリティ
│   └── api/
│       ├── client.ts          # Axiosクライアント
│       └── users.ts           # ユーザーAPI
│
├── __tests__/                 # テストファイル
│   └── store.test.ts          # ストアテスト
│
├── assets/                    # 静的アセット
│   ├── icon.png               # アプリアイコン
│   ├── splash-icon.png        # スプラッシュ画面
│   └── adaptive-icon.png      # Androidアダプティブアイコン
│
├── app.json                   # Expo設定
├── package.json               # 依存関係
├── tsconfig.json              # TypeScript設定
├── babel.config.js            # Babel設定
├── jest.config.js             # Jest設定
└── jest.setup.js              # Jestセットアップ
```

## セットアップ

### 前提条件

- Node.js 22 以上
- npm または yarn
- **iOS 開発**: macOS + Xcode
- **Android 開発**: Android Studio + JDK

### 初回セットアップ

1. **依存関係のインストール**

```powershell
cd react-native
npm install
```

2. **開発サーバー起動**

```powershell
npm start
```

3. **プラットフォーム別実行**

```powershell
# iOS (macOS のみ)
npm run ios

# Android
npm run android

# Web
npm run web
```

## 開発

### Expo Go での開発 (推奨)

1. スマートフォンに**Expo Go**アプリをインストール

   - [iOS App Store](https://apps.apple.com/jp/app/expo-go/id982107779)
   - [Google Play Store](https://play.google.com/store/apps/details?id=host.exp.exponent)

2. 開発サーバー起動

```powershell
npm start
```

3. QR コードをスキャンして実行

### ローカルビルドでの開発

```powershell
# iOSシミュレーター (macOS)
npm run ios

# Androidエミュレーター
npm run android
```

### ホットリロード

コードを変更すると自動的にリロードされます:

- **Fast Refresh**: コンポーネントの状態を保持したまま更新
- **R キー**: 手動リロード
- **Shift + R**: キャッシュクリア & リロード

### 環境変数

`.env.local` ファイル作成 (Git 除外):

```bash
EXPO_PUBLIC_API_URL=http://localhost:4000
```

使用例:

```typescript
const apiUrl = process.env.EXPO_PUBLIC_API_URL
```

## テスト

### Jest + React Native Testing Library

```powershell
# テスト実行
npm test

# ウォッチモード
npm test -- --watch

# カバレッジ
npm test -- --coverage
```

### テスト例

```typescript
import { render, fireEvent } from '@testing-library/react-native'
import CounterScreen from '@/app/(app)/(tabs)/counter'

test('counter increments', () => {
  const { getByText } = render(<CounterScreen />)

  const incrementButton = getByText('+1')
  fireEvent.press(incrementButton)

  expect(getByText('1')).toBeTruthy()
})
```

## ビルド・デプロイ

### EAS Build (推奨)

1. **EAS CLI インストール**

```powershell
npm install -g eas-cli
```

2. **EAS ログイン**

```powershell
eas login
```

3. **プロジェクト設定**

```powershell
eas build:configure
```

4. **ビルド実行**

```powershell
# iOS
eas build --platform ios

# Android
eas build --platform android

# 両方
eas build --platform all
```

### ローカルビルド

#### Android APK

```powershell
# 開発ビルド
npx expo run:android --variant debug

# プロダクションビルド
eas build --platform android --local
```

#### iOS IPA (macOS のみ)

```powershell
# 開発ビルド
npx expo run:ios --configuration Debug

# プロダクションビルド
eas build --platform ios --local
```

### ストア公開

#### iOS App Store

1. EAS でプロダクションビルド
2. App Store Connect にアップロード
3. TestFlight でテスト
4. 審査提出

#### Google Play Store

1. EAS でプロダクションビルド (AAB)
2. Google Play Console にアップロード
3. 内部テスト → クローズドテスト → 公開

## 主な機能

### 1. Expo Router (ファイルベースルーティング)

#### ディレクトリ構造 → ルート

```
app/
├── (app)/
│   └── (tabs)/
│       ├── index.tsx      → /
│       ├── counter.tsx    → /counter
│       └── users.tsx      → /users
```

#### ナビゲーション

```typescript
import { Link, router } from 'expo-router'

// Linkコンポーネント
;<Link href='/counter'>カウンターへ</Link>

// プログラムナビゲーション
router.push('/users')
router.back()
```

### 2. Redux Toolkit

#### スライス定義

```typescript
const counterSlice = createSlice({
  name: 'counter',
  initialState: { value: 0 },
  reducers: {
    increment: (state) => {
      state.value += 1
    }
  }
})
```

#### コンポーネントで使用

```typescript
import { useAppDispatch, useAppSelector } from '@/hooks/useRedux'

const count = useAppSelector((state) => state.counter.value)
const dispatch = useAppDispatch()

;<Button onPress={() => dispatch(increment())} />
```

### 3. API 連携 (Axios)

#### クライアント設定

```typescript
const apiClient = axios.create({
  baseURL: 'http://localhost:4000',
  timeout: 10000
})
```

#### API 呼び出し

```typescript
const users = await userApi.getUsers()
const user = await userApi.getUser(id)
await userApi.createUser({ name, email })
```

### 4. タブナビゲーション

```typescript
<Tabs>
  <Tabs.Screen
    name='index'
    options={{
      title: 'ホーム',
      tabBarIcon: ({ color }) => <Ionicons name='home' color={color} />
    }}
  />
</Tabs>
```

## トラブルシューティング

### キャッシュクリア

```powershell
# Metro bundler キャッシュクリア
npx expo start --clear

# node_modules 再インストール
Remove-Item -Recurse -Force node_modules
npm install
```

### iOS ビルドエラー

```powershell
# CocoaPods 再インストール
cd ios
pod install
cd ..
```

### Android ビルドエラー

```powershell
# Gradleキャッシュクリア
cd android
./gradlew clean
cd ..
```

### Metro bundler ポート競合

```powershell
# 別ポート使用
npx expo start --port 8082
```

### TypeScript エラー

```powershell
# 型定義再生成
rm -rf node_modules
npm install
```

### Expo Go で動作しない機能

一部のネイティブモジュールは Expo Go で動作しません:

- カスタムネイティブコード
- 特定のライブラリ (react-native-camera 等)

→ **開発ビルド**を使用:

```powershell
npx expo run:ios
npx expo run:android
```

## パフォーマンス最適化

### 1. リスト最適化

```typescript
<FlatList
  data={users}
  renderItem={renderUser}
  keyExtractor={(item) => item.id}
  removeClippedSubviews={true}
  maxToRenderPerBatch={10}
  windowSize={5}
/>
```

### 2. 画像最適化

```typescript
<Image
  source={{ uri: imageUrl }}
  style={styles.image}
  resizeMode='cover'
  // キャッシュ有効化
  cache='force-cache'
/>
```

### 3. メモ化

```typescript
const MemoizedComponent = React.memo(MyComponent)

const expensiveValue = useMemo(() => {
  return computeExpensiveValue(a, b)
}, [a, b])
```

## 参考リンク

- [React Native 公式](https://reactnative.dev/)
- [Expo 公式ドキュメント](https://docs.expo.dev/)
- [Expo Router](https://docs.expo.dev/router/introduction/)
- [Redux Toolkit](https://redux-toolkit.js.org/)
- [React Navigation](https://reactnavigation.org/)
- [EAS Build](https://docs.expo.dev/build/introduction/)

## ライセンス

MIT
