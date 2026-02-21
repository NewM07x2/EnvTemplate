# Sample Directory Structure

以下は`sample`フォルダ配下のディレクトリ構成です。

```
.sample/
├── .eslintrc.json
├── .gitignore
├── .node-version
├── .storybook/
│   ├── main.ts
│   └── preview.ts
├── next.config.mjs
├── package-lock.json
├── package.json
├── postcss.config.js
├── prisma/
│   ├── migrations/
│   └── schema.prisma
├── public/
│   ├── favicon.ico
│   ├── next.svg
│   ├── sanuna.svg
│   └── vercel.svg
├── README.md
├── src/
│   ├── app/
│   │   ├── api/
│   │   │   ├── get-api/
│   │   │   ├── getJsonData.ts
│   │   │   ├── layout.tsx
│   │   │   ├── page.tsx
│   │   │   ├── sample/
│   │   │   └── weather/
│   │   ├── blog-page/
│   │   ├── contact-page/
│   │   ├── error.tsx
│   │   ├── graphql/
│   │   ├── layout.tsx
│   │   ├── modal-page/
│   │   ├── not-found.tsx
│   │   ├── page.tsx
│   │   ├── pages/
│   │   ├── providers.tsx
│   │   ├── reducer-page/
│   │   ├── redux-page/
│   │   └── type-script/
│   ├── components/
│   │   ├── base/
│   │   ├── page/
│   │   ├── sample/
│   │   └── ui/
│   ├── const/
│   ├── hooks.ts
│   ├── lib/
│   │   ├── api.ts
│   │   └── その他のライブラリ
│   ├── model/
│   ├── module/
│   ├── store/
│   ├── stories/
│   │   ├── assets/
│   │   ├── button.css
│   │   ├── Button.stories.ts
│   │   ├── Button.tsx
│   │   ├── Configure.mdx
│   │   ├── header.css
│   │   ├── Header.stories.ts
│   │   ├── Header.tsx
│   │   ├── page.css
│   │   ├── Page.stories.ts
│   │   └── Page.tsx
│   └── styles/
├── tailwind.config.ts
└── tsconfig.json
```

## 補足

- **`.storybook/`**: Storybookの設定ファイルが含まれています。コンポーネントのドキュメント化やUIテストに使用されます。
- **`prisma/`**: Prisma ORMのスキーマとマイグレーションファイルが格納されています。
- **`public/`**: 静的アセット（画像やアイコンなど）が配置されています。
- **`src/`**: アプリケーションの主要なソースコードが含まれています。
  - **`app/`**: Next.jsのApp Routerを使用したページやAPIルートが含まれています。
  - **`components/`**: 再利用可能なUIコンポーネントが格納されています。
  - **`lib/`**: ユーティリティ関数やAPIクライアントが含まれています。
  - **`stories/`**: Storybook用のストーリーファイルが含まれています。
- **`tailwind.config.ts`**: Tailwind CSSの設定ファイル。
- **`tsconfig.json`**: TypeScriptの設定ファイル。