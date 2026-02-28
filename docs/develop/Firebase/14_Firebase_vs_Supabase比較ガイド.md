# Firebase vs Supabase 比較ガイド

> **レベル**: ★☆☆ / 所要時間: 約 20 分  
> **対象**: どちらを使うか迷っている方・両方を理解して使い分けたい方

---

## 目次

1. [概要比較](#1-概要比較)
2. [技術スタック比較](#2-技術スタック比較)
3. [主要機能の対応表](#3-主要機能の対応表)
4. [データベース比較（Firestore vs PostgreSQL）](#4-データベース比較firestore-vs-postgresql)
5. [認証比較](#5-認証比較)
6. [料金比較](#6-料金比較)
7. [ユースケース別の選定基準](#7-ユースケース別の選定基準)
8. [同じプロジェクトで両方使う場合](#8-同じプロジェクトで両方使う場合)

---

## 1. 概要比較

```
Firebase                          Supabase
────────────────────────────────  ────────────────────────────────
提供元: Google                    提供元: Supabase Inc.（OSS）
設立:   2014年（Googleが買収）    設立:   2020年
DB:     NoSQL（Firestore）        DB:     PostgreSQL（リレーショナル）
特徴:   リアルタイム・モバイル    特徴:   SQL 標準・オープンソース
思想:   クライアント直接接続      思想:   PostgreSQL を BaaS 化
```

| 項目 | Firebase | Supabase |
|------|---------|---------|
| **データベース** | Firestore（NoSQL）/ RTDB | PostgreSQL（リレーショナル） |
| **オープンソース** | ❌ クローズド | ✅ MIT ライセンス |
| **セルフホスト** | ❌ 不可 | ✅ Docker で自前運用可能 |
| **ベンダーロックイン** | 高い | 低い（PostgreSQL 標準） |
| **無料枠** | 充実（Spark プラン） | 充実（2プロジェクト無料） |
| **日本語ドキュメント** | 充実 | 英語中心（翻訳ドキュメントあり） |
| **モバイル SDK** | iOS / Android 充実 | 基本機能のみ |

---

## 2. 技術スタック比較

```
┌─────────────────────────────────────────────────────────────┐
│  Firebase                    │  Supabase                     │
│  ────────────────────────    │  ────────────────────────    │
│  Firestore（NoSQL）          │  PostgreSQL                   │
│  Firebase Auth               │  GoTrue（Auth）               │
│  Cloud Storage               │  Storage（S3互換）            │
│  Cloud Functions（Node.js）  │  Edge Functions（Deno）       │
│  Firebase Hosting            │  （Hosting なし）             │
│  Firebase ML / Vertex AI     │  pgvector（ベクトル検索）     │
│  FCM（プッシュ通知）          │  Realtime（WebSocket）        │
│  Analytics                   │  （Analytics なし）           │
└─────────────────────────────────────────────────────────────┘
```

---

## 3. 主要機能の対応表

| Firebase | Supabase | 相違点 |
|---------|---------|-------|
| Firestore | PostgreSQL + PostgREST | Firebase は NoSQL、Supabase は SQL |
| Realtime Database | Realtime Subscriptions | Supabase は PostgreSQL の変更を Websocket で配信 |
| Firebase Auth | GoTrue | 機能は類似。Firebase は Google 系が簡単 |
| Cloud Storage | Supabase Storage | どちらも S3 互換。Firebase は GCS ベース |
| Cloud Functions | Edge Functions | Firebase は Node.js、Supabase は Deno |
| Firebase Hosting | ❌（なし） | Supabase はホスティング機能がない |
| Analytics / Crashlytics | ❌（なし） | モバイル分析は Firebase が優位 |
| FCM（プッシュ通知） | ❌（なし） | プッシュ通知は Firebase のみ |
| Vertex AI in Firebase | pgvector | Firebase は Gemini 統合、Supabase はベクトル検索 |
| App Check | ❌（なし） | ボット対策は Firebase のみ |
| Remote Config | ❌（なし） | A/B テストは Firebase のみ |

---

## 4. データベース比較（Firestore vs PostgreSQL）

### データモデルの違い

```
Firestore（NoSQL）              PostgreSQL（SQL）
───────────────────────────     ──────────────────────────────
コレクション                    テーブル
  └ ドキュメント（JSON）          └ 行（カラム型が決まっている）
      └ サブコレクション            └ 外部キー（JOIN が使える）

users/                          users テーブル
  user1/                        ┌─────┬──────┬───────┐
    name: "Alice"               │ id  │ name │ email │
    email: "alice@..."          ├─────┼──────┼───────┤
    posts/                      │  1  │Alice │ alice │
      post1/                    └─────┴──────┴───────┘
        title: "Hello"
                                posts テーブル
                                ┌────┬───────┬─────────┐
                                │ id │ title │ user_id │
                                ├────┼───────┼─────────┤
                                │  1 │Hello  │       1 │
                                └────┴───────┴─────────┘
```

### クエリの比較

```typescript
// ── ユーザーの投稿を取得 ──────────────────────────────────────

// Firebase（Firestore）
const q = query(
  collection(db, 'posts'),
  where('authorId', '==', userId),
  orderBy('createdAt', 'desc'),
  limit(10)
);
const snapshot = await getDocs(q);

// Supabase（PostgreSQL）
const { data } = await supabase
  .from('posts')
  .select('*, users(name, avatar_url)')  // JOIN が1行でできる
  .eq('user_id', userId)
  .order('created_at', { ascending: false })
  .limit(10);
```

### Firestore と PostgreSQL の向き不向き

| 項目 | Firestore が有利 | PostgreSQL が有利 |
|------|---------------|-----------------|
| データ構造 | 柔軟なスキーマ・ネスト構造 | 正規化されたリレーショナル |
| スケール | 自動スケール（書き込み分散） | 複雑なクエリ・集計 |
| リアルタイム | onSnapshot で即座に反映 | Realtime で変更通知 |
| JOIN | ❌ できない（別途取得が必要） | ✅ 複雑な JOIN も可能 |
| 全文検索 | ❌ 不可（外部サービス必要） | ✅ pg_trgm・tsvector |
| トランザクション | ドキュメント横断は制限あり | ACID トランザクション完全対応 |
| SQL の知識 | 不要 | 必要 |

---

## 5. 認証比較

| 機能 | Firebase Auth | Supabase Auth |
|------|-------------|-------------|
| メール・パスワード | ✅ | ✅ |
| Google | ✅（設定が簡単） | ✅ |
| GitHub | ✅ | ✅ |
| Apple | ✅ | ✅ |
| Twitter / X | ✅ | ✅ |
| 電話番号（SMS） | ✅ | ✅ |
| Magic Link（メールリンク） | ✅ | ✅ |
| SAML / OIDC（Enterprise） | ✅（Identity Platform） | ✅ |
| 匿名認証 | ✅ | ✅ |
| カスタムトークン | ✅ | ❌ |
| Multi-Factor Auth（MFA） | ✅ | ✅ |
| アクセス制御 | セキュリティルール | Row Level Security（RLS） |

---

## 6. 料金比較

### 無料枠の比較

| 項目 | Firebase Spark | Supabase Free |
|------|--------------|--------------|
| プロジェクト数 | 制限なし | 2 プロジェクト |
| データベースストレージ | 1 GB（Firestore） | 500 MB（PostgreSQL） |
| 読み取り回数 | 50,000 回/日 | 制限なし（API コール） |
| 書き込み回数 | 20,000 回/日 | 制限なし |
| Auth ユーザー数 | 制限なし | 50,000 MAU |
| Storage | 5 GB | 1 GB |
| Functions | 使用不可 | 50万 Edge Function 呼び出し/月 |
| 帯域幅 | 10 GB/月 | 5 GB/月 |
| 休止 | なし | 1週間アクセスなしで停止 |

### 有料プランの比較

| 項目 | Firebase Blaze | Supabase Pro（$25/月） |
|------|--------------|---------------------|
| 月額 | $0（従量課金のみ） | $25 固定 + 超過分 |
| DB ストレージ | $0.18/GB | 8 GB 込み |
| MAU | メール認証は無料 | 100,000 MAU 込み |
| バックアップ | 手動（GCS エクスポート） | 毎日自動バックアップ |
| サポート | コミュニティ | Email サポート |

---

## 7. ユースケース別の選定基準

### Firebase が向いているケース

```
✅ モバイルアプリ（iOS / Android）が主体
✅ リアルタイム機能が重要（チャット・共同編集・ライブ更新）
✅ Google サービスとの連携（Analytics・Crashlytics・AdMob）
✅ プッシュ通知（FCM）が必要
✅ SQL の知識がなく NoSQL が扱いやすい
✅ スキーマが頻繁に変わる柔軟なデータ構造
✅ A/B テスト・Remote Config が必要
```

### Supabase が向いているケース

```
✅ SQL や既存の RDB の知識がある
✅ 複雑な JOIN・集計クエリが必要
✅ ベンダーロックインを避けたい（PostgreSQL 標準）
✅ セルフホストが必要（オンプレミス・プライベートクラウド）
✅ AI・ベクトル検索（pgvector）を使いたい
✅ データの正規化が重要なビジネスアプリ
✅ オープンソースで中身を確認・カスタマイズしたい
```

### 判断フローチャート

```
モバイルアプリが主体か？
  ├─ YES → Firebase（FCM・Analytics・Crashlytics）
  └─ NO
        │
        SQL に慣れているか？
          ├─ YES → Supabase（PostgreSQL の知識を活かせる）
          └─ NO
                │
                複雑なリレーション（JOIN）が必要か？
                  ├─ YES → Supabase（PostgreSQL）
                  └─ NO → Firebase（シンプルに始められる）
```

---

## 8. 同じプロジェクトで両方使う場合

実務では Firebase の一部機能（FCM・Analytics）と Supabase の PostgreSQL を組み合わせることもあります。

### 組み合わせ例

| 機能 | 担当 |
|------|------|
| メインデータ（ユーザー・投稿・注文） | Supabase（PostgreSQL） |
| リアルタイムチャット | Firebase（Firestore） |
| プッシュ通知 | Firebase（FCM） |
| ファイルストレージ | どちらか一方に統一 |
| 認証 | どちらか一方に統一（混在は複雑になる） |

### 注意点

- **認証は1つに統一する**（Firebase Auth と Supabase Auth を両方使うと管理が複雑になる）
- **コストが二重にかかる**可能性がある
- 学習コストも2系統分かかるため、**よほど明確な理由がない限り片方に統一する**方が推奨

---

## まとめ

| | Firebase | Supabase |
|--|---------|---------|
| **向いている開発者** | NoSQL に慣れた人・モバイル開発者 | SQL に慣れた人・フルスタック開発者 |
| **向いているアプリ** | モバイルアプリ・リアルタイムアプリ | Webアプリ・業務システム・データ集計アプリ |
| **ロックイン** | 高（Google 依存） | 低（PostgreSQL 標準） |
| **学習コスト** | NoSQL の考え方を習得する必要あり | SQL の知識があればすぐ使える |
| **エコシステム** | Google の豊富なサービスと連携 | PostgreSQL のエコシステムを活用 |

**迷ったら**: Web アプリ中心で SQL に慣れているなら **Supabase**、モバイルアプリやリアルタイム重視なら **Firebase** が選択しやすいです。

---

## 関連ドキュメント

- [Supabase 学習ガイド](../../develop/Supabase/README.md) — Supabase の詳細ドキュメント
- [Firebase とは](01_Firebaseとは.md) — Firebase の概要
