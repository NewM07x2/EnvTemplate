# Next.js プロジェクト

このプロジェクトは、[`create-next-app`](https://github.com/vercel/next.js/tree/canary/packages/create-next-app)を使用して作成された[Next.js](https://nextjs.org/)プロジェクトです。

## プロジェクト概要

このプロジェクトは、Next.js を使用してモダンな Web アプリケーションを構築するためのテンプレートです。API ルート、動的ルーティング、Tailwind CSS との統合など、さまざまな機能の例が含まれています。

## ディレクトリ構成

```plaintext
next/
├── .storybook/         # Storybook の設定ファイル
├── public/             # 静的アセット（画像、フォントなど）
├── src/                # ソースコード
│   ├── app/            # Next.js のアプリディレクトリ（ページ、レイアウトなど）
│   ├── components/     # 再利用可能な UI コンポーネント
│   ├── const/          # アプリ全体で使用される定数
│   ├── hooks/          # カスタム React フック
│   ├── lib/            # ユーティリティ関数やライブラリ
│   ├── store/          # Redux ストアとスライス
│   ├── styles/         # グローバル CSS と Tailwind の設定
│   └── module/         # 特定の機能やモジュール
├── docker/             # Docker 関連の設定ファイル
│   ├── Dockerfile      # Next.js アプリケーション用の Dockerfile
│   └── docker-compose.yml # Docker Compose 設定ファイル
└── ...
```

## はじめに

### 必要条件

以下がインストールされていることを確認してください：

- Node.js (v16 以上)
- npm, yarn, pnpm, または bun（いずれかのパッケージマネージャー）

### インストール

依存関係をインストールします：

```bash
npm install
# または
yarn install
# または
pnpm install
# または
bun install
```

### 開発サーバーの起動

開発サーバーを起動します：

```bash
npm run dev
# または
yarn dev
# または
pnpm dev
# または
bun dev
```

ブラウザで [http://localhost:3000](http://localhost:3000) を開き、結果を確認してください。

### 本番ビルド

本番用にアプリケーションをビルドします：

```bash
npm run build
# または
yarn build
# または
pnpm build
# または
bun build
```

### 本番サーバーの起動

ビルド後、本番サーバーを起動します：

```bash
npm run start
# または
yarn start
# または
pnpm start
# または
bun start
```

## Docker を使用した起動方法

このプロジェクトは Docker を使用して起動することも可能です。以下の手順に従ってください。

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