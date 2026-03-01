# Vercel 環境設定・CI-CD

> **対象者**: 本番環境・ステージング環境を構築したい開発者  
> **主要トピック**: 環境変数 / Secrets 管理 / GitHub Actions / デプロイメント自動化

---

## 📚 目次

1. [環境変数の基礎](#1-環境変数の基礎)
2. [環境別設定（Development / Preview / Production）](#2-環境別設定)
3. [Secrets 管理](#3-secrets-管理)
4. [GitHub Actions との連携](#4-github-actions-との連携)
5. [自動デプロイメント](#5-自動デプロイメント)
6. [Webhook による自動トリガー](#6-webhook-による自動トリガー)
7. [ロールバック・ホットフィックス](#7-ロールバックホットフィックス)
8. [監視・アラート](#8-監視アラート)
9. [トラブルシューティング](#9-トラブルシューティング)

---

## 1. 環境変数の基礎

### 1.1 環境変数の種類

Vercel では **3つの環境** でそれぞれ異なる環境変数を設定できます。

| 環境 | 説明 | 用途 |
|---|---|---|
| **Development** | `vercel dev` で実行 | ローカル開発 |
| **Preview** | PR・ブランチ別デプロイ | 検証・テスト |
| **Production** | main ブランチ本番環境 | 本番サービス |

### 1.2 CLI での環境変数設定

```bash
# 全環境に設定
vercel env add MY_VAR

# 特定環境のみ
vercel env add MY_VAR --environment=production

# 確認
vercel env list

# 削除
vercel env rm MY_VAR
```

### 1.3 Vercel ダッシュボード UI での設定

```
Settings > Environment Variables
```

手動で以下を入力：
- **Variable name**: `MY_VAR`
- **Value**: `my-value`
- **Environments**: `Production`, `Preview`, `Development` から選択

---

## 2. 環境別設定

### 2.1 開発環境 (Development)

```bash
# .env.local (git 管理から除外)
DATABASE_URL=postgresql://localhost:5432/dev_db
API_SECRET=dev-secret-key
DEBUG=true
```

`vercel dev` で自動読み込み。

### 2.2 プレビュー環境 (Preview)

PR・デプロイプレビューで使う環境変数。

**Vercel ダッシュボード設定:**

```
Settings > Environment Variables

Variable: API_URL
Value: https://staging-api.example.com
Environments: Preview
```

### 2.3 本番環境 (Production)

**Vercel ダッシュボード設定:**

```
Settings > Environment Variables

Variable: API_URL
Value: https://api.example.com
Environments: Production
```

### 2.4 環境別 .env ファイルの使い分け

```
.env.local              # ローカル開発（git 除外）
.env.development        # development 環境（git 除外）
.env.preview            # preview 環境（オプション）
.env.production         # production 環境（オプション）
.env.example            # テンプレート（git 管理）✅
```

```bash
# .env.example (リポジトリに含める)
DATABASE_URL=postgresql://localhost:5432/dev_db
API_SECRET=your-secret-here
DEBUG=false
```

### 2.5 フレームワーク別アクセス方法

#### Next.js

```javascript
// 全環境で利用可能
const apiUrl = process.env.API_URL;

// クライアント側で利用する場合は NEXT_PUBLIC_ プレフィックス
const publicUrl = process.env.NEXT_PUBLIC_API_URL;
```

#### React / Vite

```javascript
// React App
const secret = process.env.REACT_APP_MY_VAR;

// Vite
const secret = import.meta.env.VITE_MY_VAR;
```

#### Nuxt / SvelteKit / Astro

```javascript
// Nuxt
const secret = process.env.NUXT_PUBLIC_VAR;

// SvelteKit
const secret = process.env.PUBLIC_VAR;

// Astro
const secret = process.env.PUBLIC_VAR;
```

---

## 3. Secrets 管理

### 3.1 Secrets と環境変数の違い

| | 環境変数 | Secrets |
|---|---|---|
| **暗号化** | 不要 | 自動暗号化 ✅ |
| **管理画面** | 表示 | 一度登録後は表示不可 |
| **ビルド時** | 内容が見える | ビルドログに出ない |
| **用途** | 設定値全般 | パスワード・API キー |

### 3.2 CLI でのシークレット設定

```bash
# セキュアに設定（入力時はマスク）
vercel env add DATABASE_PASSWORD --environment=production

# または一行で設定
echo "my-secret-password" | vercel env add DATABASE_PASSWORD

# Vercel secrets コマンド（代替）
vercel secrets add DATABASE_PASSWORD "my-secret-password"
```

### 3.3 ダッシュボード UI での設定

```
Settings > Environment Variables > 値入力欄で「Encrypt」チェック
```

### 3.4 シークレット利用時の注意

```javascript
// ✅ サーバーサイドでのみ使用
export async function getServerSideProps(context) {
  const dbPassword = process.env.DATABASE_PASSWORD;
  // database 接続処理
}

// ❌ クライアント側では使用禁止（ビルド時にコンパイル）
// 絶対に以下のようにしない：
const secret = process.env.DATABASE_PASSWORD;
console.log(secret); // ブラウザに晒される！
```

### 3.5 .env ファイルから一括インポート

```bash
# セキュアな secrets.env ファイルから一括登録
# (ローカルのみ、git 除外)
cat secrets.env | while IFS='=' read -r key value; do
  vercel env add $key "$value" --environment=production
done
```

---

## 4. GitHub Actions との連携

### 4.1 Vercel トークン取得

```
Settings > Tokens > Create Token
```

トークン名: `VERCEL_TOKEN`
トークンをコピー。

### 4.2 GitHub Secrets 設定

```
Repository > Settings > Secrets and variables > Actions > New repository secret
```

追加するシークレット：
- **VERCEL_TOKEN**: `[Vercel から取得]`
- **VERCEL_ORG_ID**: `[Vercel Settings > General から取得]`
- **VERCEL_PROJECT_ID**: `[Vercel Settings > General から取得]`

### 4.3 Vercel IDs 確認方法

```bash
# ローカルで実行
vercel project inspect

# 出力例
Project ID: prj_abcdef1234567890
Organization ID: team_xyz1234
```

---

## 5. 自動デプロイメント

### 5.1 GitHub Actions ワークフロー（基本）

```yaml
# .github/workflows/deploy.yml
name: Deploy to Vercel

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Install Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18'

      - name: Install dependencies
        run: npm ci

      - name: Build
        run: npm run build

      - name: Run tests
        run: npm test

      - name: Deploy to Vercel
        uses: vercel/action@v1
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
          production: ${{ github.ref == 'refs/heads/main' }}
```

### 5.2 環境別デプロイ（複数環境）

```yaml
# .github/workflows/deploy-multi-env.yml
name: Deploy to Vercel (Multi-Env)

on:
  push:
    branches:
      - main
      - staging
      - develop

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Setup Node
        uses: actions/setup-node@v3
        with:
          node-version: '18'

      - name: Install
        run: npm ci

      - name: Build
        run: npm run build

      - name: Deploy (Production)
        if: github.ref == 'refs/heads/main'
        run: |
          npm install -g vercel
          vercel --prod --token=${{ secrets.VERCEL_TOKEN }}

      - name: Deploy (Staging)
        if: github.ref == 'refs/heads/staging'
        run: |
          npm install -g vercel
          vercel --token=${{ secrets.VERCEL_TOKEN }}

      - name: Deploy (Development)
        if: github.ref == 'refs/heads/develop'
        run: |
          npm install -g vercel
          vercel --token=${{ secrets.VERCEL_TOKEN }}
```

### 5.3 デプロイ前にテスト実行

```yaml
# .github/workflows/deploy-with-tests.yml
name: Deploy with Tests

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - run: npm ci
      - run: npm run lint
      - run: npm test
      - run: npm run build

  deploy:
    needs: test  # test が成功したら実行
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: vercel/action@v1
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          production: true
```

---

## 6. Webhook による自動トリガー

### 6.1 Webhook URL 取得

```
Project Settings > Git Integrations > Deploy Hooks
```

下部の「Create Hook」でボタンをクリック。
- **Branch**: `main` または特定ブランチ
- **Hook 名**: 任意（例: `manual-trigger`）

表示される URL をコピー。

### 6.2 cURL での手動トリガー

```bash
# 本番環境へ即座にデプロイ
curl -X POST https://api.vercel.com/v1/integrations/deploy-hooks/...

# または
curl -X POST \
  https://api.vercel.com/v1/integrations/deploy-hooks/YOUR_HOOK_ID \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### 6.3 GitHub Actions からの呼び出し

```yaml
# .github/workflows/webhook-deploy.yml
name: Manual Webhook Deploy

on:
  workflow_dispatch:  # 手動実行

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Trigger Vercel Deployment
        run: |
          curl -X POST \
            https://api.vercel.com/v1/integrations/deploy-hooks/${{ secrets.VERCEL_DEPLOY_HOOK_ID }}
```

---

## 7. ロールバック・ホットフィックス

### 7.1 ダッシュボードからのロールバック

```
Project > Deployments > [ロールバック対象] > Promote to Production
```

### 7.2 CLI からのロールバック

```bash
# 本番環境を特定デプロイメントに変更
vercel promote [DEPLOYMENT_URL]

# 例
vercel promote my-app-abc123.vercel.app
```

### 7.3 デプロイメント履歴確認

```bash
# 最近のデプロイメント一覧
vercel list

# 詳細確認
vercel inspect [DEPLOYMENT_URL]
```

### 7.4 緊急ホットフィックス ワークフロー

```
1. hotfix ブランチを main から作成
   git checkout -b hotfix/urgent-fix

2. 修正を実装・コミット
   git commit -m "fix: urgent issue"

3. Pull Request を作成
   - タイトル: [HOTFIX] ...
   - プレビュー環境自動デプロイ

4. レビュー・マージ
   git checkout main
   git merge hotfix/urgent-fix

5. 本番環境に自動デプロイ ✅
```

---

## 8. 監視・アラート

### 8.1 デプロイメント通知設定

#### Slack 通知

```
Project Settings > Integrations > Slack > Connect
```

下記イベントを選択：
- Deployment created
- Deployment succeeded
- Deployment failed

#### メール通知

```
Account Settings > Email Notifications
```

- Deployment completed
- Deployment failed

### 8.2 監視メトリクス

Vercel ダッシュボード > **Analytics** タブ：

| メトリクス | 説明 |
|---|---|
| **Build time** | ビルド所要時間 |
| **Response time** | API 応答時間 |
| **Edge requests** | Edge Network リクエスト数 |
| **Serverless invocations** | サーバーレス関数呼び出し数 |

### 8.3 Core Web Vitals 監視

```
Project > Analytics > Web Vitals
```

- **LCP** (Largest Contentful Paint)
- **FID** (First Input Delay)
- **CLS** (Cumulative Layout Shift)

---

## 9. トラブルシューティング

### よくある問題

| 問題 | 原因 | 解決策 |
|---|---|---|
| 環境変数が反映されない | デプロイ後キャッシュ | `vercel env pull` で同期後 `vercel dev` 再起動 |
| GitHub Actions 失敗 | VERCEL_TOKEN 期限切れ | 新規トークン生成・更新 |
| シークレットが見える | クライアント側にコンパイル | サーバーサイドのみで使用 |
| ロールバック後も古い版 | CDN キャッシュ | `Settings > Caching > Clear All` |
| Webhook が実行されない | Hook URL 間違い | Deploy Hooks 再確認 |

### デバッグコマンド

```bash
# 環境変数を一覧表示
vercel env list

# 環境変数をローカルにプル
vercel env pull

# ビルドログを確認
vercel logs --follow

# デプロイメント詳細確認
vercel inspect [URL]

# 現在の設定確認
vercel project inspect
```

---

## 📖 関連ドキュメント

- [01_基本情報.md](./01_基本情報.md) — Vercel 概要
- [02_クイックスタート.md](./02_クイックスタート.md) — 基本セットアップ
- [03_フレームワーク別設定.md](./03_フレームワーク別設定.md) — フレームワーク設定
- [05_データベース連携.md](./05_データベース連携.md) — DB 設定
