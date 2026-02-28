# Copilot Instructions — Control Entry Point (v1.2)

本リポジトリは厳格なアーキテクチャ制御下でAI支援開発を行います。


---


## 🔴 最優先指令：Single Source of Truth (SSOT)

すべての推論と行動は `steering/` 配下の定義を絶対基準とすること。
AIの「一般的な正解」よりも、本プロジェクトの「独自の掟」を常に優先すること。

優先参照ファイル：
1. `steering/structure.md`  — レイヤ構造・依存制約・修正順序
2. `steering/paths.md`      — 物理パス・パッケージ定義
3. `steering/workflow.md`   — 必須プロセス（精錬・調査・実装・監査）
4. `steering/guardrails.md` — 設計上の禁止事項
5. `steering/build.md`      — ビルドシステム規約・依存関係ロック


---


## 🔴 指導原則

- **既存パターンの尊重:** 確立されたアーキテクチャの「美学」を最優先する。
- **最小限の介入:** 最小の差分を目指す。無許可のリファクタリングは禁止。
- **厳格な遵守:** 明示的に指示されない限り、アーキテクチャを「改善」しようとしない。
- **ボトムアップ実装:** 必ず修正順序（XML -> Mapper -> Service -> UI）に従う。


### 優先順位マトリクス：

**安定性 > 一貫性 > 掟の遵守 > 最小差分 >> (越えられない壁) >> 最適化**

---


## 🔴 成果物の配置場所（全エージェント共通知識）

すべてのワークフロー成果物は、以下の正式な配置場所に保存すること：

### 仕様書
- **配置場所:** `docs/specs/`
- **管理者:** `@spec-refiner`
- **形式:** Markdown (`.md`)
- **命名規則:** `SPEC-{ID}-{機能名}.md` (例: `SPEC-001-seismic-force-calculation.md`)

### 影響分析レポート
- **配置場所:** `docs/analysis/`
- **管理者:** `@analyst`
- **形式:** Markdown (`.md`)
- **命名規則:** `IMPACT-{ID}-{機能名}.md`

### 実装計画書
- **配置場所:** `docs/plans/`
- **管理者:** `@architect`
- **形式:** Markdown (`.md`)  
- **命名規則:** `PLAN-{ID}-{機能名}.md`

### 監査レポート
- **配置場所:** `docs/audits/`
- **管理者:** `@governor`
- **形式:** Markdown (`.md`)
- **命名規則:** `AUDIT-{ID}-{日付}.md`

**ルール:** エージェントは作業を進める前に、前提となる成果物が存在することを確認すること。不足している場合は、`@orchestrator` に調整を依頼すること。

---


## 🔴 エージェント運用ルール

個別のタスクは、専用のエージェント定義（`.github/agents/*.agent.md`）に従って実行せよ。

- `@orchestrator`: ワークフロー調整とエージェント委譲（詳細は `orchestrator.agent.md` を参照）
- `@partner`: 相談・設計判断
- `@spec-refiner`: 仕様精錬
- `@analyst`: 影響調査
- `@architect`: 実装執行（厳格な「修正順序」に従う）
- `@governor`: 適合性監査

**注意:** 複雑な多段階ワークフローの場合は、`@orchestrator` を呼び出してエージェント調整を依頼すること。

---


## 🔴 必須事前飛行チェック（全エージェント）

コードや回答を生成する前に、必ず以下の「内部監査」を実行し出力せよ：

1. **Steering Check:** このタスクに関連する `.github/steering/` ファイルはどれか？
   - 適切なファイルを読み込む: `structure.md`, `paths.md`, `workflow.md`, `guardrails.md`, `build.md`

2. **Context Check:** 現在の作業が `.github/steering/structure.md` のどのセクション（レイヤ）に関係するか？
   - 明示せよ: Controller / Service / Repository / Mapper / XML

3. **Constraint Declaration:** このターンで遵守すべき最優先の制約を宣言せよ。
   - 例: "SQLはJavaに書かない。すべてのSQLは `mapper/` 配下のMyBatis XMLに配置する。"

4. **Artifact Check（該当する場合）:** 実装タスクの場合、前提成果物が存在するか確認せよ：
   - [ ] 仕様書: `docs/specs/SPEC-{ID}-*.md`
   - [ ] 影響分析: `docs/analysis/IMPACT-{ID}-*.md`
   - 不足している場合 → `@orchestrator` に調整を依頼するか、ユーザーに確認せよ。

---

**迷った場合は人間に尋ねよ。「掟（Steering）」違反よりも「わからない」と答える方が良い。**