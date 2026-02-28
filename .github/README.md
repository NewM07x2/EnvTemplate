# `.github/` ディレクトリ — AI支援開発ガイドセンター

本リポジトリの AI 支援開発（GitHub Copilot / Agent mode）を円滑に進めるため、`.github/` フォルダは「開発ガイドのシングルソースオブトゥルース（SSOT）」として機能します。

新規参画者は、このフォルダの各ドキュメントを読むことで、プロジェクト構造・開発フロー・コミット規約などを理解できます。

---

## 📋 本フォルダの役割

`.github/` は以下の責務を持つ「開発ガイドセンター」です：

| フォルダ | 役割 | 対象者 |
|---------|------|--------|
| **steering/** | アーキテクチャ・開発フロー・コミット規約 | すべての開発者 |
| **agents/** | AI エージェント定義・責務分担 | AI支援開発を利用する者 |
| **prompts/** | 特定タスク用の LLM プロンプト | 高度なカスタマイズが必要な場合 |
| **skills/** | LLM の拡張スキル定義 | カスタマイズスキルの追加が必要な場合 |
| **tools/** | GitHub Actions 連携・ツール定義 | CI/CD・自動化に関わる者 |
| **workflows/** | GitHub Actions ワークフロー定義 | CI/CD・デプロイメント実行者 |

---

## 🎯 新規参画者チェックリスト

このプロジェクトに参画した際、以下の順で確認してください：

### Phase 1: アーキテクチャ理解（必須）

- [ ] **`steering/structure.md`** を読む
  - プロジェクト構成（Flutter + FastAPI + Supabase）
  - ディレクトリ構造
  - 層ごとの責務
  - 依存関係制約
  
- [ ] **`steering/workflow.md`** を読む
  - 開発ワークフロー（修正順序）
  - DB 変更時のステップ
  - テスト実装方針
  - プリチェックリスト

### Phase 2: コミット規約理解（必須）

- [ ] **`steering/commit-messages.md`** を読む
  - コミットメッセージ形式（Type/Scope/Subject）
  - 実装パターン別の例
  - コミット粒度ガイドライン

### Phase 3: AI 支援開発を使う場合（オプション）

- [ ] **`agents/`** フォルダで各エージェント定義を確認
  - どのエージェントにどの責務があるか
  - 各エージェントの使い分け

---

## 🗂️ 各ディレクトリの詳細

### `steering/` — アーキテクチャ定義（SSOT）

**このフォルダが最も重要です。**

開発時に参照すべき 3 つの文書が含まれます：

#### 1. **structure.md** — 正式アーキテクチャ定義
- ✅ プロジェクト構成：Flutter（フロント）+ FastAPI（API）+ Supabase（DB）+ Drift（ローカルDB）
- ✅ ディレクトリ構造：各レイヤの配置（Presentation / Business Logic / Data）
- ✅ 層ごとの責務：各層で「何ができるか」「何ができないか」
- ✅ 依存関係制約：レイヤ間の呼び出しルール
- ✅ Database 設計：Supabase PostgreSQL + Drift SQLite の使い分け
- ✅ パッケージ命名規約：Flutter と Python の両方

**読むべき人:** すべての開発者  
**確認タイミング:** 新規機能追加前、コードレビュー時

#### 2. **workflow.md** — 開発フロー・修正順序
- ✅ 必須の事前飛行チェック（修正前の確認事項）
- ✅ DB 変更を伴う場合の修正順序（9 ステップ）
- ✅ DB 変更なしの場合の修正順序（3 ステップ）
- ✅ API 側のみの変更フロー
- ✅ テスト実装方針
- ✅ 修正完了後のチェックリスト

**読むべき人:** 新規機能を実装する全開発者  
**確認タイミング:** タスク開始時、コミット前

#### 3. **commit-messages.md** — コミットメッセージ規約
- ✅ Type（feat / fix / refactor / test など）
- ✅ Scope（Flutter / API / Database など）
- ✅ Subject（命令形・日本語・50文字以内）
- ✅ Body（「なぜ」を記述）
- ✅ Footer（Breaking Changes / Issue references）
- ✅ 実装パターン別の例（DB 変更 / バグ修正 / 最適化 / テスト / リファクタリング）
- ✅ 禁止事項・コミット粒度ガイドライン

**読むべき人:** すべての開発者  
**確認タイミング:** コミット前に必ず確認

---

### `agents/` — AI エージェント定義

AI 支援開発（Copilot Agent mode）を利用する際に参照します。

各エージェントの責務分担：

| エージェント | 責務 | 使用場面 |
|-------------|------|---------|
| **@orchestrator** | ワークフロー調整・エージェント委譲 | 複数エージェント連携が必要なタスク |
| **@partner** | 設計判断・相談 | アーキテクチャ判断が必要な場合 |
| **@spec-refiner** | 仕様精錬・要件書作成 | 新規機能の仕様を詳細化したい場合 |
| **@analyst** | 影響調査・変更範囲分析 | 変更による影響を調べたい場合 |
| **@architect** | 実装執行 | 実装を開始したい場合 |
| **@governor** | 適合性監査 | 実装完了後の検証を実行したい場合 |
| **@reviewer** | コードレビュー | コード品質チェックが必要な場合 |
| **@curator** | ドキュメント整理 | ドキュメントを整理・更新したい場合 |

**各エージェント定義ファイル：** `agents/{agent-name}.agent.md`

---

### `prompts/` — カスタム LLM プロンプト

Copilot へ特定の指示を与えるカスタムプロンプト集です。

含まれるプロンプト：
- `update-copilot-customizations.prompt.md` — Copilot カスタマイズの更新方法
- `update-skill-creator.prompt.md` — スキルクリエーター機能の更新方法

**使用場面:** Copilot の動作を詳細にカスタマイズしたい場合

---

### `skills/` — LLM 拡張スキル定義

Copilot が利用可能な拡張スキルの定義です。

含まれるスキル：
- `schema-interpreter.skill.md` — スキーマ解釈スキル
- `custom-agents-creator/` — カスタムエージェント作成ツール
- `custom-instructions-creator/` — カスタム指示作成ツール
- `hooks-creator/` — GitHub Hooks 作成ツール
- `prompt-creator/` — プロンプト作成ツール
- `skill-creator/` — スキル作成ツール

**使用場面:** Copilot の機能を拡張したい場合

---

### `tools/` — ツール・ユーティリティ定義

GitHub Actions や開発ツール連携の定義が含まれます。

**使用場面:** CI/CD パイプラインやカスタムツールを追加したい場合

---

### `workflows/` — GitHub Actions ワークフロー

自動テスト・デプロイメント・品質チェックなどの自動実行フロー定義です。

**使用場面:** CI/CD を設定・変更したい場合

---

## 🚀 よくある作業フロー

### 新規機能を実装したい場合

```
1. steering/structure.md を読んで、機能を実装するべきレイヤを確認
2. steering/workflow.md で DB 変更の有無を判定
3. 修正順序に従って実装（DB → Data → Domain → Presentation）
4. steering/commit-messages.md に従ってコミット
```

### バグを修正したい場合

```
1. steering/structure.md で該当レイヤを確認
2. steering/workflow.md で修正順序を確認
3. 必要に応じて各レイヤを修正
4. steering/commit-messages.md で type: fix でコミット
```

### AI 支援開発を活用したい場合

```
1. agents/orchestrator.agent.md を確認
2. @orchestrator を呼び出して、タスクを説明
3. 必要に応じて他のエージェント（@architect など）に委譲
4. steering/ のドキュメントに従って実装が進行
```

---

## ⚠️ 重要ルール

### SSOT（Single Source of Truth）原則

**`steering/` フォルダ内の定義が絶対基準です。**

- 設計判断に迷ったら → `steering/structure.md`
- 実装フロー に迷ったら → `steering/workflow.md`
- コミット形式に迷ったら → `steering/commit-messages.md`

### AI のルール

Copilot（またはその他の LLM）は以下を優先します：

1. **steering/** の定義 > 一般的な正解
2. **既存パターン** > 新しいパターン
3. **安定性** > 最適化
4. **明示性** > 推測

---

## 📌 参考資料

### リポジトリ全体の構成

```
Poopoolab/
├── .github/              ← ここ！AI支援開発ガイドセンター
│   ├── steering/         — アーキテクチャ定義（SSOT）
│   ├── agents/           — AIエージェント定義
│   ├── prompts/          — カスタムプロンプト
│   ├── skills/           — 拡張スキル定義
│   ├── tools/            — ツール定義
│   └── workflows/        — GitHub Actions ワークフロー
│
├── app/                  ← Flutter フロントエンド
│   └── lib/
│       ├── core/         — 共有ロジック
│       ├── data/         — データ層（Repository / DataSource）
│       └── features/     — 機能（Presentation + Business Logic）
│
├── api/                  ← FastAPI バックエンド
│   └── app/
│       ├── api/          — REST エンドポイント
│       ├── graphql/      — GraphQL スキーマ・リゾルバー
│       ├── services/     — ビジネスロジック
│       └── repositories/ — DB アクセス層
│
└── supabase/             ← PostgreSQL + Migrations
    └── migrations/       — DB スキーマ定義
```

---

## 🆘 困ったときは

| 困りごと | 確認先 |
|---------|--------|
| アーキテクチャについて | `steering/structure.md` |
| 実装フローについて | `steering/workflow.md` |
| コミットメッセージについて | `steering/commit-messages.md` |
| AI エージェントについて | `agents/` フォルダ |
| CI/CD について | `workflows/` フォルダ |
| その他 | GitHub Issues を作成するか、チーム内で相談 |

---

**このドキュメントが本プロジェクトの開発を加速させる「羅針盤」となることを目指しています。**