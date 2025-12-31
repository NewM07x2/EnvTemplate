# React + GraphQL + Prisma ディレクトリ構造

```
react/
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
│   ├── store/
│   │   ├── store.ts            # Redux store設定
│   │   └── slices/
│   │       ├── counterSlice.ts     # サンプルslice
│   │       └── counterSlice.test.ts # sliceテスト
│   ├── pages/
│   │   ├── HomePage.tsx        # ホームページ
│   │   ├── HomePage.test.tsx   # ホームページテスト
│   │   ├── GraphQLPage.tsx     # urql使用例
│   │   ├── GraphQLPage.test.tsx # GraphQLページテスト
│   │   ├── PrismaPage.tsx      # Prisma使用例
│   │   └── PrismaPage.test.tsx # Prismaページテスト
│   ├── test/
│   │   ├── setup.ts            # テストセットアップ
│   │   └── testing-guide.md    # テストガイド
│   ├── styles/
│   │   └── index.css           # グローバルスタイル
│   ├── App.tsx                 # メインアプリケーション
│   ├── App.test.tsx            # アプリテスト
│   └── main.tsx                # エントリーポイント
├── coverage/                   # カバレッジレポート（自動生成）
├── index.html                  # HTMLテンプレート
├── vite.config.ts             # Vite設定（Vitest設定含む）
├── tsconfig.json              # TypeScript設定
├── tsconfig.node.json         # Node用TypeScript設定
├── eslint.config.js           # ESLint設定
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

### `/src/store/`

Redux Toolkit の状態管理

### `/src/pages/`

各ページコンポーネントとそのテスト

### `/src/test/`

テスト設定とガイド

- `setup.ts` - グローバルテストセットアップ
- `testing-guide.md` - 詳細なテストガイド

### `/docker/`

Docker 関連ファイル

### `/coverage/`

テストカバレッジレポート（`npm run test:coverage`で自動生成）

## テストファイルの命名規則

- コンポーネント: `ComponentName.test.tsx`
- ロジック/ユーティリティ: `fileName.test.ts`
- テストファイルは対象ファイルと同じディレクトリに配置
