# Vue + GraphQL + Prisma ディレクトリ構造

```
vue/
├── docker/
│   └── Dockerfile              # フロントエンド用Dockerファイル
├── src/
│   ├── lib/
│   │   ├── graphql/
│   │   │   ├── urqlClient.ts   # urql GraphQLクライアント設定 (CSR用)
│   │   │   ├── urqlClient.test.ts # urqlクライアントテスト
│   │   │   └── graphql.md      # GraphQL使用ガイド
│   │   └── prisma/
│   │       ├── client.ts       # Prismaクライアント設定
│   │       └── schema.prisma   # Prismaスキーマ定義
│   ├── stores/
│   │   ├── counter.ts          # サンプルstore (Pinia)
│   │   └── counter.test.ts     # storeテスト
│   ├── views/
│   │   ├── HomePage.vue        # ホームページ
│   │   ├── HomePage.test.ts    # ホームページテスト
│   │   ├── GraphQLPage.vue     # urql使用例
│   │   └── PrismaPage.vue      # Prisma使用例
│   ├── router/
│   │   └── index.ts            # Vue Routerの設定
│   ├── test/
│   │   └── setup.ts            # テストセットアップ
│   ├── styles/
│   │   └── main.css            # グローバルスタイル
│   ├── App.vue                 # メインアプリケーション
│   ├── App.test.ts             # アプリテスト
│   └── main.ts                 # エントリーポイント
├── coverage/                   # カバレッジレポート（自動生成）
├── index.html                  # HTMLテンプレート
├── vite.config.ts             # Vite設定（Vitest設定含む）
├── tsconfig.json              # TypeScript設定
├── tsconfig.node.json         # Node用TypeScript設定
├── .eslintrc.cjs              # ESLint設定
├── package.json               # 依存関係（テストツール含む）
├── docker-compose.yml         # Docker Compose設定
├── .env.example               # 環境変数サンプル
├── .gitignore                 # Git除外設定
├── .node-version              # Node.jsバージョン指定
└── README.md                  # ドキュメント
```

## 主要ディレクトリの説明

### `/src/lib/graphql/`

CSR 用の GraphQL 設定と urql クライアント

### `/src/lib/prisma/`

Prisma クライアントとスキーマ定義（API 経由で使用）

### `/src/stores/`

Pinia の状態管理ストア

### `/src/views/`

各ページコンポーネントとそのテスト

### `/src/router/`

Vue Router の設定

### `/src/test/`

テスト設定とガイド

### `/docker/`

Docker 関連ファイル

### `/coverage/`

テストカバレッジレポート（`npm run test:coverage`で自動生成）

## テストファイルの命名規則

- コンポーネント: `ComponentName.test.ts`
- Store: `storeName.test.ts`
- ユーティリティ: `fileName.test.ts`
- テストファイルは対象ファイルと同じディレクトリに配置
