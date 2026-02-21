# Next.js + GraphQL + Prisma テンプレート

GraphQLとPrismaをSSRで利用するNext.jsアプリケーション用のテンプレートです。このテンプレートをコピーしてすぐに開発を始められます。

## 特徴

- ✨ **Next.js 14.1.0** - 最新のServer Componentsサポート
- 🔗 **GraphQL** - urql/Next によるSSR対応のAPI通信
- 🗄️ **Prisma** - 型安全なORM
- 🎨 **Tailwind CSS** - ユーティリティファーストなCSS
- 📦 **Redux Toolkit** - 状態管理
- 🔍 **TypeScript** - 完全なType Safety

## ディレクトリ構成

```plaintext
src/
├── app/                # Next.js App Router
│   ├── api/           # API ルート
│   ├── layout.tsx     # ルートレイアウト
│   ├── page.tsx       # ホームページ
│   ├── error.tsx      # エラーページ
│   └── not-found.tsx  # 404 ページ
├── components/        # React コンポーネント
│   ├── base/         # レイアウト、ヘッダーなど
│   └── elements/     # ボタン、入力フィールドなど
├── const/            # 定数定義
├── hooks/            # カスタム React フック
├── lib/              # ユーティリティとライブラリ
│   ├── graphql/      # GraphQL クライアント設定
│   └── prisma/       # Prisma スキーマ
├── store/            # Redux ストア
│   └── slices/       # Redux スライス
├── styles/           # グローバル CSS
└── providers.tsx     # アプリプロバイダー
```

## セットアップ手順

### 1. 依存パッケージをインストール

```bash
npm install
```

### 2. 環境変数を設定

`.env.local` を作成して環境変数を設定します：

```env
# データベース
DATABASE_URL="your-database-url"

# GraphQL
GRAPHQL_ENDPOINT="your-graphql-endpoint"
```

### 3. Prisma をセットアップ

```bash
# Prisma を初期化
npx prisma init

# スキーマを設定後、マイグレーションを実行
npx prisma migrate dev --name init

# Prisma クライアントを生成
npx prisma generate
```

### 4. 開発サーバーを起動

```bash
npm run dev
```

[http://localhost:3000](http://localhost:3000) にアクセスしてアプリが起動しているか確認してください。

## 利用可能なコマンド

```bash
# 開発サーバー起動
npm run dev

# 本番ビルド
npm run build

# 本番サーバー起動
npm start

# Lint チェック
npm run lint
```

## 主要な設定ファイル

- **`next.config.mjs`** - Next.js の設定
- **`tsconfig.json`** - TypeScript の設定
- **`tailwind.config.ts`** - Tailwind CSS の設定
- **`.eslintrc.json`** - ESLint の設定
- **`postcss.config.js`** - PostCSS の設定

## Prisma の使用例

### スキーマ定義

`src/lib/prisma/schema.prisma`:

```prisma
model User {
  id    Int     @id @default(autoincrement())
  email String  @unique
  name  String?
}
```

### データ操作

```typescript
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

// ユーザーを作成
const user = await prisma.user.create({
  data: {
    email: 'user@example.com',
    name: 'John Doe',
  },
});

// ユーザーを取得
const users = await prisma.user.findMany();
```

## GraphQL の使用例

`src/lib/graphql/urqlClient.ts` を参照して urql クライアントを設定し、GraphQL クエリを実行します。

## Docker での起動

```bash
docker-compose -f docker/docker-compose.yml up
```

## 注意事項

- このテンプレートはSSRを前提としています
- Prisma のマイグレーションを実行する前に、スキーマを適切に設定してください
- GraphQL エンドポイントの設定を忘れずに行ってください

## ライセンス

MIT

### 必要な環境

- Docker がインストールされていること。
- Docker Compose が使用可能であること。

### 手順

1. Docker イメージをビルドします：

   ```bash
   docker-compose build
   ```

2. コンテナを起動します：

   ```bash
   docker-compose up
   ```

3. ブラウザで [http://localhost:3000](http://localhost:3000) を開き、結果を確認してください。

4. コンテナを停止する場合：

   ```bash
   docker-compose down
   ```

### その他のコマンド

- **キャッシュを削除してビルドする場合**:

  ```bash
  docker-compose build --no-cache
  ```

- **ボリュームを削除して再ビルドする場合**:

  ```bash
  docker-compose down -v && docker-compose up --build
  ```

- **バックグラウンドでコンテナを起動する場合**:

  ```bash
  docker-compose up -d
  ```

- **実行中のコンテナを確認する場合**:

  ```bash
  docker ps
  ```

- **コンテナのログを確認する場合**:

  ```bash
  docker-compose logs
  ```

### Docker 関連のフォルダ構成

```plaintext
docker/               # Docker 関連の設定ファイルを格納
├── Dockerfile        # Next.js アプリケーション用の Dockerfile
├── docker-compose.yml # Docker Compose 設定ファイル
```

Docker を使用することで、ローカル環境に依存せずにアプリケーションを実行できます。

## 使用技術

- [Next.js](https://nextjs.org/): サーバーサイドレンダリングと静的サイト生成のための React フレームワーク。
- [Tailwind CSS](https://tailwindcss.com/): ユーティリティファーストの CSS フレームワーク。
- [Redux Toolkit](https://redux-toolkit.js.org/): 状態管理ライブラリ。
- [Storybook](https://storybook.js.org/): UI コンポーネントエクスプローラー。
- [GraphQL](https://graphql.org/): 柔軟で効率的なデータ取得のためのクエリ言語。
- [Prisma](https://www.prisma.io/): データベース操作を簡素化するための次世代 ORM。
- [Jest](https://jestjs.io/): JavaScript テストフレームワーク。
- [React Testing Library](https://testing-library.com/docs/react-testing-library/intro): React コンポーネントのテストライブラリ。

## 環境変数

ルートディレクトリに `.env.local` ファイルを作成し、必要な環境変数を追加します。例：

```plaintext
NEXT_PUBLIC_API_URL=https://api.example.com
```

## テスト

以下のコマンドを使用してテストを実行します：

```bash
npm run test
# または
yarn test
# または
pnpm test
# または
bun test
```

## デプロイ

Next.js アプリをデプロイする最も簡単な方法は、[Vercel プラットフォーム](https://vercel.com/)を使用することです。  
詳細については、[Next.js のデプロイメントドキュメント](https://nextjs.org/docs/deployment)を参照してください。

---

質問や問題がある場合は、このリポジトリで issue を作成してください。