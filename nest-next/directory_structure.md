# Nest.js + Next.js ディレクトリ構造

```
nest-next/
├── docker-compose.yml          # Docker Compose設定ファイル
├── .env.example                # 環境変数のサンプルファイル
├── .gitignore                  # Gitで追跡しないファイルの設定
├── .node-version               # Node.jsバージョン指定 (22)
├── README.md                   # プロジェクト説明書
│
├── nest-app/                   # NestJSバックエンドアプリケーション
│   ├── src/
│   │   ├── main.ts             # アプリケーションエントリーポイント
│   │   ├── app.module.ts       # ルートモジュール (GraphQL、Prisma、各機能モジュールを統合)
│   │   │
│   │   ├── prisma/             # Prisma ORM関連
│   │   │   ├── prisma.service.ts   # PrismaClientのサービスクラス
│   │   │   └── prisma.module.ts    # Prismaのグローバルモジュール
│   │   │
│   │   ├── users/              # ユーザー機能モジュール
│   │   │   ├── user.model.ts       # GraphQLオブジェクトタイプ定義
│   │   │   ├── users.service.ts    # ユーザービジネスロジック
│   │   │   ├── users.resolver.ts   # GraphQLリゾルバー (クエリ・ミューテーション)
│   │   │   └── users.module.ts     # ユーザーモジュール定義
│   │   │
│   │   ├── posts/              # 投稿機能モジュール
│   │   │   ├── posts.service.ts    # 投稿ビジネスロジック
│   │   │   ├── posts.resolver.ts   # GraphQLリゾルバー
│   │   │   └── posts.module.ts     # 投稿モジュール定義
│   │   │
│   │   └── auth/               # 認証機能モジュール
│   │       ├── auth.service.ts     # 認証ロジック (JWT発行、検証)
│   │       ├── auth.module.ts      # 認証モジュール (PassportJS、JWT設定)
│   │       └── jwt.strategy.ts     # JWT認証ストラテジー
│   │
│   ├── prisma/
│   │   └── schema.prisma       # Prismaデータモデル定義 (User, Post)
│   │
│   ├── test/                   # テストファイル格納ディレクトリ
│   │   └── jest-e2e.json       # E2Eテスト設定
│   │
│   ├── package.json            # NestJS依存関係・スクリプト
│   ├── tsconfig.json           # TypeScript設定
│   ├── tsconfig.build.json     # ビルド用TypeScript設定
│   ├── nest-cli.json           # NestJS CLI設定
│   └── Dockerfile              # バックエンド用Dockerイメージ
│
└── next/                       # Next.jsフロントエンドアプリケーション
    ├── src/
    │   ├── app/                # App Router (Next.js 13+)
    │   │   ├── layout.tsx          # ルートレイアウト (Providers設定)
    │   │   ├── page.tsx            # ホームページ
    │   │   ├── globals.css         # グローバルスタイル (Tailwind CSS)
    │   │   ├── users/
    │   │   │   └── page.tsx        # ユーザー一覧ページ (Apollo Clientでデータ取得)
    │   │   └── graphql/
    │   │       └── page.tsx        # GraphQL API解説ページ
    │   │
    │   ├── components/         # Reactコンポーネント
    │   │   ├── Counter.tsx         # Reduxカウンターコンポーネント
    │   │   └── Providers.tsx       # Redux + Apollo Clientプロバイダー
    │   │
    │   ├── store/              # Redux Toolkit状態管理
    │   │   ├── store.ts            # Reduxストア設定
    │   │   └── slices/
    │   │       └── counterSlice.ts # カウンタースライス (状態・アクション)
    │   │
    │   ├── lib/
    │   │   └── graphql/        # GraphQL関連
    │   │       ├── apolloClient.ts # Apollo Clientインスタンス
    │   │       └── queries.ts      # GraphQLクエリ・ミューテーション定義
    │   │
    │   ├── hooks.ts            # Reduxカスタムフック (useAppDispatch, useAppSelector)
    │   │
    │   └── test/               # テスト関連
    │       ├── setup.ts            # Vitestセットアップ
    │       └── example.test.ts     # サンプルテストケース
    │
    ├── public/                 # 静的ファイル配置
    │   └── (ファビコン、画像など)
    │
    ├── package.json            # Next.js依存関係・スクリプト
    ├── tsconfig.json           # TypeScript設定
    ├── next.config.mjs         # Next.js設定
    ├── tailwind.config.ts      # Tailwind CSS設定
    ├── postcss.config.js       # PostCSS設定
    ├── vitest.config.ts        # Vitestテスト設定
    └── Dockerfile              # フロントエンド用Dockerイメージ
```

## 各ディレクトリの役割

### バックエンド (nest-app/)

- **src/main.ts**: NestJS アプリケーションのエントリーポイント。CORS、バリデーション設定を行う
- **src/app.module.ts**: GraphQL、Prisma、各機能モジュールを統合するルートモジュール
- **src/prisma/**: PrismaClient を NestJS の DI コンテナに登録するグローバルモジュール
- **src/users/**: ユーザー CRUD 操作の GraphQL リゾルバーとサービス
- **src/posts/**: 投稿 CRUD 操作の GraphQL リゾルバーとサービス
- **src/auth/**: JWT 認証ロジック (PassportJS + bcrypt)
- **prisma/schema.prisma**: データベーススキーマ定義 (User, Post)

### フロントエンド (next/)

- **src/app/**: Next.js App Router (ファイルベースルーティング)
- **src/components/**: 再利用可能な React コンポーネント
- **src/store/**: Redux Toolkit による状態管理 (カウンターサンプル)
- **src/lib/graphql/**: Apollo Client 設定と GraphQL クエリ定義
- **src/hooks.ts**: Redux の型安全なカスタムフック
- **src/test/**: Vitest + React Testing Library のテスト設定

## アーキテクチャ特徴

### TypeScript 統一

- フロントエンド: TypeScript + React
- バックエンド: TypeScript + NestJS
- GraphQL による型安全な通信

### モジュラー設計 (NestJS)

各機能(users, posts, auth)が独立したモジュールとして実装され、依存性注入(DI)により疎結合を実現

### App Router (Next.js)

- **RSC (React Server Components)**: デフォルトでサーバーコンポーネント
- **クライアントコンポーネント**: 'use client'ディレクティブで明示
- **ファイルベースルーティング**: page.tsx がルートになる

### データフェッチング戦略

- **Apollo Client**: GraphQL クエリによるキャッシュ管理
- **Redux Toolkit**: クライアント側状態管理
- **Prisma**: サーバー側データベースアクセス

### 認証フロー

1. フロントエンド: ログインフォーム送信
2. バックエンド: JWT 発行 (auth.service.ts)
3. フロントエンド: トークンを localStorage に保存
4. 以降のリクエスト: Authorization Bearer ヘッダーでトークン送信
5. バックエンド: JwtStrategy で検証 → リゾルバーで@CurrentUser()使用可能
