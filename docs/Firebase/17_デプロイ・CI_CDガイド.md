# デプロイ・CI/CD ガイド

> **レベル**: ★★★ / 所要時間: 約 45 分  
> **前提**: [クイックスタート](02_クイックスタート.md)・[テスト戦略ガイド](16_テスト戦略ガイド.md) の完了推奨

---

## 目次

1. [デプロイ戦略の概要](#1-デプロイ戦略の概要)
2. [Firebase プロジェクトの環境分離（dev / stg / prd）](#2-firebase-プロジェクトの環境分離dev--stg--prd)
3. [Firebase CLI によるデプロイ](#3-firebase-cli-によるデプロイ)
4. [GitHub Actions によるデプロイ自動化](#4-github-actions-によるデプロイ自動化)
5. [Next.js（Vercel）× Firebase の CI/CD](#5-nextjsvercel--firebase-の-cicd)
6. [Cloud Functions の CI/CD](#6-cloud-functions-の-cicd)
7. [プレビューチャンネルを使ったレビュー環境](#7-プレビューチャンネルを使ったレビュー環境)
8. [デプロイ通知とロールバック](#8-デプロイ通知とロールバック)

---

## 1. デプロイ戦略の概要

```
ブランチ戦略とデプロイ環境のマッピング

  feature/* ──→ Pull Request ──→ [自動テスト] ──→ Preview Channel（一時 URL）
                                                     ↓ レビュー・承認
  develop   ──→ Push ──────────→ [自動テスト] ──→ Staging 環境（dev プロジェクト）
                                                     ↓ QA 確認
  main      ──→ Push ──────────→ [自動テスト] ──→ Production 環境（prd プロジェクト）
```

---

## 2. Firebase プロジェクトの環境分離（dev / stg / prd）

Firebase コンソールで環境ごとに別プロジェクトを作成することを強く推奨します。

### プロジェクト作成

```
Firebase コンソールで以下の 3 プロジェクトを作成:
  my-app-dev   （開発環境）
  my-app-stg   （ステージング環境）
  my-app-prd   （本番環境）
```

### Firebase CLI でのエイリアス設定

```bash
# プロジェクトのエイリアスを設定（.firebaserc に保存される）
firebase use --add
# → プロジェクト一覧から選択し、エイリアス名を入力
#   my-app-dev  → エイリアス: dev
#   my-app-stg  → エイリアス: stg
#   my-app-prd  → エイリアス: prd
```

```json
// .firebaserc（自動生成）
{
  "projects": {
    "dev":     "my-app-dev",
    "stg":     "my-app-stg",
    "prd":     "my-app-prd",
    "default": "my-app-dev"
  }
}
```

```bash
# 環境を切り替えてデプロイ
firebase use dev
firebase deploy

firebase use prd
firebase deploy
```

### 環境変数ファイルの管理

```
.env.local          ← ローカル開発（Git 管理外）
.env.development    ← dev 環境ビルド用
.env.staging        ← stg 環境ビルド用
.env.production     ← prd 環境ビルド用（Git 管理外・CI で注入）
```

```bash
# .env.development
NEXT_PUBLIC_FIREBASE_PROJECT_ID=my-app-dev
NEXT_PUBLIC_FIREBASE_API_KEY=AIza-dev-xxxx
# ...

# .env.production
NEXT_PUBLIC_FIREBASE_PROJECT_ID=my-app-prd
NEXT_PUBLIC_FIREBASE_API_KEY=AIza-prd-xxxx
# ...
```

---

## 3. Firebase CLI によるデプロイ

### 手動デプロイコマンド一覧

```bash
# すべてのリソースをデプロイ
firebase deploy

# サービスを個別に指定
firebase deploy --only hosting
firebase deploy --only firestore:rules
firebase deploy --only firestore:indexes
firebase deploy --only storage:rules
firebase deploy --only functions
firebase deploy --only functions:createPost,functions:sendNotification  # 特定の関数のみ

# 複数のサービスを組み合わせ
firebase deploy --only hosting,functions

# ドライラン（変更内容の確認のみ・実際のデプロイは行わない）
firebase deploy --only functions --dry-run
```

### `firebase.json` のデプロイ設定

```json
{
  "firestore": {
    "rules":   "firestore.rules",
    "indexes": "firestore.indexes.json"
  },
  "storage": {
    "rules": "storage.rules"
  },
  "hosting": {
    "public": "out",
    "ignore": ["firebase.json", "**/.*", "**/node_modules/**"],
    "rewrites": [
      { "source": "**", "destination": "/index.html" }
    ],
    "headers": [
      {
        "source": "**/*.@(js|css)",
        "headers": [{ "key": "Cache-Control", "value": "max-age=31536000" }]
      }
    ]
  },
  "functions": {
    "source":  "functions",
    "runtime": "nodejs20",
    "predeploy": [
      "npm --prefix functions run build",
      "npm --prefix functions run lint"
    ]
  }
}
```

---

## 4. GitHub Actions によるデプロイ自動化

### Staging 自動デプロイ（`develop` ブランチへの Push）

```yaml
# .github/workflows/deploy-staging.yml
name: Deploy to Staging

on:
  push:
    branches: [develop]

jobs:
  test:
    name: テスト実行
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '20', cache: 'npm' }
      - run: npm ci
      - run: npm test

  deploy:
    name: Staging デプロイ
    needs: test  # テストが成功した場合のみ実行
    runs-on: ubuntu-latest
    environment: staging  # GitHub Environments で承認設定可能
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with: { node-version: '20', cache: 'npm' }

      - run: npm ci

      - name: Next.js ビルド
        run: npm run build
        env:
          NEXT_PUBLIC_FIREBASE_PROJECT_ID:         ${{ secrets.STG_FIREBASE_PROJECT_ID }}
          NEXT_PUBLIC_FIREBASE_API_KEY:            ${{ secrets.STG_FIREBASE_API_KEY }}
          NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN:        ${{ secrets.STG_FIREBASE_AUTH_DOMAIN }}
          NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET:     ${{ secrets.STG_FIREBASE_STORAGE_BUCKET }}
          NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID: ${{ secrets.STG_FIREBASE_MESSAGING_SENDER_ID }}
          NEXT_PUBLIC_FIREBASE_APP_ID:             ${{ secrets.STG_FIREBASE_APP_ID }}

      - name: Firebase Hosting にデプロイ
        uses: FirebaseExtended/action-hosting-deploy@v0
        with:
          repoToken:       ${{ secrets.GITHUB_TOKEN }}
          firebaseServiceAccount: ${{ secrets.STG_FIREBASE_SERVICE_ACCOUNT }}
          projectId:       ${{ secrets.STG_FIREBASE_PROJECT_ID }}
          channelId:       live

      - name: Cloud Functions をデプロイ
        run: |
          npm install -g firebase-tools
          firebase deploy --only functions --project ${{ secrets.STG_FIREBASE_PROJECT_ID }}
        env:
          FIREBASE_TOKEN: ${{ secrets.FIREBASE_CI_TOKEN }}
```

### Production デプロイ（`main` ブランチへの Push）

```yaml
# .github/workflows/deploy-production.yml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  test:
    name: テスト実行
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '20', cache: 'npm' }
      - run: npm ci
      - run: npm test

  deploy:
    name: Production デプロイ
    needs: test
    runs-on: ubuntu-latest
    environment: production  # 手動承認を設定することを推奨
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '20', cache: 'npm' }
      - run: npm ci

      - name: Next.js ビルド（本番用）
        run: npm run build
        env:
          NEXT_PUBLIC_FIREBASE_PROJECT_ID:         ${{ secrets.PRD_FIREBASE_PROJECT_ID }}
          NEXT_PUBLIC_FIREBASE_API_KEY:            ${{ secrets.PRD_FIREBASE_API_KEY }}
          NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN:        ${{ secrets.PRD_FIREBASE_AUTH_DOMAIN }}
          NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET:     ${{ secrets.PRD_FIREBASE_STORAGE_BUCKET }}
          NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID: ${{ secrets.PRD_FIREBASE_MESSAGING_SENDER_ID }}
          NEXT_PUBLIC_FIREBASE_APP_ID:             ${{ secrets.PRD_FIREBASE_APP_ID }}

      - name: Firebase Hosting にデプロイ
        uses: FirebaseExtended/action-hosting-deploy@v0
        with:
          repoToken:       ${{ secrets.GITHUB_TOKEN }}
          firebaseServiceAccount: ${{ secrets.PRD_FIREBASE_SERVICE_ACCOUNT }}
          projectId:       ${{ secrets.PRD_FIREBASE_PROJECT_ID }}
          channelId:       live

      - name: Firestore ルール・インデックスをデプロイ
        run: |
          npm install -g firebase-tools
          firebase deploy --only firestore,storage --project ${{ secrets.PRD_FIREBASE_PROJECT_ID }}
        env:
          FIREBASE_TOKEN: ${{ secrets.FIREBASE_CI_TOKEN }}

      - name: Cloud Functions をデプロイ
        run: |
          firebase deploy --only functions --project ${{ secrets.PRD_FIREBASE_PROJECT_ID }}
        env:
          FIREBASE_TOKEN: ${{ secrets.FIREBASE_CI_TOKEN }}
```

### GitHub Secrets の設定

| Secret 名 | 内容 | 取得方法 |
|-----------|------|---------|
| `STG_FIREBASE_SERVICE_ACCOUNT` | サービスアカウント JSON | Firebase コンソール → プロジェクト設定 → サービスアカウント |
| `PRD_FIREBASE_SERVICE_ACCOUNT` | 本番サービスアカウント JSON | 同上 |
| `FIREBASE_CI_TOKEN` | CLI 認証トークン | `firebase login:ci` を実行 |
| `PRD_FIREBASE_API_KEY` など | 各環境の Firebase 設定値 | Firebase コンソール → プロジェクト設定 → 全般 |

```bash
# CI 用トークンの発行
firebase login:ci
# → 表示されたトークンを FIREBASE_CI_TOKEN に設定
```

---

## 5. Next.js（Vercel）× Firebase の CI/CD

Next.js を Vercel にデプロイする場合は、Vercel の Git 連携が最もシンプルです。

### Vercel の設定

```
Vercel ダッシュボード → プロジェクト → Settings → Environment Variables

本番（Production）:
  NEXT_PUBLIC_FIREBASE_PROJECT_ID = my-app-prd
  NEXT_PUBLIC_FIREBASE_API_KEY    = AIza-prd-xxxx
  FIREBASE_ADMIN_PROJECT_ID       = my-app-prd
  FIREBASE_ADMIN_CLIENT_EMAIL     = firebase-adminsdk@my-app-prd.iam.gserviceaccount.com
  FIREBASE_ADMIN_PRIVATE_KEY      = -----BEGIN PRIVATE KEY-----\n...

ステージング（Preview）:
  NEXT_PUBLIC_FIREBASE_PROJECT_ID = my-app-stg
  ...（stg 用の値）

開発（Development）:
  NEXT_PUBLIC_FIREBASE_PROJECT_ID = my-app-dev
  NEXT_PUBLIC_USE_FIREBASE_EMULATOR = true
```

### Vercel + Firebase のデプロイフロー

```
1. PR 作成（feature/* → develop）
   → Vercel がプレビューデプロイを自動作成
   → GitHub Actions でテスト実行

2. develop にマージ
   → Vercel が stg ブランチのプレビューをデプロイ
   → Firebase の stg プロジェクトにルール・Functions をデプロイ

3. main にマージ（本番リリース）
   → Vercel が本番デプロイ
   → Firebase の prd プロジェクトにデプロイ
```

### Vercel と Firebase Functions の組み合わせ

```yaml
# .github/workflows/deploy-firebase-only.yml
# Vercel が Next.js を担当するため、Firebase リソースのみデプロイ
name: Deploy Firebase Resources

on:
  push:
    branches: [main]
    paths:
      - 'firestore.rules'
      - 'storage.rules'
      - 'firestore.indexes.json'
      - 'functions/**'

jobs:
  deploy-firebase:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '20', cache: 'npm' }
      - run: npm install -g firebase-tools
      - run: npm ci --prefix functions
      - run: |
          firebase deploy \
            --only firestore,storage,functions \
            --project ${{ secrets.PRD_FIREBASE_PROJECT_ID }}
        env:
          FIREBASE_TOKEN: ${{ secrets.FIREBASE_CI_TOKEN }}
```

---

## 6. Cloud Functions の CI/CD

```yaml
# .github/workflows/deploy-functions.yml
name: Deploy Cloud Functions

on:
  push:
    branches: [main]
    paths: ['functions/**']  # functions フォルダ変更時のみ実行

jobs:
  test-and-deploy:
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: functions

    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '20', cache: 'npm', cache-dependency-path: 'functions/package-lock.json' }
      - uses: actions/setup-java@v4
        with: { distribution: 'temurin', java-version: '17' }

      - run: npm ci

      - name: TypeScript のビルド確認
        run: npm run build

      - name: Lint チェック
        run: npm run lint

      - name: Functions のユニットテスト
        run: npm test

      - name: 本番 Functions をデプロイ
        working-directory: .
        run: |
          npm install -g firebase-tools
          firebase deploy --only functions --project ${{ secrets.PRD_FIREBASE_PROJECT_ID }}
        env:
          FIREBASE_TOKEN: ${{ secrets.FIREBASE_CI_TOKEN }}
```

---

## 7. プレビューチャンネルを使ったレビュー環境

Firebase Hosting のプレビューチャンネルを使うと、PR ごとに一時 URL を自動作成できます。

```yaml
# .github/workflows/preview.yml
name: PR Preview

on:
  pull_request:
    branches: [main, develop]

jobs:
  preview:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '20', cache: 'npm' }
      - run: npm ci
      - run: npm run build
        env:
          NEXT_PUBLIC_FIREBASE_PROJECT_ID: ${{ secrets.DEV_FIREBASE_PROJECT_ID }}
          NEXT_PUBLIC_FIREBASE_API_KEY:    ${{ secrets.DEV_FIREBASE_API_KEY }}
          # ...

      - name: プレビューチャンネルにデプロイ
        uses: FirebaseExtended/action-hosting-deploy@v0
        with:
          repoToken:       ${{ secrets.GITHUB_TOKEN }}
          firebaseServiceAccount: ${{ secrets.DEV_FIREBASE_SERVICE_ACCOUNT }}
          projectId:       ${{ secrets.DEV_FIREBASE_PROJECT_ID }}
          # channelId を省略すると PR 番号ベースの一時チャンネルが自動作成される
          expires: 7d  # 7 日後に自動削除
```

PR に自動でプレビュー URL がコメントされます：

```
🚀 Deploy Preview for my-app ready!
✅ Preview URL: https://my-app--pr-42-abc12345.web.app
📋 Expires: 2024-01-22 10:00 UTC
```

---

## 8. デプロイ通知とロールバック

### Slack 通知

```yaml
- name: デプロイ成功通知
  if: success()
  uses: slackapi/slack-github-action@v1
  with:
    channel-id: '#deploys'
    slack-message: |
      ✅ *本番デプロイ完了*
      コミット: ${{ github.sha }}
      作業者: ${{ github.actor }}
      URL: https://my-app.web.app
  env:
    SLACK_BOT_TOKEN: ${{ secrets.SLACK_BOT_TOKEN }}

- name: デプロイ失敗通知
  if: failure()
  uses: slackapi/slack-github-action@v1
  with:
    channel-id: '#deploys'
    slack-message: |
      ❌ *本番デプロイ失敗*
      コミット: ${{ github.sha }}
      ログ: ${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}
  env:
    SLACK_BOT_TOKEN: ${{ secrets.SLACK_BOT_TOKEN }}
```

### ロールバック

```bash
# Hosting のロールバック（Firebase コンソール または CLI）
# コンソール: Hosting → リリース履歴 → 対象バージョンの「ロールバック」

# CLI でのロールバック
firebase hosting:releases:list          # リリース一覧を確認
firebase hosting:rollback               # 直前のバージョンに戻す

# Cloud Functions のロールバック
# → 過去のコミットに revert して再デプロイするのが基本
git revert <commit-hash>
git push origin main
```

---

## まとめ

| 項目 | 推奨設定 |
|------|---------|
| 環境分離 | Firebase プロジェクトを dev / stg / prd で分ける |
| ブランチ戦略 | feature → develop（stg）→ main（prd） |
| 本番デプロイ | 必ずテスト通過後・手動承認（GitHub Environments）を推奨 |
| 環境変数 | GitHub Secrets または Vercel Environment Variables に格納 |
| プレビュー | PR ごとに Firebase Hosting のプレビューチャンネルを自動作成 |
| ロールバック | Hosting はコンソールから即時・Functions は revert & 再デプロイ |

---

## 次のステップ

- [パフォーマンス最適化ガイド](18_パフォーマンス最適化ガイド.md) — デプロイ後の速度改善
- [テスト戦略ガイド](16_テスト戦略ガイド.md) — CI に組み込むテストの整備
