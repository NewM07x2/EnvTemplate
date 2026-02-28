# GitHub Actions CI/CD 入門ガイド

> **対象者**: CI/CD を初めて設定する開発者  
> **所要時間**: 約 50 分

---

## 📚 目次

- [GitHub Actions CI/CD 入門ガイド](#github-actions-cicd-入門ガイド)
  - [📚 目次](#-目次)
  - [1. GitHub Actions とは](#1-github-actions-とは)
    - [なぜ必要か](#なぜ必要か)
  - [2. ワークフローの基本構造](#2-ワークフローの基本構造)
    - [主要な構成要素](#主要な構成要素)
  - [3. よく使うトリガー](#3-よく使うトリガー)
  - [4. 実践例①：テスト自動実行](#4-実践例テスト自動実行)
    - [Next.js + Vitest の場合](#nextjs--vitest-の場合)
    - [Python + pytest の場合](#python--pytest-の場合)
  - [5. 実践例②：型チェック + Lint + テスト](#5-実践例型チェック--lint--テスト)
  - [6. 実践例③：Docker ビルド + プッシュ](#6-実践例docker-ビルド--プッシュ)
  - [7. 実践例④：Prisma マイグレーション自動実行](#7-実践例prisma-マイグレーション自動実行)
  - [8. シークレット（環境変数）の管理](#8-シークレット環境変数の管理)
    - [Secrets の登録方法](#secrets-の登録方法)
    - [ワークフローでの使い方](#ワークフローでの使い方)
    - [Environments（環境別 Secrets）](#environments環境別-secrets)
  - [9. キャッシュで高速化](#9-キャッシュで高速化)
  - [10. よくあるエラーと対処法](#10-よくあるエラーと対処法)
    - [`Permission denied` エラー](#permission-denied-エラー)
    - [`secrets.GITHUB_TOKEN` が使えない](#secretsgithub_token-が使えない)
    - [ジョブが遅い](#ジョブが遅い)
    - [DB を使うテストが失敗する](#db-を使うテストが失敗する)
  - [📌 まとめ](#-まとめ)

---

## 1. GitHub Actions とは

**GitHub Actions** は、GitHub リポジトリ上で **CI/CD（継続的インテグレーション / 継続的デプロイ）** を自動化するサービスです。

```
開発フロー（GitHub Actions あり）:

開発者がコードを Push
    ↓
GitHub Actions が自動で実行
    ├── テストを実行 → 失敗したらマージ不可
    ├── 型チェック・Lint
    └── ビルド・デプロイ
    ↓
問題なければ本番環境に自動デプロイ ✅
```

### なぜ必要か

| 手動 | GitHub Actions |
|------|--------------|
| 「テスト忘れた」がある | すべての Push で自動実行 |
| 「自分の PC では動く」 | CI 環境で再現可能なテスト |
| デプロイ手順をミスる | 自動化でヒューマンエラーをゼロに |

---

## 2. ワークフローの基本構造

ワークフローは `.github/workflows/` ディレクトリに **YAML ファイル** で定義します。

```yaml
# .github/workflows/ci.yml

name: CI                          # ワークフローの名前（GitHub UI に表示される）

on:                               # トリガー（いつ実行するか）
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:                             # ジョブ（並列実行される処理の単位）
  test:                           # ジョブ名
    runs-on: ubuntu-latest        # 実行環境

    steps:                        # ステップ（ジョブ内の順番に実行される処理）
      - name: コードをチェックアウト
        uses: actions/checkout@v4  # 公式アクション（リポジトリのコードを取得）

      - name: Node.js のセットアップ
        uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: 依存関係をインストール
        run: npm ci                # コマンドを直接実行

      - name: テストを実行
        run: npm test
```

### 主要な構成要素

| 要素 | 説明 |
|------|------|
| `name` | ワークフロー・ジョブ・ステップの名前 |
| `on` | トリガー（push・PR・cron 等） |
| `jobs` | 並列実行される処理の単位 |
| `runs-on` | 実行環境（`ubuntu-latest` / `windows-latest` / `macos-latest`） |
| `steps` | ジョブ内の順番実行ステップ |
| `uses` | 公式・サードパーティアクションを使う |
| `run` | シェルコマンドを直接実行 |
| `with` | アクションへのパラメータ |
| `env` | 環境変数 |

---

## 3. よく使うトリガー

```yaml
on:
  # main ブランチへの Push 時
  push:
    branches: [main, develop]
    paths:                          # 特定パスの変更時のみ
      - 'src/**'
      - 'package.json'

  # PR 作成・更新時
  pull_request:
    branches: [main]

  # 手動実行（GitHub UI から実行ボタンが現れる）
  workflow_dispatch:
    inputs:
      environment:
        description: 'デプロイ先環境'
        required: true
        default: 'staging'

  # 定期実行（cron）
  schedule:
    - cron: '0 9 * * 1-5'  # 平日の朝 9 時（UTC）
```

---

## 4. 実践例①：テスト自動実行

### Next.js + Vitest の場合

```yaml
# .github/workflows/test.yml
name: Test

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'             # node_modules をキャッシュ

      - name: 依存関係をインストール
        run: npm ci

      - name: テストを実行
        run: npm run test
```

### Python + pytest の場合

```yaml
# .github/workflows/test-python.yml
name: Python Test

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
          cache: 'pip'

      - name: 依存関係をインストール
        run: pip install -r requirements.txt

      - name: テストを実行
        run: pytest tests/ -v
```

---

## 5. 実践例②：型チェック + Lint + テスト

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  lint-and-test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - run: npm ci

      # TypeScript 型チェック
      - name: 型チェック
        run: npx tsc --noEmit

      # ESLint
      - name: Lint
        run: npm run lint

      # テスト（カバレッジレポート付き）
      - name: テスト
        run: npm run test -- --coverage

      # カバレッジレポートを PR にコメント（オプション）
      - name: カバレッジをコメントに投稿
        uses: davelosert/vitest-coverage-report-action@v2
        if: github.event_name == 'pull_request'
```

---

## 6. 実践例③：Docker ビルド + プッシュ

```yaml
# .github/workflows/docker.yml
name: Docker Build & Push

on:
  push:
    branches: [main]
    tags:
      - 'v*'  # v1.0.0 のようなタグ Push 時

env:
  REGISTRY: ghcr.io                          # GitHub Container Registry
  IMAGE_NAME: ${{ github.repository }}       # owner/repo-name

jobs:
  build-push:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write                         # GHCR への Push 権限

    steps:
      - uses: actions/checkout@v4

      # Docker Buildx（マルチプラットフォームビルド）
      - uses: docker/setup-buildx-action@v3

      # GitHub Container Registry にログイン
      - name: GHCR にログイン
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}  # 自動提供されるトークン

      # イメージのタグを自動生成
      - name: メタデータを生成
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=ref,event=branch
            type=semver,pattern={{version}}
            type=sha,prefix=sha-

      # ビルドしてプッシュ
      - name: ビルド & プッシュ
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          cache-from: type=gha
          cache-to: type=gha,mode=max          # GitHub Actions キャッシュを使う
```

---

## 7. 実践例④：Prisma マイグレーション自動実行

```yaml
# .github/workflows/migrate.yml
name: DB Migration

on:
  push:
    branches: [main]
    paths:
      - 'prisma/migrations/**'  # マイグレーションファイルが変更された時だけ実行

jobs:
  migrate:
    runs-on: ubuntu-latest
    environment: production     # GitHub Environments で本番環境の承認フロー

    services:
      # テスト用 PostgreSQL を起動（本番は secrets を使う）
      postgres:
        image: postgres:16
        env:
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: testdb
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - run: npm ci

      - name: マイグレーションを実行
        run: npx prisma migrate deploy
        env:
          DATABASE_URL: ${{ secrets.DATABASE_URL }}
```

---

## 8. シークレット（環境変数）の管理

API キー・DB パスワードなどの機密情報は **Secrets** として管理します。

### Secrets の登録方法

1. GitHub リポジトリ → **Settings** → **Secrets and variables** → **Actions**
2. **New repository secret** をクリック
3. `Name`（例: `DATABASE_URL`）と `Value` を入力

### ワークフローでの使い方

```yaml
steps:
  - name: DB マイグレーション
    run: npx prisma migrate deploy
    env:
      DATABASE_URL: ${{ secrets.DATABASE_URL }}
      OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
```

### Environments（環境別 Secrets）

**staging** と **production** で異なる設定を管理できます。

1. **Settings** → **Environments** → **New environment**
2. 環境名（`staging` / `production`）を作成
3. 各環境に Secrets を登録

```yaml
jobs:
  deploy-staging:
    environment: staging          # staging 環境の Secrets を使う
    runs-on: ubuntu-latest
    steps:
      - run: echo ${{ secrets.DATABASE_URL }}  # staging の DB URL が展開される

  deploy-production:
    environment: production       # production 環境の Secrets を使う
    needs: deploy-staging         # staging 成功後に実行
```

---

## 9. キャッシュで高速化

```yaml
# Node.js の依存関係をキャッシュ
- uses: actions/setup-node@v4
  with:
    node-version: '20'
    cache: 'npm'      # package-lock.json を元にキャッシュ

# Python の依存関係をキャッシュ
- uses: actions/setup-python@v5
  with:
    python-version: '3.12'
    cache: 'pip'

# 手動でキャッシュを制御する場合
- uses: actions/cache@v4
  with:
    path: ~/.npm
    key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
    restore-keys: |
      ${{ runner.os }}-node-
```

---

## 10. よくあるエラーと対処法

### `Permission denied` エラー

```yaml
# パーミッションを明示的に設定
permissions:
  contents: read
  packages: write
  pull-requests: write
```

### `secrets.GITHUB_TOKEN` が使えない

```yaml
# 同じ名前で登録すると衝突する。別名で登録する
env:
  MY_TOKEN: ${{ secrets.MY_GITHUB_PAT }}
```

### ジョブが遅い

```yaml
# ジョブを並列実行する
jobs:
  typecheck:
    runs-on: ubuntu-latest
    steps: [...]

  lint:
    runs-on: ubuntu-latest       # typecheck と並列実行
    steps: [...]

  test:
    runs-on: ubuntu-latest
    needs: [typecheck, lint]     # 両方が成功してから実行
    steps: [...]
```

### DB を使うテストが失敗する

```yaml
# services でテスト用 DB を起動
services:
  postgres:
    image: postgres:16-alpine
    env:
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: test
    ports:
      - 5432:5432
    options: >-
      --health-cmd pg_isready
      --health-interval 10s
      --health-retries 5
```

---

## 📌 まとめ

```
.github/
└── workflows/
    ├── ci.yml        ← テスト・型チェック・Lint（PR 時）
    ├── docker.yml    ← Docker ビルド＆プッシュ（main Push 時）
    └── migrate.yml   ← DB マイグレーション（スキーマ変更時）
```

| よく使うアクション | 用途 |
|-----------------|------|
| `actions/checkout@v4` | リポジトリをチェックアウト |
| `actions/setup-node@v4` | Node.js をセットアップ（キャッシュ付き） |
| `actions/setup-python@v5` | Python をセットアップ |
| `docker/build-push-action@v5` | Docker イメージをビルド＆プッシュ |
| `actions/cache@v4` | 任意のファイルをキャッシュ |
