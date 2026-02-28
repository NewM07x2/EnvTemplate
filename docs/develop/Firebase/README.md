# Firebase 学習ガイド

> **対象者**: 開発初心者・新規参画者向けの Firebase 解説資料です。

---

## 📚 ドキュメント一覧

| # | ファイル | 内容 | レベル |
|---|---------|------|--------|
| — | [Firebase とは](01_Firebaseとは.md) | 概要・主な機能・Supabase との比較・ユースケース | ★☆☆ |
| 1 | [クイックスタート](02_クイックスタート.md) | プロジェクト作成・SDK 設定・初回接続・エミュレーター | ★☆☆ |
| 2 | [Authentication（認証）ガイド](03_Authentication（認証）ガイド.md) | メール・Google 認証・Next.js 統合・エラーハンドリング | ★★☆ |
| 3 | [Firestore（データベース）ガイド](04_Firestore（データベース）ガイド.md) | データの読み書き・クエリ・リアルタイム同期・セキュリティルール | ★★☆ |
| 4 | [Cloud Storage（ストレージ）ガイド](05_Cloud_Storage（ストレージ）ガイド.md) | ファイルのアップロード・ダウンロード・削除・セキュリティルール | ★★☆ |
| 5 | [Cloud Functions（サーバーレス関数）ガイド](06_Cloud_Functions（サーバーレス関数）ガイド.md) | HTTP・Callable・Firestore/Auth/Storage トリガー・定期実行 | ★★★ |
| 6 | [Hosting・FCM・その他サービスガイド](07_Hosting・FCM・その他サービスガイド.md) | Web 公開・プッシュ通知・Analytics・Remote Config・A/B Testing | ★★☆ |
| 7 | [Next.js 統合ガイド](08_Next.js統合ガイド.md) | App Router × Firebase・Server/Client Components の使い分け | ★★★ |
| 8 | [セキュリティルール詳細ガイド](09_セキュリティルール詳細ガイド.md) | Firestore/Storage のアクセス制御・データ検証・ルールテスト | ★★★ |
| 9 | [コスト・料金管理ガイド](10_コスト・料金管理ガイド.md) | 無料枠の把握・コスト削減策・予算アラート設定 | ★★☆ |
| 10 | [エミュレーター・ローカル開発ガイド](11_エミュレーター・ローカル開発ガイド.md) | ローカル環境構築・シードデータ・CI/CD 連携 | ★★☆ |
| 11 | [Firebase × AI 機能ガイド](12_Firebase×AI機能ガイド.md) | Gemini API・マルチモーダル・Function Calling・Extensions | ★★★ |
| 12 | [マイグレーション・データ移行ガイド](13_マイグレーション・データ移行ガイド.md) | スキーマ変更・バッチ移行・バックアップ・他 DB からの移行 | ★★★ |
| 13 | [Firebase vs Supabase 比較ガイド](14_Firebase_vs_Supabase比較ガイド.md) | 機能・料金・ユースケース別の選定基準 | ★☆☆ |
| 14 | [Realtime Database ガイド](15_Realtime_Databaseガイド.md) | プレゼンス管理・チャット・Firestore との使い分け | ★★☆ |
| 15 | [テスト戦略ガイド](16_テスト戦略ガイド.md) | ユニット/統合/E2E テスト・Firebase モック・セキュリティルールテスト | ★★★ |
| 16 | [デプロイ・CI/CD ガイド](17_デプロイ・CI_CDガイド.md) | firebase deploy・GitHub Actions・環境分離・プレビューチャンネル | ★★★ |
| 17 | [パフォーマンス最適化ガイド](18_パフォーマンス最適化ガイド.md) | Firestore インデックス・Bundle 削減・コールドスタート対策 | ★★★ |

---

## 学習の進め方

```
Step 1:  01_Firebaseとは.md              で全体像を把握（15分）
Step 2:  02_クイックスタート.md          でプロジェクトを作成（20分）
Step 3:  11_エミュレーター・ローカル開発  でローカル環境を構築（35分）← 早めに設定推奨
Step 4:  03_Authentication ガイド        でログイン機能を実装（35分）
Step 5:  04_Firestore ガイド             でデータの読み書きを実装（45分）
Step 6:  05_Cloud_Storage ガイド         でファイル管理を実装（30分）
Step 7:  06_Cloud_Functions ガイド       でバックエンド処理を追加（50分）
Step 8:  07_Hosting・FCM ガイド          でアプリを公開・通知を設定（40分）
Step 9:  08_Next.js 統合ガイド           で本番品質の統合パターンを習得（60分）
Step 10: 09_セキュリティルール詳細       でアクセス制御を強化（50分）
Step 11: 10_コスト・料金管理             で本番運用前にコスト対策（30分）
```

---

## 関連ドキュメント

- [Supabase 学習ガイド](../develop/Supabase/README.md) — Firebase と比較されることが多い BaaS
