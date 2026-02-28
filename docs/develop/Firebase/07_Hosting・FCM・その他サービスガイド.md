# Hosting・FCM・その他サービスガイド

> **所要時間**: 約 40 分  
> **対象レベル**: 初心者～中級者  
> **前提**: [Firebase とは何か](01_Firebaseとは.md) を読んでいること  
> **目標**: Firebase Hosting でアプリを公開し、FCM でプッシュ通知を送り、Analytics / Remote Config などの運用系サービスを理解する

---

## 📚 目次

1. [Firebase Hosting（ホスティング）](#firebase-hostingホスティング)
2. [Firebase Cloud Messaging / FCM（プッシュ通知）](#firebase-cloud-messaging--fcmプッシュ通知)
3. [Google Analytics for Firebase（分析）](#google-analytics-for-firebase分析)
4. [Crashlytics（クラッシュ監視）](#crashlyticsクラッシュ監視)
5. [Remote Config（リモート設定）](#remote-configリモート設定)
6. [Performance Monitoring（パフォーマンス計測）](#performance-monitoringパフォーマンス計測)
7. [A/B Testing](#ab-testing)
8. [サービス全体マップ](#サービス全体マップ)

---

## Firebase Hosting（ホスティング）

### Firebase Hosting とは

**Firebase Hosting** は、Web アプリ・静的サイトを **HTTPS で安全かつ高速に配信** できるホスティングサービスです。

```
【Firebase Hosting の特徴】

✅ SSL（HTTPS）が自動で有効
✅ Google の CDN で世界中に高速配信
✅ カスタムドメイン（独自ドメイン）が無料で設定可能
✅ デプロイはコマンド 1 つ（firebase deploy）
✅ プレビューチャンネル（PR ごとの確認 URL を自動生成）
✅ 1 クリックでロールバック可能
```

### セットアップと初回デプロイ

#### ステップ 1: Firebase Hosting の初期化

```bash
# プロジェクトのルートディレクトリで実行
firebase init hosting
```

対話形式の質問：

```
? What do you want to use as your public directory?
  → out  （Next.js の場合）または  dist / build（Vite / CRA の場合）

? Configure as a single-page app (rewrite all urls to /index.html)?
  → Yes  （SPA / Next.js の場合）

? Set up automatic builds and deploys with GitHub?
  → No  （後から設定可）
```

`firebase.json` が生成されます：

```json
{
  "hosting": {
    "public": "out",
    "ignore": ["firebase.json", "**/.*", "**/node_modules/**"],
    "rewrites": [
      {
        "source": "**",
        "destination": "/index.html"
      }
    ]
  }
}
```

#### ステップ 2: アプリをビルド

```bash
# Next.js の場合（Static Export）
npm run build

# Vite / CRA の場合
npm run build
```

#### ステップ 3: デプロイ

```bash
firebase deploy --only hosting
```

デプロイ完了後、以下の URL でアクセスできます：

```
Hosting URL: https://my-app.web.app
             https://my-app.firebaseapp.com
```

### プレビューチャンネル（開発・レビュー用）

本番環境に影響を与えずに **一時的な URL** を発行できます。

```bash
# プレビューチャンネルを作成（有効期限: 7 日間）
firebase hosting:channel:deploy preview-feature-x --expires 7d

# 出力例:
# ✔  hosting:channel: Channel URL (preview-feature-x):
#    https://my-app--preview-feature-x-abc123.web.app
```

### カスタムドメインの設定

1. Firebase Console → 「Hosting」→「カスタムドメインを追加」
2. ドメイン名を入力（例: `www.myapp.com`）
3. DNS に表示される TXT レコードを追加（ドメイン所有権の確認）
4. A レコードまたは CNAME レコードを追加
5. SSL 証明書が自動発行される（数分〜数時間）

### GitHub Actions による自動デプロイ

```bash
# GitHub Actions の設定を自動生成
firebase init hosting:github
```

`.github/workflows/firebase-hosting-*.yml` が生成され、  
PR 作成時にプレビュー URL が、main ブランチへのマージ時に本番デプロイが自動実行されます。

---

## Firebase Cloud Messaging / FCM（プッシュ通知）

### FCM とは

**Firebase Cloud Messaging（FCM）** は、iOS・Android・Web アプリに **無料でプッシュ通知を送信** できるサービスです。

```
【FCM の仕組み】

サーバー / Cloud Functions
  │
  │ 通知リクエスト（FCM API）
  ▼
Firebase Cloud Messaging
  │
  ├── iOS デバイス（APNs 経由）
  ├── Android デバイス（FCM 直接）
  └── Web ブラウザ（Service Worker 経由）
```

### Web（ブラウザ）への通知セットアップ

#### ステップ 1: Messaging の初期化

```typescript
// lib/firebase.ts に追加
import { getMessaging } from "firebase/messaging";

export const messaging = typeof window !== "undefined" ? getMessaging(app) : null;
```

#### ステップ 2: Service Worker の作成

`public/firebase-messaging-sw.js` を作成：

```javascript
// Firebase SDK を読み込む（Service Worker 用）
importScripts("https://www.gstatic.com/firebasejs/10.0.0/firebase-app-compat.js");
importScripts("https://www.gstatic.com/firebasejs/10.0.0/firebase-messaging-compat.js");

firebase.initializeApp({
  apiKey: "YOUR_API_KEY",
  authDomain: "YOUR_AUTH_DOMAIN",
  projectId: "YOUR_PROJECT_ID",
  storageBucket: "YOUR_STORAGE_BUCKET",
  messagingSenderId: "YOUR_SENDER_ID",
  appId: "YOUR_APP_ID",
});

const messaging = firebase.messaging();

// バックグラウンドでの通知受信
messaging.onBackgroundMessage((payload) => {
  console.log("バックグラウンド通知:", payload);
  self.registration.showNotification(payload.notification.title, {
    body: payload.notification.body,
    icon: "/icon.png",
  });
});
```

#### ステップ 3: 通知許可の取得と FCM トークンの取得

```typescript
import { getToken, onMessage } from "firebase/messaging";
import { messaging } from "@/lib/firebase";

async function requestNotificationPermission(): Promise<string | null> {
  if (!messaging) return null;

  // 通知許可を要求
  const permission = await Notification.requestPermission();
  if (permission !== "granted") {
    console.log("通知が拒否されました");
    return null;
  }

  // FCM トークンを取得（VAPID キーは Firebase Console から取得）
  const token = await getToken(messaging, {
    vapidKey: process.env.NEXT_PUBLIC_FIREBASE_VAPID_KEY,
  });

  console.log("FCM トークン:", token);
  // ← このトークンをサーバー（Firestore 等）に保存して通知送信に使う

  return token;
}

// フォアグラウンドでの通知受信
if (messaging) {
  onMessage(messaging, (payload) => {
    console.log("フォアグラウンド通知:", payload);
    // カスタム UI で通知を表示
    alert(`${payload.notification?.title}: ${payload.notification?.body}`);
  });
}
```

### Cloud Functions から通知を送信

```typescript
// functions/src/index.ts
import * as admin from "firebase-admin";
import { initializeApp } from "firebase-admin/app";

initializeApp();

// 特定ユーザーに通知を送る関数
async function sendNotification(fcmToken: string, title: string, body: string) {
  const message = {
    token: fcmToken,
    notification: {
      title,
      body,
    },
    webpush: {
      fcmOptions: {
        link: "https://my-app.web.app", // 通知クリック時の遷移先
      },
    },
  };

  const response = await admin.messaging().send(message);
  console.log("通知送信成功:", response);
}

// 複数ユーザーに一括送信
async function sendMulticastNotification(tokens: string[], title: string, body: string) {
  const message = {
    tokens, // 最大 500 件
    notification: { title, body },
  };

  const response = await admin.messaging().sendEachForMulticast(message);
  console.log(`${response.successCount} 件送信成功, ${response.failureCount} 件失敗`);
}
```

---

## Google Analytics for Firebase（分析）

### Analytics とは

**Google Analytics for Firebase** は、アプリのユーザー行動を **自動的に収集・分析** できるサービスです。

```
【自動収集されるイベント例】

- first_open（アプリの初回起動）
- session_start（セッション開始）
- screen_view（画面遷移）
- user_engagement（アプリ使用時間）
- scroll（スクロール）
- click（クリック）
```

### カスタムイベントの送信

```typescript
import { getAnalytics, logEvent } from "firebase/analytics";
import app from "@/lib/firebase";

const analytics = getAnalytics(app);

// 商品の閲覧イベント
logEvent(analytics, "view_item", {
  item_id: "prod_001",
  item_name: "商品A",
  item_category: "category1",
  price: 1500,
  currency: "JPY",
});

// ボタンクリックイベント
logEvent(analytics, "button_click", {
  button_name: "signup_button",
  page: "landing",
});

// 購入完了イベント
logEvent(analytics, "purchase", {
  transaction_id: "order_123",
  value: 5000,
  currency: "JPY",
  items: [
    { item_id: "prod_001", item_name: "商品A", price: 1500 },
  ],
});
```

> 💡 **活用ポイント**  
> Firebase Console → 「Analytics」ダッシュボードで収集されたデータをグラフで確認できます。  
> ユーザーの離脱ポイントや人気コンテンツの把握に役立ちます。

---

## Crashlytics（クラッシュ監視）

### Crashlytics とは

**Crashlytics** は、アプリの **クラッシュ（エラー）をリアルタイムで検知・レポート** するサービスです。  
主にモバイルアプリ（iOS / Android / Flutter）で使われます。

```
【Crashlytics でわかること】

✅ クラッシュが発生した端末・OS バージョン
✅ クラッシュのスタックトレース（どこでエラーが起きたか）
✅ クラッシュ率（影響を受けているユーザーの割合）
✅ クラッシュ発生の時系列グラフ
✅ クラッシュフリーユーザー率
```

### 非致命的なエラーを手動で記録

```typescript
// Web では Firebase SDK の Crashlytics は非対応（モバイルのみ）
// Web アプリでは代わりに console.error + Analytics でエラーを記録

import { getAnalytics, logEvent } from "firebase/analytics";

const analytics = getAnalytics(app);

function recordError(error: Error, context: string) {
  console.error(`[${context}] エラー:`, error);

  logEvent(analytics, "exception", {
    description: `${context}: ${error.message}`,
    fatal: false,
  });
}

// 使用例
try {
  await riskyOperation();
} catch (error) {
  recordError(error as Error, "riskyOperation");
}
```

---

## Remote Config（リモート設定）

### Remote Config とは

**Remote Config** は、アプリを **再デプロイせずに設定値を変更** できるサービスです。

```
【Remote Config のユースケース】

✅ 機能フラグ（特定ユーザーにだけ新機能を公開）
✅ キャンペーンのテキスト・色をリモートから変更
✅ APIの URLや閾値の動的な変更
✅ A/B テストの設定値の管理
```

### セットアップと使い方

```typescript
import { getRemoteConfig, getValue, fetchAndActivate } from "firebase/remote-config";
import app from "@/lib/firebase";

const remoteConfig = getRemoteConfig(app);

// デフォルト値を設定（Remote Config から取得できない場合のフォールバック）
remoteConfig.defaultConfig = {
  welcome_message: "ようこそ！",
  feature_new_ui_enabled: false,
  max_items_per_page: 20,
};

// キャッシュの最小有効期間（開発中は 0、本番は 3600 = 1時間推奨）
remoteConfig.settings.minimumFetchIntervalMillis = 3600000;

// Remote Config からフェッチして適用
await fetchAndActivate(remoteConfig);

// 値を取得
const welcomeMsg = getValue(remoteConfig, "welcome_message").asString();
const isNewUiEnabled = getValue(remoteConfig, "feature_new_ui_enabled").asBoolean();
const itemsPerPage = getValue(remoteConfig, "max_items_per_page").asNumber();

console.log(welcomeMsg);     // "春のキャンペーン中！" (コンソールで変更した値)
console.log(isNewUiEnabled); // true/false
```

### Firebase Console での設定

1. Firebase Console → 「Remote Config」
2. 「パラメータを追加」で新しいキーと値を設定
3. 「変更を公開」でアプリに反映（再デプロイ不要）

---

## Performance Monitoring（パフォーマンス計測）

### Performance Monitoring とは

**Performance Monitoring** は、アプリの **読み込み速度・API レスポンス時間などを自動計測** するサービスです。

```
【自動収集されるメトリクス（Web）】

- First Contentful Paint（FCP）：最初のコンテンツが表示されるまでの時間
- First Input Delay（FID）：最初の操作に反応するまでの時間
- Largest Contentful Paint（LCP）：最大のコンテンツが表示されるまでの時間
- Time to First Byte（TTFB）：サーバーの最初のレスポンスまでの時間
- HTTP リクエストのレスポンス時間
```

### カスタムトレースで任意の処理時間を計測

```typescript
import { getPerformance, trace } from "firebase/performance";
import app from "@/lib/firebase";

const perf = getPerformance(app);

async function fetchUserData(userId: string) {
  // カスタムトレースの開始
  const t = trace(perf, "fetch_user_data");
  t.start();

  try {
    const data = await fetch(`/api/users/${userId}`).then((r) => r.json());

    // カスタム属性を追加
    t.putAttribute("user_type", data.role ?? "unknown");
    t.putMetric("response_size_bytes", JSON.stringify(data).length);

    return data;
  } finally {
    t.stop(); // トレース終了（自動的に Firebase に送信）
  }
}
```

---

## A/B Testing

### A/B Testing とは

**A/B Testing** は、異なる UI や機能をユーザーグループに分けて見せ、**どちらが効果的かを統計的に検証** するサービスです。  
Remote Config または FCM と組み合わせて使います。

```
【A/B Testing の流れ】

① グループ A（50%）→ ボタンの色: 青
② グループ B（50%）→ ボタンの色: 赤

↓ 一定期間経過後

Firebase Console で結果を比較：
- コンバージョン率: A=3.2%, B=4.8%
- 統計的有意性: 95%
→ B（赤）が優れているため、全ユーザーに赤を採用
```

### Firebase Console での設定手順

1. Firebase Console → 「A/B Testing」→「実験を作成」
2. Remote Config または Messaging を選択
3. 対象ユーザーと割合を設定
4. バリアント（A/B の違い）を設定
5. 評価指標（コンバージョンイベント）を設定
6. 実験を開始 → 結果を確認 → 勝者を採用

---

## サービス全体マップ

Firebase の全サービスの関係を整理すると以下のようになります。

```
【Firebase サービス全体マップ】

データ管理
  ├── Firestore（NoSQL DB）
  ├── Realtime Database（リアルタイム DB）
  └── Cloud Storage（ファイル保存）

ユーザー管理
  └── Authentication（認証）

バックエンド処理
  └── Cloud Functions（サーバーレス関数）

フロントエンド配信
  └── Hosting（Web ホスティング）

通知
  └── Cloud Messaging / FCM（プッシュ通知）

運用・分析
  ├── Google Analytics（行動分析）
  ├── Crashlytics（クラッシュ監視）
  ├── Performance Monitoring（パフォーマンス）
  ├── Remote Config（リモート設定）
  └── A/B Testing（AB テスト）
```

| サービス | 主な用途 | 習得優先度 |
|---------|---------|-----------|
| **Firestore** | データの保存・取得 | ⭐⭐⭐ 最優先 |
| **Authentication** | ユーザーログイン | ⭐⭐⭐ 最優先 |
| **Hosting** | Web アプリの公開 | ⭐⭐⭐ 最優先 |
| **Cloud Storage** | ファイル保存 | ⭐⭐ 中優先 |
| **Cloud Functions** | バックエンド処理 | ⭐⭐ 中優先 |
| **FCM** | プッシュ通知 | ⭐ 必要に応じて |
| **Analytics** | ユーザー行動分析 | ⭐ 必要に応じて |
| **Crashlytics** | クラッシュ監視 | ⭐ モバイル開発時 |
| **Remote Config** | 設定のリモート管理 | ⭐ 必要に応じて |
| **A/B Testing** | UI の効果検証 | ⭐ 必要に応じて |

---

## 📌 参考リンク

| リソース | URL |
|---------|-----|
| Firebase Hosting 公式ドキュメント | https://firebase.google.com/docs/hosting?hl=ja |
| FCM 公式ドキュメント | https://firebase.google.com/docs/cloud-messaging?hl=ja |
| Analytics 公式ドキュメント | https://firebase.google.com/docs/analytics?hl=ja |
| Crashlytics 公式ドキュメント | https://firebase.google.com/docs/crashlytics?hl=ja |
| Remote Config 公式ドキュメント | https://firebase.google.com/docs/remote-config?hl=ja |
| Performance Monitoring 公式ドキュメント | https://firebase.google.com/docs/perf-mon?hl=ja |

---

> 📝 **学習完了おめでとうございます！**  
> このシリーズを通して Firebase の全主要サービスを把握できました。  
> 実際にプロジェクトを作りながら、各ガイドを参照して実装を進めてみてください。  
>
> **ドキュメント一覧に戻る：**
> 1. [Firebase とは何か](01_Firebaseとは.md)
> 2. [Firestore（データベース）ガイド](02_Firestore（データベース）ガイド.md)
> 3. [Authentication（認証）ガイド](03_Authentication（認証）ガイド.md)
> 4. [Cloud Storage（ストレージ）ガイド](04_Cloud_Storage（ストレージ）ガイド.md)
> 5. [Cloud Functions（サーバーレス関数）ガイド](05_Cloud_Functions（サーバーレス関数）ガイド.md)
> 6. [Hosting・FCM・その他サービスガイド](06_Hosting・FCM・その他サービスガイド.md)
