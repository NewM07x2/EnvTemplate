# Workflow — 必須開発手順

> **テンプレート利用者へ**: このドキュメントは next-python プロジェクト向けです。修正順序やレイヤ構造は、プロジェクトの実装に合わせてカスタマイズしてください。

本ドキュメントは変更時に必ず従う手順を定義する。
本手順を守らずに実装を開始してはならない。
速度よりも安定性と最小影響を優先する。

---

# 1. コードを書く前に

必ず以下を実施すること：

1. 類似の既存実装を検索する
2. 既存の構造・命名規則・パターンに従う
3. 新規作成より既存ファイル拡張を優先する
4. 新しい設計スタイルを導入しない
5. 修正対象レイヤを確認する（structure.md参照）
6. `app/lib/` のディレクトリ構造に従う

迷った場合は最も近い既存実装に従う。

---

# 2. 修正順序（厳守）

### DB変更がある場合:

1. `supabase/migrations/` で PostgreSQL スキーマ修正
2. `app/lib/data/models/` で Drift Entity 更新
3. `app/lib/data/datasources/` で API/DB アクセス更新
4. `app/lib/data/repositories/` で Repository 更新
5. `features/[feature]/domain/` で UseCase 更新
6. `features/[feature]/presentation/providers/` で Provider 更新
7. `features/[feature]/presentation/` で UI 更新

### 業務ロジックのみ変更の場合:

1. `features/[feature]/domain/` で UseCase 更新
2. `features/[feature]/presentation/providers/` で Provider 更新
3. `features/[feature]/presentation/` で UI 更新

不要なレイヤ変更は禁止。

---

# 3. 状態管理（Riverpod）

- StateNotifier を使用して Provider を定義する
- UI層は Provider 経由でのみアクセスする
- ローカルキャッシュが必要な場合は Drift を使用する
- Provider 間の依存関係を明示的に定義する


- Provider定義時に StateNotifier を使用
- UI層は Provider 経由でのみアクセス
- ローカルキャッシュが必要な場合は Drift を使用
- Provider 間の依存関係を明示的に定義する

---

# 4. 最小差分原則

- 必要な箇所のみ変更
- 無関係なリファクタ禁止
- 不要なリネーム禁止
- ディレクトリ再編禁止
- 明示指示がない限り既存コード削除禁止

---

# 5. テスト方針

必要に応じて：

- UseCase → 純粋関数の単体テスト
- Provider → Repository モックによる単体テスト
- Database 変更 → 必要に応じて結合テスト

テスト設定の変更は禁止。

---

# 6. 禁止事項

明示指示がない限り禁止：

- アーキテクチャ改善
- 抽象化導入
- 性能最適化
- 共通ユーティリティ追加
- パターン置き換え
- 新規フレームワーク導入
- Drift スキーマの手動修正
- バージョンのアップデート
- コードスタイルの変更
- ディレクトリ構造の変更
- 命名規則の変更
- 既存コードの削除(必要な削除を行う場合、ユーザの指示に従って行うこと)
- 既存ファイルの削除(必要な削除を行う場合、ユーザの指示に従って行うこと。削除する場合、影響調査を実施し、関連するコードの修正も行うこと)


---

# 7. 挙動変更時

挙動が変わる場合：

- コードコメントに理由を明記する
- 明示指示がない限り後方互換を維持する

---

# 8. 完了前チェック

終了前に必ず確認：

- 依存関係が正しいか（Presentation → Business Logic → Data）
- 逆方向参照がないか
- ディレクトリ構造に従っているか
- 修正順序（structure.md）に従っているか
- 最小差分原則を守っているか
- Database migrations と Drift Entity が一致しているか

違反があれば修正すること。
