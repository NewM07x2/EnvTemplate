# Firebase vs Supabase 比較ガイド

> **対象者**: どちらの BaaS を採用するか検討している開発者・設計者  
> **目的**: 技術選定の判断基準を提供する

---

## 📚 目次

1. [一言まとめ](#1-一言まとめ)
2. [機能比較](#2-機能比較)
3. [データベース比較](#3-データベース比較)
4. [料金比較](#4-料金比較)
5. [開発体験の比較](#5-開発体験の比較)
6. [ユースケース別の選択指針](#6-ユースケース別の選択指針)
7. [移行コスト](#7-移行コスト)
8. [決定フローチャート](#8-決定フローチャート)

---

## 1. 一言まとめ

| | Firebase | Supabase |
|--|----------|----------|
| **一言** | Googleが作るNoSQLの万能BaaS | PostgreSQLベースのオープンソースBaaS |
| **向いている人** | モバイル開発者・NoSQL 初心者・素早いプロトタイプが必要な人 | SQL に慣れた開発者・オープンソース重視・複雑なデータ構造が必要な人 |

---

## 2. 機能比較

| 機能 | Firebase | Supabase | 備考 |
|------|:--------:|:--------:|------|
| **データベース** | ✅ Firestore（NoSQL） | ✅ PostgreSQL（RDB） | 根本的なアーキテクチャが異なる |
| **リアルタイム同期** | ✅ ネイティブ（高速） | ✅ 対応（WebSocket） | Firebase の方が成熟している |
| **認証** | ✅ 充実 | ✅ 充実 | ほぼ同等 |
| **ソーシャルログイン** | ✅ 豊富 | ✅ 豊富 | ほぼ同等 |
| **ストレージ** | ✅ Cloud Storage | ✅ Supabase Storage | ほぼ同等 |
| **サーバーレス関数** | ✅ Cloud Functions | ✅ Edge Functions（Deno） | Firebase は Node.js、Supabase は Deno |
| **REST API 自動生成** | ❌ なし | ✅ DB から自動生成 | Supabase の強み |
| **GraphQL** | ❌（Firebase Extensions で別途） | ✅ pg_graphql で対応 | |
| **全文検索** | ❌（Algolia 等との連携が必要） | ⚠️ PostgreSQL の `tsvector` で対応（外部ほど強力ではない） | |
| **ベクトル検索（AI）** | ❌（Firebase Extensions で別途） | ✅ pgvector で対応 | Supabase の強み |
| **プッシュ通知（FCM）** | ✅ ネイティブ | ❌（別途実装が必要） | Firebase の圧倒的な強み |
| **クラッシュ分析** | ✅ Crashlytics | ❌ | Firebase の強み（モバイル向け） |
| **A/B テスト** | ✅ | ❌ | Firebase の強み |
| **オープンソース** | ❌ | ✅ | セルフホスト可否に直結 |
| **セルフホスト** | ❌ | ✅ Docker 対応 | ベンダーロックイン回避 |

---

## 3. データベース比較

これが両者の最大の違いです。

### Firebase（Firestore）: NoSQL ドキュメント DB

```javascript
// データ構造の例
{
  "posts": {
    "post_001": {
      "title": "Hello World",
      "authorId": "user_001",    // ← JOIN できない。参照のみ
      "tags": ["tech", "web"],
      "createdAt": Timestamp
    }
  }
}
```

**得意なこと:**
- ネストしたデータをそのまま保存できる
- スキーマレス（カラムの定義不要）
- 水平スケールが得意

**苦手なこと:**
```
❌ JOIN（関連データを1クエリで取れない）
   → 投稿一覧と著者名を同時に取る → 2回クエリが必要

❌ 集計クエリ
   → 月別の売上合計 → Cloud Functions 等で別途集計

❌ トランザクション（複数コレクションにまたがる場合は制約あり）
```

### Supabase（PostgreSQL）: リレーショナル DB

```sql
-- テーブル定義が必要
CREATE TABLE posts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  title TEXT NOT NULL,
  author_id UUID REFERENCES users(id),  -- 外部キー
  created_at TIMESTAMPTZ DEFAULT now()
);
```

```typescript
// JOIN で1クエリで取得できる
const { data } = await supabase
  .from('posts')
  .select(`
    id, title,
    author:users(id, name, avatar_url)  ← JOIN
  `)
```

**得意なこと:**
- JOIN・複雑な集計クエリ
- スキーマによる型安全
- トランザクションの完全サポート
- SQL の豊富なエコシステム

**苦手なこと:**
```
⚠️ スキーマ変更はマイグレーションが必要（Firestore は不要）
⚠️ ネストしたデータは複数テーブルに分割が必要
```

### どちらを選ぶか？

```
データ構造で選ぶ：

✅ Firebase が向いている
  - フィールドが可変・構造が頻繁に変わる
  - ネストが深いドキュメント（チャットメッセージ等）
  - データが独立していてリレーションが少ない

✅ Supabase が向いている
  - 複数のテーブルを結合して分析したい
  - 厳格なスキーマで型安全を確保したい
  - 既に SQL の知識がある
  - 集計・レポートが必要な業務システム
```

---

## 4. 料金比較

### 無料枠の比較（2026年2月現在）

| リソース | Firebase（Spark） | Supabase（Free） |
|---------|:----------------:|:---------------:|
| **DB 容量** | 1 GiB | 500 MB |
| **ストレージ** | 5 GB | 1 GB |
| **転送量** | 10 GB / 月 | 5 GB / 月 |
| **Functions / Edge Functions** | 125K 呼び出し / 月 | 50 万回 / 月 |
| **認証ユーザー数** | 無制限 | 無制限 |
| **自動停止** | なし | 7 日間無操作で停止 |
| **プロジェクト数** | 制限あり | 2 件 |

> ⚠️ Supabase Free プランは **7 日間アクセスがないと自動停止**します。本番環境には Pro プランが必要です。

### 有料プランの比較

| | Firebase（Blaze） | Supabase（Pro） |
|-|:----------------:|:--------------:|
| **月額基本料** | $0（従量課金のみ） | $25 |
| **DB** | $0.06 / GB / 月 | 8 GB 込み、超過 $0.125 / GB |
| **Functions** | $0.0000004 / 回 | 500 万回 / 月含む |
| **コスト予測** | ⚠️ アクセス急増で高額になる可能性 | ✅ 基本料金で予測しやすい |

### コスト選択の目安

```
月額コストで選ぶ：

Firebase（Blaze）が向いている
  → 普段はアクセス少ないが、たまにバースト（スパイク）がある
  → 使わない月は課金ゼロにしたい

Supabase（Pro: $25）が向いている
  → 月額コストを固定したい
  → 本番環境で安定した予測コストが必要
```

---

## 5. 開発体験の比較

### セットアップの速さ

| | Firebase | Supabase |
|-|:--------:|:--------:|
| アカウント作成〜初回クエリ | 約 10 分 | 約 10 分 |
| SDK の学習コスト | 低（独自 API） | 低〜中（SQL 知識が必要） |
| 型定義の自動生成 | ❌（手動で定義） | ✅ CLI で自動生成 |
| ローカルエミュレーター | ✅ Firebase Emulator Suite | ✅ Supabase CLI（Docker 必要） |

### SDK の使い勝手

```typescript
// Firebase: 独自の API スタイル
const q = query(
  collection(db, 'posts'),
  where('published', '==', true),
  orderBy('createdAt', 'desc'),
  limit(10)
)
const snapshot = await getDocs(q)

// Supabase: SQL ライクで直感的
const { data } = await supabase
  .from('posts')
  .select('id, title, created_at')
  .eq('published', true)
  .order('created_at', { ascending: false })
  .limit(10)
```

**Firebase**: 独自の API を覚える必要があるが、SQL の知識は不要  
**Supabase**: SQL の知識がある人には直感的。型定義も自動生成できる

---

## 6. ユースケース別の選択指針

### 🏆 Firebase を選ぶべきケース

| ケース | 理由 |
|--------|------|
| **iOS / Android ネイティブアプリ** | FCM（プッシュ通知）・Crashlytics が充実 |
| **チャットアプリ** | Realtime Database は超低レイテンシのリアルタイム同期が得意 |
| **プッシュ通知が必須** | FCM は Firebase の圧倒的な強み |
| **ゲームアプリ** | Analytics・A/B テスト・Remote Config が充実 |
| **SQL の知識がないチーム** | スキーマレスで始めやすい |
| **データ構造が頻繁に変わる MVP** | スキーマ変更が不要 |

### 🏆 Supabase を選ぶべきケース

| ケース | 理由 |
|--------|------|
| **業務システム・管理画面** | JOIN・集計クエリが必須 |
| **SQL に慣れたチーム** | 既存の知識をそのまま活かせる |
| **ベンダーロックインを避けたい** | オープンソース・セルフホスト可 |
| **AI / RAG アプリ** | pgvector による埋め込みベクトル検索 |
| **REST API を自動生成したい** | テーブル定義だけで API が使える |
| **Next.js / SSR アプリ** | Server Components との相性が良い |
| **コストを固定したい** | Pro プランで予測しやすい |

### 🤝 両方使うケース

```
mobile アプリ（Firebase）+ Web 管理画面（Supabase）

  モバイルアプリ
  ├── プッシュ通知  → Firebase FCM
  ├── クラッシュ監視 → Firebase Crashlytics
  └── ユーザーデータ → Firebase Auth / Firestore

  管理画面（内部ツール）
  ├── データ分析・集計 → Supabase PostgreSQL
  └── 管理者認証 → Supabase Auth
```

---

## 7. 移行コスト

### Firebase → Supabase

```
難しさ: ★★★★☆（高）

主な作業:
  1. NoSQL データを PostgreSQL のスキーマに設計し直す
  2. Firestore のデータをエクスポート → PostgreSQL にインポート
  3. リアルタイム同期のコードを書き換え
  4. セキュリティルール → RLS ポリシーに書き換え
  5. Cloud Functions → Edge Functions に書き換え

難しい理由:
  - データモデルが根本的に異なる（NoSQL → RDB）
  - Firestore の独自クエリ → SQL への書き換え
```

### Supabase → Firebase

```
難しさ: ★★★☆☆（中〜高）

主な作業:
  1. PostgreSQL のテーブル → Firestore コレクション設計
  2. SQL クエリ → Firestore クエリへの書き換え
  3. RLS ポリシー → セキュリティルールへの書き換え

難しい理由:
  - JOIN が使えなくなるため、データモデルの再設計が必要
  - SQL の集計ロジックを Cloud Functions で再実装
```

### Supabase → 別の PostgreSQL（移行が簡単）

```
難しさ: ★☆☆☆☆（低）

Supabase は標準 PostgreSQL なので、
  → AWS RDS、Google Cloud SQL、PlanetScale 等にほぼそのまま移行可能
  → ベンダーロックインが低い最大の理由
```

---

## 8. 決定フローチャート

```
スタート
  │
  ├─ モバイルアプリ（iOS/Android）で
  │  プッシュ通知・クラッシュ監視が必要？
  │   YES → 🔥 Firebase
  │
  ├─ SQL（JOIN・集計）が必要？
  │   YES → ⚡ Supabase
  │
  ├─ ベンダーロックインを避けたい？
  │   YES → ⚡ Supabase
  │
  ├─ チームに SQL 経験者がいる？
  │   YES → ⚡ Supabase（学習コスト低い）
  │   NO  → どちらでも OK（Firebase の方が SQL 知識不要）
  │
  ├─ リアルタイム同期が最重要？
  │   YES → 🔥 Firebase（より成熟している）
  │
  ├─ AI / ベクトル検索が必要？
  │   YES → ⚡ Supabase（pgvector）
  │
  └─ 上記に当てはまらない（CRUD 中心のシンプルなアプリ）
      → どちらでも OK。チームの好みで選ぶ
```

---

## 📌 まとめ

| 判断軸 | Firebase | Supabase |
|--------|:--------:|:--------:|
| モバイル（FCM/Crashlytics） | 🏆 | — |
| リアルタイム | 🏆 | ✅ |
| SQL・複雑なクエリ | — | 🏆 |
| ベンダーロックインなし | — | 🏆 |
| AI / ベクトル検索 | — | 🏆 |
| コスト予測しやすい | — | 🏆 |
| 学習コスト（SQL 知識不要） | 🏆 | — |
| セルフホスト | — | 🏆 |

> **どちらが優れているかではなく、プロジェクトの要件に合った方を選ぶこと。**

---

## 関連ドキュメント

- [Firebase 学習ガイド](../Firebase/README.md)
- [Supabase 学習ガイド](../develop/Supabase/README.md)
