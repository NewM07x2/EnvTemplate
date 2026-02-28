# .github テンプレート カスタマイズガイド

このフォルダは **next-python** プロジェクト向けに設計された AI 支援開発ガイドセンターです。

他のプロジェクトに横展開する際は、以下のガイドに従ってカスタマイズしてください。

---

## 📋 カスタマイズが必要なファイル

### 1. **steering/structure.md** — アーキテクチャ定義

**修正内容:**
- セクション 1「プロジェクト構成」を自分のプロジェクトに合わせて修正
  - フレームワーク（Next.js / React / Vue / Flutter など）
  - バックエンド構成（FastAPI / Node.js / Python など）
  - データベース（PostgreSQL / MongoDB / Supabase など）
  - キャッシュ・ローカルDB など

**例:**
```markdown
# 1. プロジェクト構成

本リポジトリは以下の構成となる：

- **フロントエンド:** Next.js 14 + TypeScript (`web/`)
- **バックエンド API:** Express.js + Node.js (`api/`)
- **データベース:** PostgreSQL (`migrations/`)
- **キャッシュ:** Redis
```

### 2. **steering/workflow.md** — 開発フロー

**修正内容:**
- セクション 2「修正順序」を修正
  - プロジェクトの層構造に合わせて修正順序を定義
  - DB 変更時のステップを具体的に記述

**例:**
```markdown
### DB変更がある場合:

1. `migrations/` で PostgreSQL スキーマ修正
2. `api/src/models/` で Entity/Model 更新
3. `api/src/repositories/` で Repository 更新
4. `api/src/services/` でビジネスロジック更新
5. `web/src/pages/` で UI 更新
```

### 3. **steering/commit-messages.md** — コミット規約

**修正内容:**
- セクション 1.2「Scope（スコープ）」を修正
  - プロジェクトに固有のモジュール・レイヤをリストアップ
  - フロントエンド・バックエンド・インフラ等の分類をカスタマイズ

**例:**
```markdown
**フロントエンド（Next.js）:**
- `page` — ページ・Route コンポーネント変更
- `component` — コンポーネント変更
- `hook` — カスタムフック変更
- `store` — Zustand / Redux ストア変更

**バックエンド（Express.js）:**
- `route` — ルート定義変更
- `middleware` — ミドルウェア変更
- `controller` — コントローラー変更
```

### 4. **copilot-instructions.md** — Copilot 指示

**修正内容:**
- 「優先参照ファイル」セクションを修正
  - `steering/paths.md`, `steering/guardrails.md` などが存在しない場合は削除
  - プロジェクトに必要なファイルのみをリストアップ

**例:**
```markdown
優先参照ファイル：
1. `steering/structure.md`  — レイヤ構造・依存制約
2. `steering/workflow.md`   — 必須プロセス
3. `steering/commit-messages.md` — コミット規約
```

### 5. **agents/*.agent.md** — AI エージェント定義

**修正内容:**
- 各エージェントファイル内の「具体的なパス参照」をカスタマイズ
  - ディレクトリパス（`app/lib/`, `api/`, `web/src/` など）
  - ファイル拡張子（`.dart`, `.py`, `.ts` など）
  - 特定フレームワークの参照

**例：architect.agent.md**
```markdown
# 修正前（Flutter 向け）
位置: `features/[feature]/presentation/`

# 修正後（Next.js 向け）
位置: `pages/`, `components/`
```

---

## ✅ カスタマイズチェックリスト

新しいプロジェクトに適用する際、以下をチェックしてください：

- [ ] `steering/structure.md` のプロジェクト構成セクションを修正
- [ ] `steering/workflow.md` の修正順序を修正
- [ ] `steering/commit-messages.md` の Scope を修正
- [ ] `copilot-instructions.md` の優先参照ファイルを修正
- [ ] 各 `agents/` ファイルのパス参照を修正
- [ ] プロジェクトに不要なファイルは削除（例：`workflows/flutter-ci.yml`）
- [ ] プロジェクトに必要な新しいワークフローを追加

---

## 📁 削除・追加候補

### 削除すべきファイル（プロジェクト固有）
- `workflows/flutter-ci.yml` — Flutter CI 専用。別の技術スタック用に置き換え
- アジェント定義で Flutter 特有の部分

### 追加すべきファイル（プロジェクト固有）
- `steering/guardrails.md` — プロジェクト固有の禁止事項
- `steering/paths.md` — パッケージ・モジュール定義
- 新しい GitHub Actions ワークフロー

---

## 🚀 カスタマイズ例：React + Django プロジェクト

### 必要な修正

**1. steering/structure.md**
```markdown
# 1. プロジェクト構成
- **フロントエンド:** React 18 + TypeScript (`frontend/`)
- **バックエンド API:** Django REST Framework (`backend/`)
- **データベース:** PostgreSQL (`migrations/`)
```

**2. steering/workflow.md**
```markdown
### DB変更がある場合:
1. `backend/migrations/` で Django マイグレーション作成
2. `backend/models.py` で モデル更新
3. `backend/serializers.py` で シリアライザー更新
4. `backend/views.py` で API エンドポイント更新
5. `frontend/hooks/` で カスタムフック更新
6. `frontend/pages/` で UI 更新
```

**3. steering/commit-messages.md**
```markdown
**フロントエンド（React）:**
- `component` — コンポーネント変更
- `hook` — カスタムフック変更
- `page` — ページコンポーネント変更

**バックエンド（Django）:**
- `model` — Django モデル変更
- `migration` — マイグレーション変更
- `api` — API エンドポイント変更
```

---

## 🆘 サポート

カスタマイズに関する質問や問題がある場合：

1. 各ファイルの先頭に記載された「テンプレート利用者へ」を確認
2. `steering/` フォルダ内の説明セクションを再度読む
3. プロジェクト固有の用語・パスに置き換える

---

**このテンプレートが複数のプロジェクトで再利用可能な AI 支援開発基盤となることを目指しています。**
