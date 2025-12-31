# React + GraphQL + Prisma ディレクトリ構造

```
react/
├── docker/
│   └── Dockerfile              # フロントエンド用Dockerファイル
├── src/
│   ├── lib/
│   │   ├── graphql/
│   │   │   ├── urqlClient.ts   # urql GraphQLクライアント設定 (CSR用)
│   │   │   └── graphql.md      # GraphQL使用ガイド
│   │   └── prisma/
│   │       ├── client.ts       # Prismaクライアント設定
│   │       └── schema.prisma   # Prismaスキーマ定義
│   ├── store/
│   │   ├── store.ts            # Redux store設定
│   │   └── slices/
│   │       └── counterSlice.ts # サンプルslice
│   ├── pages/
│   │   ├── HomePage.tsx        # ホームページ
│   │   ├── GraphQLPage.tsx     # urql使用例
│   │   └── PrismaPage.tsx      # Prisma使用例
│   ├── styles/
│   │   └── index.css           # グローバルスタイル
│   ├── App.tsx                 # メインアプリケーション
│   └── main.tsx                # エントリーポイント
├── index.html                  # HTMLテンプレート
├── vite.config.ts             # Vite設定
├── tsconfig.json              # TypeScript設定
├── tsconfig.node.json         # Node用TypeScript設定
├── eslint.config.js           # ESLint設定
├── package.json               # 依存関係
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

各ページコンポーネント

### `/docker/`

Docker 関連ファイル
