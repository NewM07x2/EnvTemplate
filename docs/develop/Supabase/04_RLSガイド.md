# RLS（Row Level Security）ガイド：セキュアなデータアクセス

> **所要時間**: 約 50 分  
> **対象レベル**: 中級者～上級者（レベル 3）  
> **前提**: [認証ガイド](02_認証ガイド.md) と [REST API ガイド](03_REST_APIガイド.md) を完了していること

---

## 📋 このガイドでやること

1. RLS（Row Level Security）の概念理解
2. RLS ポリシーの有効化
3. 基本的なポリシーの作成
4. ユーザー別データアクセス制限
5. 複雑なポリシー設計パターン

---

## RLS とは

**RLS（Row Level Security）** は、PostgreSQL のセキュリティ機能で、**DB レベルでデータアクセスを行制御** します。

```
従来の実装：
  ユーザーからのリクエスト
    ↓
  API・アプリケーション層で権限チェック
    ↓
  不正なアクセスは API で拒否

RLS 使用時：
  ユーザーからのリクエスト
    ↓
  API・アプリケーション層（不完全でも OK）
    ↓
  DATABASE 層で権限チェック（最後の砦）
    ↓
  不正なアクセスは DB で強制的に拒否
```

### RLS の利点

| 利点 | 説明 |
|------|------|
| **安全性** | API のバグでもデータ漏洩しない |
| **シンプル** | ビジネスロジックを DB で一元管理 |
| **高速** | DB レベルで処理するため効率的 |
| **監査** | すべてのアクセスが DB で記録される |

---

## ステップ 1: RLS を有効化

### 1-1. Supabase ダッシュボードを開く

左メニュー → 「Authentication」→ 「Policies」タブ

### 1-2. テーブルごとに RLS を有効化

```
┌─────────────────────────────────┐
│ Row Level Security (RLS)        │
├─────────────────────────────────┤
│ users     ☑ Enable RLS          │
│ posts     ☑ Enable RLS          │
│ comments  ☑ Enable RLS          │
└─────────────────────────────────┘
```

すべてのテーブルで RLS を **有効化** してください。

⚠️ **注意**: RLS を有効にすると、ポリシーがないと誰もデータにアクセスできません。**必ず次のステップでポリシーを作成してください**。

---

## ステップ 2: 基本的なポリシー作成

### 2-1. ポリシーエディタを開く

テーブルの右側にある「Policies」をクリック。

```
┌──────────────────────────────────────┐
│ users テーブルの Policies            │
├──────────────────────────────────────┤
│ [+ New Policy]                       │
└──────────────────────────────────────┘
```

### 2-2. 最初のポリシー：「誰でも読める」

**シナリオ**: ユーザー情報を誰でも読めるようにしたい

```sql
CREATE POLICY "Users are viewable by everyone"
ON users
FOR SELECT
USING (true);
```

**Supabase UI での入力:**

| 項目 | 値 |
|------|-----|
| **Policy name** | Users are viewable by everyone |
| **Allowed operation** | SELECT |
| **Target role** | All roles |
| **USING expression** | `true` |

---

## ステップ 3: ユーザー別アクセス制限

### シナリオ 1: ユーザーは自分のデータだけ更新可能

**ポリシー内容**: UPDATE 時に、`user_id` が現在のユーザー ID と一致する場合のみ許可

```sql
CREATE POLICY "Users can update their own profile"
ON users
FOR UPDATE
USING (auth.uid() = id)
WITH CHECK (auth.uid() = id);
```

**説明:**
- `auth.uid()` — 現在ログインしているユーザーの ID
- `USING` — 更新前のチェック（元の行が本人か確認）
- `WITH CHECK` — 更新後のチェック（更新後も本人か確認）

**Supabase UI での入力:**

| 項目 | 値 |
|------|-----|
| **Policy name** | Users can update their own profile |
| **Allowed operation** | UPDATE |
| **Target role** | authenticated （ログイン済みユーザー） |
| **USING expression** | `auth.uid() = id` |
| **WITH CHECK expression** | `auth.uid() = id` |

### シナリオ 2: ユーザーは自分の投稿だけ削除可能

```sql
CREATE POLICY "Users can delete their own posts"
ON posts
FOR DELETE
USING (auth.uid() = user_id);
```

### シナリオ 3: 管理者はすべてのデータにアクセス可能

```sql
-- users テーブルに role カラムを追加していることが前提
CREATE POLICY "Admins can manage all users"
ON users
FOR ALL
USING (
  (SELECT role FROM users WHERE id = auth.uid()) = 'admin'
);
```

---

## ステップ 4: 複雑なポリシー設計

### 4-1. 複数の条件を組み合わせる

**シナリオ**: 投稿者またはオーナーが投稿を編集可能

```sql
CREATE POLICY "Users can update their posts or posts on their own profile"
ON posts
FOR UPDATE
USING (
  auth.uid() = user_id
  OR auth.uid() = (SELECT owner_id FROM users WHERE id = user_id)
)
WITH CHECK (
  auth.uid() = user_id
  OR auth.uid() = (SELECT owner_id FROM users WHERE id = user_id)
);
```

### 4-2. ロールベースのアクセス制御（RBAC）

**テーブル構造:**
```
users テーブル:
- id (UUID)
- email (VARCHAR)
- role (VARCHAR) — 'admin', 'moderator', 'user'
```

**複数のポリシー:**

```sql
-- 一般ユーザーは公開情報のみ閲覧
CREATE POLICY "Users can view public data"
ON posts
FOR SELECT
USING (is_public = true);

-- モデレーターはすべての投稿を閲覧
CREATE POLICY "Moderators can view all posts"
ON posts
FOR SELECT
USING (
  (SELECT role FROM users WHERE id = auth.uid()) = 'moderator'
);

-- 管理者はすべての操作が可能
CREATE POLICY "Admins have full access"
ON posts
FOR ALL
USING (
  (SELECT role FROM users WHERE id = auth.uid()) = 'admin'
);
```

### 4-3. タイムスタンプベースのアクセス制限

**シナリオ**: 投稿は 24 時間以内なら編集可能

```sql
CREATE POLICY "Users can edit posts within 24 hours"
ON posts
FOR UPDATE
USING (
  auth.uid() = user_id
  AND (NOW() - created_at) < INTERVAL '24 hours'
);
```

---

## ステップ 5: ポリシーのテスト

### 5-1. SQL Editor でテスト

左メニュー → 「SQL Editor」

```sql
-- 現在のユーザーの情報を取得（RLS が適用される）
SELECT * FROM users;

-- 特定のユーザー ID のデータを取得（RLS で拒否される可能性あり）
SELECT * FROM users WHERE id = 'other-user-id';
```

### 5-2. クライアント側でテスト

```typescript
import { supabase } from '@/lib/supabase'

// テスト 1: 自分のデータを取得（成功するはず）
const { data, error } = await supabase
  .from('users')
  .select('*')
  .eq('id', currentUserId)

console.log('テスト 1 結果:', data, error)

// テスト 2: 他人のデータを取得（RLS で拒否されるはず）
const { data, error } = await supabase
  .from('users')
  .select('*')
  .eq('id', otherUserId)

console.log('テスト 2 結果:', data, error)
// エラー: "403 Forbidden" または "new row violates row-level security policy"
```

---

## ステップ 6: よくあるポリシーパターン

### パターン 1: 公開 / プライベート

```sql
-- 公開投稿はすべて表示、プライベート投稿は本人だけ
CREATE POLICY "Public posts visible to all, private to owner"
ON posts
FOR SELECT
USING (
  is_public = true
  OR auth.uid() = user_id
);
```

### パターン 2: チームメンバーのみアクセス

```sql
-- 同じチームに属するメンバーのみアクセス
CREATE POLICY "Team members can view team data"
ON team_posts
FOR SELECT
USING (
  team_id IN (
    SELECT team_id FROM team_members WHERE user_id = auth.uid()
  )
);
```

### パターン 3: 承認済みデータのみ表示

```sql
-- 公開されている投稿のみ表示
CREATE POLICY "Show only approved posts"
ON posts
FOR SELECT
USING (
  status = 'approved'
  OR (status = 'draft' AND auth.uid() = user_id)
);
```

### パターン 4: 親レコードの所有者がアクセス可能

```sql
-- コメントは投稿の所有者またはコメント作成者が管理可能
CREATE POLICY "Comment access via post ownership"
ON comments
FOR ALL
USING (
  auth.uid() = user_id
  OR auth.uid() = (SELECT user_id FROM posts WHERE id = post_id)
);
```

---

## セキュリティのベストプラクティス

### 🔐 Do's（推奨）

- ✅ **すべてのテーブルで RLS を有効化** — 最小権限の原則
- ✅ **明示的にポリシーを定義** — デフォルトは拒否
- ✅ **auth.uid() を使用** — 信頼できるユーザー識別
- ✅ **ポリシーを定期的にレビュー** — 不要なポリシーは削除
- ✅ **監査ログを有効化** — すべてのアクセスを記録

### 🚫 Don'ts（禁止）

- ❌ **RLS なしでプロダクション運用** — 致命的なセキュリティリスク
- ❌ **USING = true（すべてをオープン）** — RLS の意味がない
- ❌ **クライアント側のみで権限チェック** — API のバグで突破される
- ❌ **ユーザー入力を直接 SQL に使用** — SQL インジェクションのリスク
- ❌ **複雑なポリシーを過度に作成** — 管理と パフォーマンスの低下

---

## トラブルシューティング

### Q: 「403 Forbidden」エラーが出ている

**確認事項:**
1. RLS が有効になっているか
2. ポリシーが正しく定義されているか
3. `auth.uid()` が正しく機能しているか（ログイン状態か）

**解決方法:**
```sql
-- ポリシーが有効か確認
SELECT * FROM pg_policies WHERE tablename = 'users';

-- ポリシーを一時的に削除してテスト
DROP POLICY "policy-name" ON users;
```

### Q: すべてのユーザーがすべてのデータにアクセスできてしまう

**原因**: ポリシーが定義されていないか、`USING = true` になっている

**解決方法**: 最小権限の原則に基づいて ポリシーを再設計

```sql
-- 安全なデフォルトに変更
CREATE POLICY "Restrict access by default"
ON sensitive_table
FOR ALL
USING (false);  -- すべてアクセス拒否

-- その後、必要に応じて許可ルールを追加
CREATE POLICY "Allow specific users"
ON sensitive_table
FOR SELECT
USING (auth.uid() IN (SELECT user_id FROM allowed_users));
```

---

## 🎉 RLS マスター完了！

セキュアな Supabase アプリケーション設計ができました。

---

## 次のステップ

- 📚 [Supabase 公式ドキュメント](https://supabase.com/docs/guides/auth/row-level-security)
- 🎓 [PostgreSQL RLS チュートリアル](https://www.postgresql.org/docs/current/ddl-rowsecurity.html)
- 🔒 [セキュリティベストプラクティス](https://supabase.com/docs/guides/auth/overview)

---

## チェックリスト：本番環境への移行前確認

本番環境に移行する前に、以下をチェックしてください：

- [ ] すべてのテーブルで RLS が有効
- [ ] すべてのテーブルに適切なポリシーが定義済み
- [ ] `auth.uid()` を使ったユーザー識別ポリシー実装済み
- [ ] 管理者用の特別なポリシースコープ実装済み
- [ ] ローカル環境でのポリシーテスト完了
- [ ] 複数ユーザーでのアクセステスト完了
- [ ] 監査ログが有効化
- [ ] セキュリティレビュー完了

---

**Supabase での安全なデータベース開発をお楽しみください！**
