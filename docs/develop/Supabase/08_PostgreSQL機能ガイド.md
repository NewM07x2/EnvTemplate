# 08. PostgreSQL 機能ガイド

> **レベル**: ★★★☆☆（中級）  
> **前提知識**: [01_クイックスタート](01_クイックスタート.md) の完了・基本的な SQL 知識  
> **所要時間**: 約 70 分

---

## 📚 目次

1. [Supabase の DB 基盤について](#1-supabase-の-db-基盤について)
2. [テーブル設計のベストプラクティス](#2-テーブル設計のベストプラクティス)
3. [よく使う PostgreSQL 型](#3-よく使う-postgresql-型)
4. [インデックス](#4-インデックス)
5. [ビュー（View）](#5-ビューview)
6. [関数（Function）とトリガー（Trigger）](#6-関数functionとトリガーtrigger)
7. [トランザクション](#7-トランザクション)
8. [全文検索](#8-全文検索)
9. [JSON / JSONB カラム](#9-json--jsonb-カラム)
10. [バックアップと復元](#10-バックアップと復元)

---

## 1. Supabase の DB 基盤について

Supabase のデータベースは **フルマネージドの PostgreSQL** です。  
Supabase ダッシュボードの **SQL Editor** から直接 SQL を実行できます。

```
Supabase DB の構成:

public スキーマ       ← ユーザーが作るテーブルはここ
auth スキーマ         ← Supabase Auth が管理するユーザーテーブル
storage スキーマ      ← Supabase Storage が使用
extensions スキーマ   ← pgvector 等の拡張機能
```

### ダッシュボードから SQL を実行する

1. Supabase Console > **SQL Editor** を開く
2. SQL を入力して **Run（Ctrl+Enter）** をクリック

---

## 2. テーブル設計のベストプラクティス

### 基本テンプレート

```sql
-- 推奨される標準的なテーブル構造
CREATE TABLE public.articles (
  -- 主キーは UUID を使う（連番より安全・分散環境でも一意）
  id          UUID        PRIMARY KEY DEFAULT gen_random_uuid(),

  -- 作成者と Supabase Auth を紐付ける
  user_id     UUID        NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,

  -- 必須フィールド
  title       TEXT        NOT NULL CHECK (char_length(title) BETWEEN 1 AND 255),
  content     TEXT,

  -- フラグ系はデフォルト値を必ず設定
  is_published BOOLEAN    NOT NULL DEFAULT false,
  is_deleted   BOOLEAN    NOT NULL DEFAULT false,  -- 論理削除

  -- タイムスタンプは必ず付ける
  created_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);
```

### ON DELETE の選択指針

| 設定 | 動作 | 使う場面 |
|------|------|---------|
| `CASCADE` | 親を削除すると子も削除 | ユーザーが退会したら投稿も削除してよい場合 |
| `SET NULL` | 親を削除すると外部キーを NULL に | 投稿者が退会しても投稿は残したい場合 |
| `RESTRICT` | 子が存在する間は親を削除不可 | 注文がある商品は削除させたくない場合 |

### updated_at の自動更新トリガー

毎回手動で `updated_at` を更新するのは忘れやすいため、トリガーで自動化します。

```sql
-- 汎用の updated_at 自動更新関数（一度作れば全テーブルで使い回せる）
CREATE OR REPLACE FUNCTION public.set_updated_at()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$$;

-- articles テーブルに適用
CREATE TRIGGER articles_set_updated_at
  BEFORE UPDATE ON public.articles
  FOR EACH ROW
  EXECUTE FUNCTION public.set_updated_at();
```

---

## 3. よく使う PostgreSQL 型

| 型 | 説明 | 使用例 |
|----|------|--------|
| `UUID` | 128bit の一意 ID | 主キー、外部キー |
| `TEXT` | 可変長文字列（長さ上限なし） | タイトル、本文 |
| `VARCHAR(n)` | 最大 n 文字の文字列 | 固定長が必要な場合（メールは TEXT で可） |
| `INTEGER` | 整数（-21億〜21億） | カウント、年齢 |
| `BIGINT` | 大きな整数 | 大量の連番 |
| `NUMERIC(p, s)` | 精度付き数値 | 金額（例: `NUMERIC(12, 2)`） |
| `BOOLEAN` | true / false | フラグ |
| `TIMESTAMPTZ` | タイムゾーン付き日時 ✅ 推奨 | created_at、updated_at |
| `DATE` | 日付のみ | 誕生日 |
| `JSONB` | バイナリ JSON（インデックス可） | 構造が可変なデータ |
| `TEXT[]` | テキストの配列 | タグ、カテゴリ一覧 |
| `ENUM` | 列挙型 | ステータス管理 |

### ENUM 型の使い方

```sql
-- ステータス用の ENUM 型を作成
CREATE TYPE public.order_status AS ENUM (
  'pending',
  'processing',
  'shipped',
  'delivered',
  'cancelled'
);

-- テーブルで使用
CREATE TABLE public.orders (
  id      UUID         PRIMARY KEY DEFAULT gen_random_uuid(),
  status  order_status NOT NULL DEFAULT 'pending'
);

-- ENUM に値を追加（削除・変更はできないので慎重に）
ALTER TYPE public.order_status ADD VALUE 'refunded';
```

### TIMESTAMPTZ vs TIMESTAMP の違い

```sql
-- ❌ TIMESTAMP: タイムゾーン情報なし（バグの原因になりやすい）
created_at TIMESTAMP DEFAULT now()

-- ✅ TIMESTAMPTZ: UTC で保存・クライアントのタイムゾーンで表示
created_at TIMESTAMPTZ DEFAULT now()
```

> 💡 **常に `TIMESTAMPTZ` を使うこと。** Supabase はすべてのタイムスタンプを UTC で保存し、クライアント側で変換します。

---

## 4. インデックス

インデックスを適切に設定することで、クエリのパフォーマンスを大幅に改善できます。

### インデックスを作る基準

```
インデックスが効果的な列:
  ✅ WHERE 句で頻繁に使う列（例: status, user_id）
  ✅ ORDER BY で使う列（例: created_at）
  ✅ 外部キー列（PostgreSQL は自動作成しない）
  ✅ JOIN のキーになる列

インデックスが不要な列:
  ❌ データ量が少ないテーブル（数百行以下）
  ❌ INSERT/UPDATE が極めて多い列（書き込みが遅くなる）
  ❌ カーディナリティが低い列（true/false の2値など）
```

### インデックスの種類

```sql
-- ① B-tree インデックス（デフォルト・等値・範囲検索に有効）
CREATE INDEX idx_articles_user_id
  ON public.articles(user_id);

CREATE INDEX idx_articles_created_at
  ON public.articles(created_at DESC);  -- DESC で作ると ORDER BY DESC が速い

-- ② 複合インデックス（複数列を組み合わせて検索する場合）
-- WHERE user_id = ? ORDER BY created_at DESC のようなクエリに対応
CREATE INDEX idx_articles_user_created
  ON public.articles(user_id, created_at DESC);

-- ③ 部分インデックス（特定の条件を満たす行だけにインデックスを張る）
-- published な記事だけを高速に検索したい場合
CREATE INDEX idx_articles_published
  ON public.articles(created_at DESC)
  WHERE is_published = true;

-- ④ GIN インデックス（配列・JSONB・全文検索に使用）
CREATE INDEX idx_articles_tags
  ON public.articles USING GIN (tags);
```

### クエリの実行計画を確認する

```sql
-- EXPLAIN ANALYZE でクエリのボトルネックを確認
EXPLAIN ANALYZE
SELECT * FROM public.articles
WHERE user_id = 'xxx' AND is_published = true
ORDER BY created_at DESC
LIMIT 20;

-- "Seq Scan"（全テーブルスキャン）が出たらインデックスを検討
-- "Index Scan" が出ていれば OK
```

---

## 5. ビュー（View）

ビューは **保存された SELECT クエリ** です。複雑な JOIN を隠蔽してシンプルなインターフェースを提供します。

```sql
-- 投稿と著者情報を結合したビュー
CREATE OR REPLACE VIEW public.article_details AS
SELECT
  a.id,
  a.title,
  LEFT(a.content, 200) AS excerpt,  -- 本文の冒頭200文字
  a.is_published,
  a.created_at,
  u.id             AS author_id,
  u.email          AS author_email,
  p.display_name   AS author_name,
  p.avatar_url     AS author_avatar
FROM public.articles a
JOIN auth.users u ON a.user_id = u.id
LEFT JOIN public.profiles p ON a.user_id = p.id
WHERE a.is_deleted = false;
```

```typescript
// クライアントからはテーブルと同じように使える
const { data } = await supabase
  .from('article_details')
  .select('*')
  .eq('is_published', true)
  .order('created_at', { ascending: false })
```

### マテリアライズドビュー（Materialized View）

通常のビューはクエリのたびに実行されます。集計など重い処理は**マテリアライズドビュー**で結果をキャッシュできます。

```sql
-- 日別の投稿数を集計するマテリアライズドビュー
CREATE MATERIALIZED VIEW public.daily_article_counts AS
SELECT
  DATE(created_at) AS date,
  COUNT(*)         AS count
FROM public.articles
WHERE is_published = true
GROUP BY DATE(created_at)
ORDER BY date DESC;

-- マテリアライズドビューの更新（データが変わったら手動 or 定期実行）
REFRESH MATERIALIZED VIEW public.daily_article_counts;
```

---

## 6. 関数（Function）とトリガー（Trigger）

### ストアドファンクション

DB 内にビジネスロジックを実装できます。

```sql
-- ユーザーの投稿数を返す関数
CREATE OR REPLACE FUNCTION public.get_article_count(p_user_id UUID)
RETURNS INTEGER
LANGUAGE sql
STABLE  -- 同じ入力に対して同じ結果を返す（最適化のヒント）
AS $$
  SELECT COUNT(*)::INTEGER
  FROM public.articles
  WHERE user_id = p_user_id AND is_deleted = false;
$$;

-- 呼び出し
SELECT public.get_article_count('user_uuid_here');
```

```typescript
// クライアントから RPC（Remote Procedure Call）で呼び出す
const { data } = await supabase.rpc('get_article_count', {
  p_user_id: userId,
})
```

### トリガーの実装例

```sql
-- ① 新規ユーザー登録時にプロフィールを自動作成
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER
LANGUAGE plpgsql
SECURITY DEFINER  -- 関数の所有者権限で実行（RLS をバイパスして書き込める）
AS $$
BEGIN
  INSERT INTO public.profiles (id, display_name, avatar_url)
  VALUES (
    NEW.id,
    COALESCE(NEW.raw_user_meta_data->>'full_name', split_part(NEW.email, '@', 1)),
    NEW.raw_user_meta_data->>'avatar_url'
  );
  RETURN NEW;
END;
$$;

-- auth.users への INSERT 後に実行
CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW
  EXECUTE FUNCTION public.handle_new_user();
```

```sql
-- ② 投稿が公開されたときに通知レコードを作成
CREATE OR REPLACE FUNCTION public.notify_on_publish()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
  -- false → true に変化したとき（公開操作）
  IF OLD.is_published = false AND NEW.is_published = true THEN
    INSERT INTO public.notifications (user_id, type, payload)
    VALUES (
      NEW.user_id,
      'article_published',
      jsonb_build_object('article_id', NEW.id, 'title', NEW.title)
    );
  END IF;
  RETURN NEW;
END;
$$;

CREATE TRIGGER articles_on_publish
  AFTER UPDATE OF is_published ON public.articles
  FOR EACH ROW
  EXECUTE FUNCTION public.notify_on_publish();
```

---

## 7. トランザクション

複数の操作をひとまとめにして、**すべて成功するか、すべて失敗するか**を保証します。

```sql
-- SQL Editor で実行する場合
BEGIN;

-- ① 在庫を減らす
UPDATE public.products
SET stock = stock - 1
WHERE id = 'product_uuid' AND stock > 0;

-- ② 失敗したらロールバック
DO $$
BEGIN
  IF NOT FOUND THEN
    RAISE EXCEPTION '在庫が不足しています';
  END IF;
END $$;

-- ③ 注文を作成
INSERT INTO public.orders (user_id, product_id, quantity)
VALUES ('user_uuid', 'product_uuid', 1);

COMMIT;
```

```typescript
// クライアントから RPC でトランザクションを実行
// 複数テーブルの操作はストアドファンクションにまとめる

// functions/src/index.ts（Edge Function）で実装するのが現実的
const { data, error } = await supabase.rpc('create_order_with_stock_check', {
  p_user_id: userId,
  p_product_id: productId,
})
```

---

## 8. 全文検索

PostgreSQL の組み込み全文検索機能を使います。

### 全文検索用カラムの追加

```sql
-- tsvector カラムを追加（検索用のインデックスを保存）
ALTER TABLE public.articles
  ADD COLUMN search_vector TSVECTOR
    GENERATED ALWAYS AS (
      -- 日本語の場合は 'simple' 設定を使う
      -- 英語の場合は 'english' が利用可能
      to_tsvector('simple',
        COALESCE(title, '') || ' ' || COALESCE(content, '')
      )
    ) STORED;

-- GIN インデックスを作成
CREATE INDEX idx_articles_search
  ON public.articles USING GIN (search_vector);
```

### 全文検索クエリ

```sql
-- "Supabase" を含む記事を検索
SELECT id, title
FROM public.articles
WHERE search_vector @@ to_tsquery('simple', 'Supabase')
ORDER BY ts_rank(search_vector, to_tsquery('simple', 'Supabase')) DESC;

-- AND 検索（両方の単語を含む）
WHERE search_vector @@ to_tsquery('simple', 'Supabase & PostgreSQL')

-- OR 検索（いずれかの単語を含む）
WHERE search_vector @@ to_tsquery('simple', 'Supabase | Firebase')

-- 前方一致（"Supabase" で始まる）
WHERE search_vector @@ to_tsquery('simple', 'Supabase:*')
```

```typescript
// クライアントからの全文検索
const { data } = await supabase
  .from('articles')
  .select('id, title, excerpt')
  .textSearch('search_vector', keyword, {
    type: 'plain',     // 自然な検索クエリ形式
    config: 'simple',
  })
```

> ⚠️ **日本語の全文検索について**  
> PostgreSQL の標準機能は日本語の形態素解析に対応していません。日本語の高精度な全文検索が必要な場合は `pgroonga` 拡張（Supabase では現時点で非対応）または Algolia・Meilisearch 等の外部サービスを利用してください。

---

## 9. JSON / JSONB カラム

スキーマが定まらない柔軟なデータを保存できます。

### JSONB の基本操作

```sql
-- テーブル定義
CREATE TABLE public.products (
  id         UUID  PRIMARY KEY DEFAULT gen_random_uuid(),
  name       TEXT  NOT NULL,
  attributes JSONB           -- 商品ごとに異なる属性
);

-- データ挿入
INSERT INTO public.products (name, attributes) VALUES
  ('Tシャツ', '{"color": "red", "size": "M", "material": "cotton"}'),
  ('ノートPC', '{"cpu": "M3", "ram": 16, "storage": 512}');

-- JSONB フィールドで検索
SELECT * FROM public.products
WHERE attributes->>'color' = 'red';

-- ネストした値へのアクセス
SELECT attributes->'spec'->>'cpu' AS cpu
FROM public.products;

-- JSONB フィールドのインデックス（特定キーへの高速アクセス）
CREATE INDEX idx_products_color
  ON public.products ((attributes->>'color'));

-- GIN インデックス（すべてのキーを検索可能に）
CREATE INDEX idx_products_attributes
  ON public.products USING GIN (attributes);
```

### JSONB の更新

```sql
-- 特定のキーだけ更新（|| 演算子でマージ）
UPDATE public.products
SET attributes = attributes || '{"color": "blue"}'::jsonb
WHERE id = 'product_uuid';

-- 特定のキーを削除
UPDATE public.products
SET attributes = attributes - 'color'
WHERE id = 'product_uuid';
```

---

## 10. バックアップと復元

### 自動バックアップ（Pro プラン以上）

- **Pro プラン**: 毎日自動バックアップ、7 日間保持
- **Team プラン**: 毎日自動バックアップ、14 日間保持

Supabase Console > **Database** > **Backups** から復元できます。

### 手動バックアップ（pg_dump）

```bash
# Supabase Console > Settings > Database から接続文字列を取得
# Connection string: postgres://postgres:[PASSWORD]@[HOST]:5432/postgres

# バックアップ
pg_dump \
  --format=custom \
  --no-acl \
  --no-owner \
  "postgres://postgres:[PASSWORD]@[HOST]:5432/postgres" \
  > backup_$(date +%Y%m%d).dump

# 復元
pg_restore \
  --format=custom \
  --no-acl \
  --no-owner \
  --dbname="postgres://postgres:[PASSWORD]@[RESTORE_HOST]:5432/postgres" \
  backup_20260228.dump
```

---

## 📌 まとめ

| 機能 | 重要ポイント |
|------|------------|
| 主キー | `UUID DEFAULT gen_random_uuid()` を使う |
| タイムスタンプ | 必ず `TIMESTAMPTZ` を使う |
| updated_at | トリガーで自動更新する |
| インデックス | 外部キー・WHERE・ORDER BY に張る |
| ビュー | 複雑な JOIN を隠蔽してクライアントをシンプルに |
| トリガー | DB レベルの自動処理（プロフィール自動作成等） |
| RPC | ストアドファンクションをクライアントから呼び出す |

---

## 次のステップ

- [Storage ガイド](09_Storageガイド.md) → ファイルのアップロード・管理
