# 13. デプロイ・CI/CD ガイド

> **レベル**: ★★★★☆（上級）  
> **前提知識**: [07_マイグレーション管理](07_マイグレーション管理.md)・[12_テストガイド](12_テストガイド.md) の完了  
> **所要時間**: 約 60 分

---

## 📚 目次

1. [デプロイ全体の流れ](#1-デプロイ全体の流れ)
2. [環境の分離（開発・ステージング・本番）](#2-環境の分離開発ステージング本番)
3. [Supabase CLI によるマイグレーションデプロイ](#3-supabase-cli-によるマイグレーションデプロイ)
4. [GitHub Actions CI/CD パイプライン](#4-github-actions-cicd-パイプライン)
5. [Edge Functions のデプロイ](#5-edge-functions-のデプロイ)
6. [環境変数・シークレット管理](#6-環境変数シークレット管理)
7. [フロントエンドのデプロイ（Vercel / Cloudflare Pages）](#7-フロントエンドのデプロイvercel--cloudflare-pages)
8. [ロールバック手順](#8-ロールバック手順)
9. [デプロイチェックリスト](#9-デプロイチェックリスト)

---

## 1. デプロイ全体の流れ

```
Git Push / PR Merge
        │
        ▼
┌───────────────────┐
│  CI: テスト実行    │  ← pgTAP + Vitest + lint
└────────┬──────────┘
         │ 成功
         ▼
┌───────────────────┐
│  DB マイグレーション│  ← supabase db push
│  をデプロイ        │
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│  Edge Functions   │  ← supabase functions deploy
│  をデプロイ        │
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│  フロントエンドを  │  ← Vercel / Cloudflare Pages
│  デプロイ          │
└───────────────────┘
```

**重要な原則**: DB マイグレーション → Functions → フロントエンドの順番を守る  
（フロントエンドが先にデプロイされると、新しいカラムを参照するコードが古い DB スキーマで動いてしまう）

---

## 2. 環境の分離（開発・ステージング・本番）

### 環境別 Supabase プロジェクトを作成する

| 環境 | Supabase プロジェクト | ブランチ | 用途 |
|------|---------------------|---------|------|
| **ローカル** | supabase start（Docker）| feature/* | 開発・テスト |
| **ステージング** | staging-myapp | develop | QA・受け入れテスト |
| **本番** | prod-myapp | main | エンドユーザー向け |

### supabase/config.toml の設定

```toml
# supabase/config.toml

[api]
port = 54321

[db]
port = 54322
major_version = 15

[studio]
port = 54323

[auth]
site_url = "http://localhost:3000"
additional_redirect_urls = ["http://localhost:3000/**"]

[auth.email]
enable_signup = true
double_confirm_changes = true
```

### プロジェクト ID の管理

```bash
# ローカルプロジェクトをリモートの Supabase プロジェクトと紐づける
supabase link --project-ref <PROJECT_REF>

# 接続確認
supabase status --linked
```

---

## 3. Supabase CLI によるマイグレーションデプロイ

### ローカルで新しいマイグレーションを作成

```bash
# マイグレーションファイルを作成
supabase migration new add_comments_table

# ファイルが生成される
# supabase/migrations/20260301120000_add_comments_table.sql
```

```sql
-- supabase/migrations/20260301120000_add_comments_table.sql

CREATE TABLE comments (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  post_id     UUID NOT NULL REFERENCES posts(id) ON DELETE CASCADE,
  user_id     UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  content     TEXT NOT NULL CHECK (char_length(content) > 0 AND char_length(content) <= 1000),
  created_at  TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- インデックス
CREATE INDEX idx_comments_post_id ON comments(post_id);
CREATE INDEX idx_comments_user_id ON comments(user_id);

-- RLS を有効化
ALTER TABLE comments ENABLE ROW LEVEL SECURITY;

-- ポリシー
CREATE POLICY "認証ユーザーは全コメントを閲覧できる"
  ON comments FOR SELECT
  TO authenticated
  USING (true);

CREATE POLICY "自分のコメントのみ投稿できる"
  ON comments FOR INSERT
  TO authenticated
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "自分のコメントのみ削除できる"
  ON comments FOR DELETE
  TO authenticated
  USING (auth.uid() = user_id);
```

### ローカルで動作確認

```bash
# ローカル DB にマイグレーションを適用
supabase db reset

# テストを実行
supabase test db

# 問題なければ本番へデプロイ
supabase db push
```

### 本番への適用コマンド

```bash
# 未適用のマイグレーションを本番 DB に適用
supabase db push

# ドライラン（適用内容を確認するだけ）
supabase db push --dry-run

# 適用済みマイグレーションの確認
supabase migration list
```

---

## 4. GitHub Actions CI/CD パイプライン

### 全体パイプライン（完全版）

```yaml
# .github/workflows/deploy.yml

name: Test and Deploy

on:
  push:
    branches:
      - main       # → 本番デプロイ
      - develop    # → ステージングデプロイ
  pull_request:
    branches: [main, develop]

jobs:
  # ─────────────────────────────────────────
  # JOB 1: テスト
  # ─────────────────────────────────────────
  test:
    name: テスト実行
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Supabase CLI をセットアップ
        uses: supabase/setup-cli@v1
        with:
          version: latest

      - name: ローカル Supabase を起動
        run: supabase start

      - name: DB テスト（pgTAP）を実行
        run: supabase test db

      - name: Node.js をセットアップ
        uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: "npm"

      - name: 依存関係をインストール
        run: npm ci

      - name: 環境変数をセット
        run: |
          STATUS=$(supabase status --output json)
          echo "NEXT_PUBLIC_SUPABASE_URL=http://localhost:54321" >> $GITHUB_ENV
          echo "NEXT_PUBLIC_SUPABASE_ANON_KEY=$(echo $STATUS | jq -r '.ANON_KEY')" >> $GITHUB_ENV
          echo "SUPABASE_SERVICE_ROLE_KEY=$(echo $STATUS | jq -r '.SERVICE_ROLE_KEY')" >> $GITHUB_ENV

      - name: 型チェック
        run: npm run type-check

      - name: Lint
        run: npm run lint

      - name: Vitest テスト
        run: npm run test

      - name: Supabase を停止
        if: always()
        run: supabase stop

  # ─────────────────────────────────────────
  # JOB 2: ステージングデプロイ
  # ─────────────────────────────────────────
  deploy-staging:
    name: ステージングデプロイ
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/develop'
    environment: staging

    steps:
      - uses: actions/checkout@v4

      - name: Supabase CLI をセットアップ
        uses: supabase/setup-cli@v1
        with:
          version: latest

      - name: ステージング DB に接続
        run: supabase link --project-ref ${{ secrets.STAGING_PROJECT_REF }}
        env:
          SUPABASE_ACCESS_TOKEN: ${{ secrets.SUPABASE_ACCESS_TOKEN }}

      - name: DB マイグレーションを適用（ドライラン）
        run: supabase db push --dry-run

      - name: DB マイグレーションを適用
        run: supabase db push
        env:
          SUPABASE_ACCESS_TOKEN: ${{ secrets.SUPABASE_ACCESS_TOKEN }}

      - name: Edge Functions をデプロイ
        run: supabase functions deploy --project-ref ${{ secrets.STAGING_PROJECT_REF }}
        env:
          SUPABASE_ACCESS_TOKEN: ${{ secrets.SUPABASE_ACCESS_TOKEN }}

  # ─────────────────────────────────────────
  # JOB 3: 本番デプロイ
  # ─────────────────────────────────────────
  deploy-production:
    name: 本番デプロイ
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    environment: production  # 承認フロー付き

    steps:
      - uses: actions/checkout@v4

      - name: Supabase CLI をセットアップ
        uses: supabase/setup-cli@v1
        with:
          version: latest

      - name: 本番 DB に接続
        run: supabase link --project-ref ${{ secrets.PRODUCTION_PROJECT_REF }}
        env:
          SUPABASE_ACCESS_TOKEN: ${{ secrets.SUPABASE_ACCESS_TOKEN }}

      - name: DB マイグレーションをドライラン確認
        run: supabase db push --dry-run

      - name: DB マイグレーションを適用
        run: supabase db push
        env:
          SUPABASE_ACCESS_TOKEN: ${{ secrets.SUPABASE_ACCESS_TOKEN }}

      - name: Edge Functions をデプロイ
        run: supabase functions deploy --project-ref ${{ secrets.PRODUCTION_PROJECT_REF }}
        env:
          SUPABASE_ACCESS_TOKEN: ${{ secrets.SUPABASE_ACCESS_TOKEN }}

      - name: デプロイ完了を Slack に通知
        uses: slackapi/slack-github-action@v1.26.0
        with:
          payload: |
            {
              "text": "✅ 本番デプロイ完了: ${{ github.repository }} @ ${{ github.sha }}"
            }
        env:
          SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}
```

### PR ごとのプレビュー環境（Supabase Branching）

Supabase Pro プラン以上では、**Supabase Branching** を使い PR ごとに専用 DB を自動作成できます。

```yaml
# .github/workflows/preview.yml

name: Preview Environment

on:
  pull_request:
    types: [opened, synchronize, reopened]

jobs:
  create-preview:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Supabase Branching でプレビュー DB を作成
        uses: supabase/preview-branch-action@v1
        with:
          supabase-project-ref: ${{ secrets.PRODUCTION_PROJECT_REF }}
          supabase-access-token: ${{ secrets.SUPABASE_ACCESS_TOKEN }}

      # Vercel のプレビューデプロイに DB URL を渡す
      - name: Vercel プレビューデプロイ
        uses: amondnet/vercel-action@v20
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
```

---

## 5. Edge Functions のデプロイ

### 単一の関数をデプロイ

```bash
# 特定の関数をデプロイ
supabase functions deploy send-email --project-ref <PROJECT_REF>

# すべての関数をデプロイ
supabase functions deploy --project-ref <PROJECT_REF>

# デプロイ済み関数の一覧
supabase functions list --project-ref <PROJECT_REF>
```

### 関数への環境変数（シークレット）設定

```bash
# シークレットを設定
supabase secrets set RESEND_API_KEY=your_api_key --project-ref <PROJECT_REF>

# 複数まとめて設定（.env ファイルから）
supabase secrets set --env-file .env.production --project-ref <PROJECT_REF>

# 設定済みシークレットの確認
supabase secrets list --project-ref <PROJECT_REF>
```

---

## 6. 環境変数・シークレット管理

### GitHub Actions Secrets の設定

| シークレット名 | 値 | 用途 |
|--------------|---|------|
| `SUPABASE_ACCESS_TOKEN` | Supabase の Personal Access Token | CLI 認証 |
| `STAGING_PROJECT_REF` | ステージングプロジェクトの ref ID | ステージングへの接続 |
| `PRODUCTION_PROJECT_REF` | 本番プロジェクトの ref ID | 本番への接続 |
| `NEXT_PUBLIC_SUPABASE_URL` | Supabase の API URL | フロントエンド |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | anon キー | フロントエンド |
| `SLACK_WEBHOOK_URL` | Slack の Webhook URL | 通知 |

### アクセストークンの取得方法

1. [Supabase ダッシュボード](https://supabase.com/dashboard) → アカウントアイコン
2. **Account Settings** → **Access Tokens**
3. **Generate new token** をクリック
4. 生成されたトークンを GitHub Secrets に設定

### 環境ファイルの管理

```
.env.local           ← Git 管理外（個人開発用）
.env.test.local      ← Git 管理外（テスト用）
.env.example         ← Git 管理対象（値なし、キーのみ）
```

```bash
# .env.example
NEXT_PUBLIC_SUPABASE_URL=
NEXT_PUBLIC_SUPABASE_ANON_KEY=
SUPABASE_SERVICE_ROLE_KEY=
DATABASE_URL=
```

---

## 7. フロントエンドのデプロイ（Vercel / Cloudflare Pages）

### Vercel の場合

```yaml
# GitHub Actions から Vercel にデプロイ

- name: Vercel へデプロイ（本番）
  uses: amondnet/vercel-action@v20
  with:
    vercel-token: ${{ secrets.VERCEL_TOKEN }}
    vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
    vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
    vercel-args: "--prod"
```

Vercel のダッシュボードで以下の環境変数を設定：

| 変数名 | Environment |
|--------|------------|
| `NEXT_PUBLIC_SUPABASE_URL` | Production / Preview |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | Production / Preview |

### Cloudflare Pages の場合

```yaml
- name: Cloudflare Pages へデプロイ
  uses: cloudflare/pages-action@v1
  with:
    apiToken: ${{ secrets.CLOUDFLARE_API_TOKEN }}
    accountId: ${{ secrets.CLOUDFLARE_ACCOUNT_ID }}
    projectName: my-app
    directory: .next  # Next.js のビルド出力
    gitHubToken: ${{ secrets.GITHUB_TOKEN }}
```

---

## 8. ロールバック手順

### DB マイグレーションのロールバック

Supabase の `db push` はロールバックを自動サポートしていません。**必ず元に戻す SQL を別ファイルとして作成します**。

```bash
# 新しいロールバック用マイグレーションを作成
supabase migration new revert_add_comments_table
```

```sql
-- supabase/migrations/20260302000000_revert_add_comments_table.sql

-- コメントテーブルを削除（前のマイグレーションで作ったものを元に戻す）
DROP TABLE IF EXISTS comments;
```

```bash
# ロールバックを本番に適用
supabase db push
```

### Edge Functions のロールバック

```bash
# 以前のコミットをチェックアウトして再デプロイ
git checkout <前のコミット SHA> -- supabase/functions/send-email/
supabase functions deploy send-email --project-ref <PROJECT_REF>
```

### フロントエンドのロールバック

Vercel では GUI から過去のデプロイを**即座に本番へ昇格**できます。

```
Vercel ダッシュボード → Deployments → 過去のデプロイ → Promote to Production
```

---

## 9. デプロイチェックリスト

### 本番デプロイ前

- [ ] `supabase test db` がすべてグリーン
- [ ] `npm run test` がすべてグリーン
- [ ] `supabase db push --dry-run` で差分を確認
- [ ] 破壊的変更（カラム削除・型変更）がないか確認
- [ ] 本番の DB バックアップが取得済み（Supabase ダッシュボード → Database → Backups）

### 本番デプロイ後

- [ ] `supabase migration list` で全マイグレーションが Applied になっているか確認
- [ ] 本番の主要ページが正常に動作するか確認（スモークテスト）
- [ ] エラーログ（Supabase ダッシュボード → Logs）に異常がないか確認
- [ ] アラートが発火していないか確認

---

## まとめ

```
開発フロー:
  feature branch → supabase start → コード実装 → supabase test db → PR

CI フロー（PR 時）:
  push → テスト（pgTAP + Vitest）→ 成功 → PR マージ可能

CD フロー（develop ブランチ）:
  merge → テスト → DB push（staging）→ Functions deploy（staging）

CD フロー（main ブランチ）:
  merge → テスト → 承認 → DB push（production）→ Functions deploy（production）→ Vercel deploy
```

---

**次のステップ**: [14_パフォーマンスガイド](14_パフォーマンスガイド.md) でクエリ最適化・スケーリングを学ぶ
