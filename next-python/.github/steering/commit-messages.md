# Commit Messages — コミットメッセージ規約

> **テンプレート利用者へ**: このドキュメントの Scope セクションはプロジェクトに合わせてカスタマイズしてください。以下の例は next-python 向けです。

本ドキュメントは、本リポジトリにおけるコミットメッセージの記述規約を定義する。

すべてのコミットはこの規約に従うこと。

---

## 1. 基本形式

```
<type>(<scope>): <subject>

<body>

<footer>
```

### 1.1 型（Type）

必ず以下のいずれかを使用：

| 型 | 説明 | 例 |
|---|---|---|
| **feat** | 新機能追加 | `feat(user): ユーザー認証機能を追加` |
| **fix** | バグ修正 | `fix(home): ホーム画面のクラッシュを解決` |
| **refactor** | リファクタリング | `refactor(provider): ロジックを抽出` |
| **style** | コード整形・フォーマット | `style: フォーマットを適用` |
| **test** | テスト追加・修正 | `test(usecase): ユニットテストを追加` |
| **docs** | ドキュメント更新 | `docs: APIガイドを更新` |
| **ci** | CI/CD設定変更 | `ci: Flutterテストステップを追加` |
| **chore** | 依存関係更新・ツール設定 | `chore(deps): Flutter SDKを更新` |
| **perf** | パフォーマンス最適化 | `perf(build): クエリを最適化` |
| **db** | データベーススキーマ変更 | `db(migration): usersテーブルを追加` |

### 1.2 スコープ（Scope）

変更の対象範囲を記述する（省略可能だが推奨）：

**フロントエンド（Flutter/Dart）:**
- `ui` — UI Widget変更（Presentation層）
- `provider` — Riverpod Provider変更（State Management）
- `usecase` — UseCase/ビジネスロジック変更（Domain層）
- `repository` — Repository/DataSource変更（Data層）
- `model` — データモデル・Entity変更
- `page` — ページ・スクリーン変更
- `navigation` — ナビゲーション変更
- `l10n` — 国際化・多言語対応
- `test` — テスト関連

**バックエンド（Supabase/PostgreSQL）:**
- `migration` — Database マイグレーション
- `rls` — Row Level Security ポリシー変更
- `schema` — テーブル・カラム定義変更

**API（FastAPI/GraphQL）:**
- `api` — API エンドポイント変更
- `graphql` — GraphQL スキーマ・リゾルバー変更
- `service` — ビジネスロジック・サービス層変更
- `repository` — データベースアクセス層変更

**ローカルDB（Drift）:**
- `drift` — Drift Entity変更

**インフラ・その他:**
- `supabase` — Supabase設定全般
- `github` — GitHub設定（Actions等）
- `config` — アプリケーション設定

**複数スコープの場合:** スコープをカンマ区切りで記述
```
feat(provider,repository): 新しいレポート機能を追加
```

### 1.3 サブジェクト（Subject）

- **日本語で統一** する（英語と日本語の混在禁止）
- 命令形で開始（`追加する`、`解決する`、`更新する`、`削除する`）
- 50文字以内を推奨

**良い例:**
```
feat(usecase): ユーザー登録ロジックを追加
fix(provider): nullポインターエラーを解決
```

**悪い例:**
```
feat(usecase): ユーザー登録ロジックを追加しました  # 過去形
feat(user): add user registration logic  # 英語混在
feat(usecase): ユーザー登録ロジック追加。  # 句点付き
```

---

## 2. ボディ（Body）

- 変更の**理由**と**詳細**を記述する
- 1行72文字以内で改行
- 変更内容そのもの（コードの「何をしたか」）より、**なぜそうしたか**を記述
- 修正順序（`structure.md`・`workflow.md`参照）に沿った変更の場合、その順序を明記

**例:**

```
DB変更に伴うData・Domain・Presentation層の修正

修正順序（structure.md遵守）:
1. supabase/migrations: add_user_verification table追加
2. app/lib/data/models: Drift Entity更新
3. app/lib/data/repositories: insertUser()メソッド更新
4. features/user/domain: RegisterNewUser UseCase統合
5. features/user/presentation: UI更新

後方互換性: 既存メソッドは変更なし
```

---

## 3. フッター（Footer）

### 3.1 Breaking Changes

挙動変更がある場合は必ず記述：

```
BREAKING CHANGE: User.email は User.emailAddress に変更
既存コード: user.email
新規コード: user.emailAddress
```

### 3.2 参照・Issue

関連Issue・PRがある場合：

```
Closes #123
Related to #456
```

### 3.3 影響範囲

大規模変更時は影響範囲を明記：

```
Impact: Data層・Domain層・Presentation層
Affected modules: data, features/user
Migration required: No
```

---

## 4. 実装パターン別の例

### 4.1 DB変更を伴う新機能

```
feat(user): ユーザーメール検証機能を追加

DB変更順序（修正順序に従う）:
1. supabase/migrations: verify_email_history テーブル追加
2. app/lib/data/models: VerifyEmailHistory Drift Entity追加
3. app/lib/data/datasources: API/DB アクセス層実装
4. app/lib/data/repositories: UserRepository に新規メソッド追加
5. features/user/domain: StartEmailVerification UseCase追加
6. features/user/presentation/providers: UserProvider 更新
7. features/user/presentation: UI更新

後方互換性: 既存メソッド不変

Closes #45
```

### 4.2 バグ修正（単一レイヤ）

```
fix(provider): 決済処理のタイムアウトを解決

原因: Supabase API呼び出しのタイムアウト設定不足

修正内容:
- PaymentProvider に明示的タイムアウト設定追加
- リトライロジック実装
- エラーログ調整

テスト: ユニットテスト追加済み
```

### 4.3 Database スキーマ最適化

```
db(migration): ユーザークエリの性能を最適化

修正詳細:
- users テーブルの email カラムにインデックス追加
- 不要な関連テーブル参照削除
- クエリ実行計画を分析・確認済み

実行前後の性能:
- 削除前: 850ms (10万レコード)
- 削除二: 120ms (10万レコード)
```

### 4.4 テスト追加

```
test(usecase): ユーザー登録のユニットテストを追加

追加テストケース:
- 正常系: 有効なメールアドレスとパスワード
- 異常系: 粗複したメールアドレス
- 異常系: 無効なパスワード形式
- 異常系: nullパラメータ

カバレッジ: RegisterUserUseCase 95% → 98%
```

### 4.5 リファクタリング

```
refactor(provider): 状態管理ロジックを抽出

修正内容:
- 複数のProvider で重複していた状態管理ロジックを共通化
- StateNotifier メソッド抽出
- 既存API は変更なし

テスト: 既存ユニットテスト全パス
```

---

## 5. 禁止事項

以下は絶対禁止：

- ✗ 複数の機能を1コミットに混在させる → 1機能=1コミット
- ✗ 無関係なリファクタリングと機能追加の混在
- ✗ コミットメッセージなし（`git commit` のみ）
- ✗ `update`, `fix`, `change` のみで詳細なし
- ✗ 個人的なメモ・絵文字の乱用
- ✗ 日本語と英語の混在（`feat(user): 新規ユーザー登録` は不可）

---

## 6. コミット粒度（重要）

### 変更単位の指針

**1コミット=1責務**

```
❌ 悪い例:
1コミット: 「ユーザー認証・決済処理・UI改善」

✅ 良い例:
1コミット: feat(usecase): ユーザー認証機能を追加
2コミット: feat(usecase): 決済処理を追加
3コミット: feat(ui): ナビゲーションデザインを改善
```

### 修正順序に基づくコミット分割

DB変更を伴う場合は、**レイヤごとにコミット分割を検討**：

```
1コミット: db(migration): add_user_verification_historyテーブル追加
2コミット: feat(model): VerifyEmailHistoryエンティティ追加
3コミット: feat(repository): insertVerificationHistory()を追加
4コミット: feat(usecase): startEmailVerification()を追加
5コミット: feat(provider): メール検証を統合
6コミット: feat(ui): メール検証画面を追加

OR(小規模な場合)

1コミット: feat(user): ユーザーメール検証機能を追加
  → 詳細をbodyで説明
```

---

## 7. チェックリスト

コミット前に必ず確認：

- [ ] Type が正しいか（feat, fix, refactor等）
- [ ] Scope が明確か
- [ ] Subject は命令形・50文字以内か
- [ ] 日本語と英語が混在していないか
- [ ] Body に「なぜ」の理由が書かれているか
- [ ] DB変更の場合、修正順序（structure.md）を記述したか
- [ ] Breaking Change がある場合、BREAKING CHANGE セクションに記述したか
- [ ] 複数機能が混在していないか（1コミット=1責務）
- [ ] workflow.md の修正順序ルールに従っているか
- [ ] Database migrations と Drift Entity が一致しているか

---

## 8. 参考

このルールは Conventional Commits をベースにカスタマイズしたものです。

**本プロジェクト特有の重要ルール：**
- `structure.md` で定義された Flutter + Supabase アーキテクチャを厳守
- `workflow.md` で定義された修正順序（DB → Data → Domain → Presentation）を遵守
- 1コミット=1責務の原則
- 日本語と英語の混在禁止
- Database migrations と Drift Entity の一致を確認

外部参考:
- 標準: https://www.conventionalcommits.org/
