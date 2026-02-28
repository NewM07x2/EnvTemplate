# Cloud Functions（サーバーレス関数）ガイド

> **レベル**: ★★★☆☆（中級）  
> **前提知識**: [02_クイックスタート](02_クイックスタート.md)・[03_Authentication（認証）ガイド](03_Authentication（認証）ガイド.md) の完了  
> **所要時間**: 約 50 分  
> **目標**: Cloud Functions の仕組みを理解し、HTTP・Firestore・Auth・定期実行など代表的なトリガーを使った処理を実装できるようになる

---

## 📚 目次

1. [Cloud Functions とは](#1-cloud-functionsとは)
2. [セットアップ](#2-セットアップ)
3. [HTTP 関数（API エンドポイント）](#3-http関数apiエンドポイント)
4. [Callable 関数（クライアントから呼び出す推奨方法）](#4-callable-関数クライアントから呼び出す推奨方法)
5. [Firestore トリガー](#5-firestoreトリガー)
6. [Authentication トリガー](#6-authenticationトリガー)
7. [スケジュール実行（Cron）](#7-スケジュール実行cron)
8. [Storage トリガー](#8-storageトリガー)
9. [環境変数・シークレットの管理](#9-環境変数シークレットの管理)
10. [デプロイとローカルテスト](#10-デプロイとローカルテスト)
11. [よくあるミスとベストプラクティス](#11-よくあるミスとベストプラクティス)

---

## 1. Cloud Functions とは

**Cloud Functions for Firebase** は、**サーバーを自分で用意・管理せずに** バックエンドのロジックを実行できるサービスです。

```
【Cloud Functions の仕組み】

イベント（HTTP リクエスト / DB の変更 / ユーザー登録 等）
  │
  ▼
Cloud Functions（コードが実行される）
  │
  ▼
処理結果（DB 更新 / メール送信 / 外部 API 呼び出し 等）

ポイント：
✅ サーバー不要（Google が管理）
✅ 使った分だけ課金（アイドル時はコスト 0）
✅ 自動スケール（アクセスが増えても自動で対応）
✅ Node.js（TypeScript / JavaScript）で実装
```

### トリガーの種類

| トリガー種別 | 説明 | 使用例 |
|------------|------|--------|
| **HTTP** | HTTP リクエストで起動 | REST API |
| **Callable** | クライアント SDK から呼び出す | 認証付き API（推奨） |
| **Firestore** | DB ドキュメントの変更で起動 | データ連動・通知 |
| **Authentication** | ユーザーの作成・削除で起動 | ウェルカムメール |
| **Cloud Storage** | ファイルのアップロード・削除で起動 | サムネイル生成 |
| **Pub/Sub（定期）** | スケジュールで起動 | バッチ処理 |

---

## 2. セットアップ

### Firebase CLI での初期化

```bash
# プロジェクトルートで実行
firebase init functions

# 質問への回答:
# ? What language would you like to use? → TypeScript
# ? Do you want to use ESLint?           → Yes
# ? Do you want to install dependencies? → Yes
```

生成されるディレクトリ構成：

```
functions/
├── src/
│   └── index.ts     ← 関数を定義するメインファイル
├── package.json
└── tsconfig.json
```

### 必要なパッケージのインストール

```bash
cd functions
npm install firebase-functions firebase-admin
npm install -D @types/node
```

### Admin SDK の初期化

```typescript
// functions/src/index.ts
import * as admin from 'firebase-admin'

// Admin SDK を初期化（Cloud Functions 内では自動的に認証される）
admin.initializeApp()

const db = admin.firestore()
```

---

## 3. HTTP 関数（API エンドポイント）

クライアントから直接 HTTP リクエストで呼び出せる API を作成します。

```typescript
import { onRequest } from 'firebase-functions/v2/https'

// シンプルな API
export const helloWorld = onRequest((req, res) => {
  res.json({ message: 'Hello from Firebase Functions!' })
})
```

```typescript
// 認証チェック・パラメーター処理付きの例
import { onRequest } from 'firebase-functions/v2/https'

export const getUser = onRequest(async (req, res) => {
  const userId = req.query.userId as string

  if (!userId) {
    res.status(400).json({ error: 'userId は必須です' })
    return
  }

  try {
    const docSnap = await db.collection('users').doc(userId).get()
    if (!docSnap.exists) {
      res.status(404).json({ error: 'ユーザーが見つかりません' })
      return
    }
    res.json({ id: docSnap.id, ...docSnap.data() })
  } catch (error) {
    res.status(500).json({ error: 'サーバーエラーが発生しました' })
  }
})
```

---

## 4. Callable 関数（クライアントから呼び出す推奨方法）

クライアント SDK から呼び出す場合は **Callable 関数** を使うと、**認証・エラーハンドリングが自動化** されるため推奨です。

```typescript
// functions/src/index.ts
import { onCall, HttpsError } from 'firebase-functions/v2/https'

export const createOrder = onCall(async (request) => {
  // 認証チェック（JWT が自動検証される）
  if (!request.auth) {
    throw new HttpsError('unauthenticated', '認証が必要です')
  }

  const { itemId, quantity } = request.data as { itemId: string; quantity: number }

  // バリデーション
  if (!itemId || quantity <= 0) {
    throw new HttpsError('invalid-argument', '不正なパラメータです')
  }

  const userId = request.auth.uid

  await db.collection('orders').add({
    userId,
    itemId,
    quantity,
    status: 'pending',
    createdAt: admin.firestore.FieldValue.serverTimestamp(),
  })

  return { success: true, message: '注文が完了しました' }
})
```

```typescript
// クライアント側の呼び出し方
import { getFunctions, httpsCallable } from 'firebase/functions'

const functions = getFunctions()
const createOrder = httpsCallable(functions, 'createOrder')

const result = await createOrder({ itemId: 'item_001', quantity: 2 })
console.log(result.data) // { success: true, message: '注文が完了しました' }
```

**HTTPS エラーコード一覧：**

| コード | 意味 | HTTP ステータス相当 |
|--------|------|------------------|
| `unauthenticated` | 未認証 | 401 |
| `permission-denied` | 権限なし | 403 |
| `not-found` | リソースが存在しない | 404 |
| `invalid-argument` | 不正なパラメータ | 400 |
| `internal` | サーバー内部エラー | 500 |

---

## 5. Firestore トリガー

Firestore のドキュメントの **作成・更新・削除** を検知して起動する関数です。

```typescript
import {
  onDocumentCreated,
  onDocumentUpdated,
  onDocumentDeleted,
} from 'firebase-functions/v2/firestore'

// ドキュメントが作成されたとき
export const onPostCreated = onDocumentCreated('posts/{postId}', async (event) => {
  const postData = event.data?.data()
  if (!postData) return

  // 例: 投稿者の投稿数をカウントアップ
  await db.collection('users').doc(postData.authorId).update({
    postCount: admin.firestore.FieldValue.increment(1),
  })
})

// ドキュメントが更新されたとき（変更前後のデータを比較できる）
export const onPostUpdated = onDocumentUpdated('posts/{postId}', async (event) => {
  const before = event.data?.before.data()
  const after = event.data?.after.data()
  if (!before || !after) return

  // published フラグが false → true に変わったとき（公開時）
  if (!before.published && after.published) {
    console.log(`投稿が公開されました: ${event.params.postId}`)
    // メール通知などの処理...
  }
})

// ドキュメントが削除されたとき
export const onPostDeleted = onDocumentDeleted('posts/{postId}', async (event) => {
  const postData = event.data?.data()
  if (!postData) return

  // 投稿者の投稿数をカウントダウン
  await db.collection('users').doc(postData.authorId).update({
    postCount: admin.firestore.FieldValue.increment(-1),
  })
})
```

---

## 6. Authentication トリガー

ユーザーの **登録・削除** を検知して起動する関数です。

```typescript
// v1 の書き方（現在も利用可能・安定）
import * as functionsV1 from 'firebase-functions'

// ユーザー登録時: Firestore にプロフィールを自動作成
export const createUserProfile = functionsV1.auth.user().onCreate(async (user) => {
  await db.collection('users').doc(user.uid).set({
    email: user.email ?? null,
    displayName: user.displayName ?? null,
    photoURL: user.photoURL ?? null,
    role: 'user',
    createdAt: admin.firestore.FieldValue.serverTimestamp(),
  })
  console.log(`✅ ユーザープロフィール作成: ${user.uid}`)
})

// ユーザー削除時: 関連データをクリーンアップ
export const deleteUserProfile = functionsV1.auth.user().onDelete(async (user) => {
  // Firestore のユーザーデータを削除
  await db.collection('users').doc(user.uid).delete()

  // Storage のユーザーファイルを削除
  const bucket = admin.storage().bucket()
  await bucket.deleteFiles({ prefix: `users/${user.uid}/` })

  console.log(`✅ ユーザーデータ削除: ${user.uid}`)
})
```

```typescript
// v2 でメールドメインを制限する例（登録前ブロック）
import { beforeUserCreated } from 'firebase-functions/v2/identity'
import { HttpsError } from 'firebase-functions/v2/https'

export const beforeSignUp = beforeUserCreated(async (event) => {
  const user = event.data
  if (!user.email?.endsWith('@company.com')) {
    throw new HttpsError('permission-denied', '社内メールアドレスのみ登録できます')
  }
})
```

---

## 7. スケジュール実行（Cron）

定期的に実行するバッチ処理を設定できます。

```typescript
import { onSchedule } from 'firebase-functions/v2/scheduler'

// 毎日深夜 0 時（日本時間）に実行
export const dailyCleanup = onSchedule(
  {
    schedule: '0 0 * * *', // Cron 式
    timeZone: 'Asia/Tokyo',
  },
  async () => {
    const thirtyDaysAgo = new Date()
    thirtyDaysAgo.setDate(thirtyDaysAgo.getDate() - 30)

    // 30 日以上前の下書きを削除
    const snapshot = await db
      .collection('posts')
      .where('published', '==', false)
      .where('createdAt', '<', thirtyDaysAgo)
      .get()

    const batch = db.batch()
    snapshot.docs.forEach((doc) => batch.delete(doc.ref))
    await batch.commit()

    console.log(`✅ ${snapshot.size} 件の古い下書きを削除しました`)
  }
)
```

**よく使う Cron 式：**

| 式 | 実行タイミング |
|----|-------------|
| `0 * * * *` | 毎時 0 分 |
| `0 9 * * 1-5` | 平日の毎朝 9 時 |
| `0 0 * * *` | 毎日深夜 0 時 |
| `0 0 1 * *` | 毎月 1 日の深夜 0 時 |
| `*/30 * * * *` | 30 分ごと |

---

## 8. Storage トリガー

ファイルの **アップロード・削除** を検知して起動する関数です。

```typescript
import { onObjectFinalized } from 'firebase-functions/v2/storage'
import * as path from 'path'

// 画像アップロード時にサムネイルを生成する例
export const generateThumbnail = onObjectFinalized(async (event) => {
  const filePath = event.data.name       // 例: "users/uid/photo.jpg"
  const contentType = event.data.contentType

  // 画像ファイル以外はスキップ
  if (!contentType?.startsWith('image/')) return
  // すでにサムネイルならスキップ（無限ループ防止）
  if (path.basename(filePath).startsWith('thumb_')) return

  console.log(`サムネイル生成開始: ${filePath}`)
  // sharp 等のライブラリで画像をリサイズする処理...
})
```

---

## 9. 環境変数・シークレットの管理

API キーなどの機密情報は安全に管理します。

### `.env` ファイル（第 2 世代）

```bash
# functions/.env（開発用）
STRIPE_SECRET_KEY=sk_test_...
SENDGRID_API_KEY=SG....

# functions/.env.production（本番用）
STRIPE_SECRET_KEY=sk_live_...
```

```typescript
// 関数内での参照
const stripeKey = process.env.STRIPE_SECRET_KEY
```

### Secret Manager（より安全な方法）

```bash
# シークレットを登録
firebase functions:secrets:set SENDGRID_API_KEY
# → プロンプトで値を入力
```

```typescript
import { onRequest } from 'firebase-functions/v2/https'
import { defineSecret } from 'firebase-functions/params'

const sendgridApiKey = defineSecret('SENDGRID_API_KEY')

export const sendEmail = onRequest(
  { secrets: [sendgridApiKey] }, // 使用するシークレットを宣言
  async (req, res) => {
    const apiKey = sendgridApiKey.value() // 値を取得
    // メール送信処理...
    res.json({ success: true })
  }
)
```

---

## 10. デプロイとローカルテスト

### デプロイ

```bash
# すべての関数をデプロイ
firebase deploy --only functions

# 特定の関数のみデプロイ
firebase deploy --only functions:createOrder,functions:onPostCreated

# 関数の削除
firebase functions:delete createOrder
```

### ローカルエミュレーターでのテスト

```bash
# エミュレーターの起動（Functions + Firestore + Auth）
firebase emulators:start --only functions,firestore,auth

# Callable 関数のテスト（別ターミナルで）
curl -X POST \
  http://127.0.0.1:5001/<PROJECT_ID>/us-central1/createOrder \
  -H "Content-Type: application/json" \
  -d '{"data": {"itemId": "item_001", "quantity": 1}}'
```

---

## 11. よくあるミスとベストプラクティス

### ❌ よくあるミス

```typescript
// ❌ NG: 非同期処理を await しない（関数が途中で終わる）
export const badFunction = onDocumentCreated('posts/{id}', (event) => {
  db.collection('logs').add({ ... }) // await なし！
})

// ❌ NG: Firestore トリガーで自分自身のドキュメントを無条件更新
// → 更新 → トリガー → 更新 → ... の無限ループになる
export const loop = onDocumentUpdated('users/{uid}', async (event) => {
  await event.data?.after.ref.update({ updatedAt: new Date() }) // NG!
})

// ❌ NG: initializeApp() を複数回呼ぶ
// → 関数ファイルを分けた場合、各ファイルで呼ぶと二重初期化エラー
```

### ✅ ベストプラクティス

```typescript
// ✅ OK: 非同期処理は必ず await する
export const goodFunction = onDocumentCreated('posts/{id}', async (event) => {
  await db.collection('logs').add({ ... })
})

// ✅ OK: 無限ループを防ぐ（更新前後のデータを比較する）
export const noLoop = onDocumentUpdated('users/{uid}', async (event) => {
  const before = event.data?.before.data()
  const after = event.data?.after.data()
  if (before?.name === after?.name) return // 変更がなければ終了
  // 処理...
})

// ✅ OK: initializeApp() は index.ts の最上位で 1 回だけ呼ぶ
admin.initializeApp()

// ✅ OK: べき等性を確保（何度実行しても同じ結果になるように）
export const idempotent = onDocumentCreated('orders/{id}', async (event) => {
  const order = event.data?.data()
  if (order?.processed) return // 処理済みならスキップ
  // 処理...
  await event.data?.ref.update({ processed: true })
})
```

---

## 📌 まとめ

| 用途 | 関数の種類 | インポート元 |
|------|-----------|------------|
| HTTP API | `onRequest` | `firebase-functions/v2/https` |
| クライアントから呼び出す | `onCall` | `firebase-functions/v2/https` |
| Firestore の変更を検知 | `onDocumentCreated` 等 | `firebase-functions/v2/firestore` |
| ユーザー登録・削除を検知 | `auth.user().onCreate` 等 | `firebase-functions` (v1) |
| 定期実行 | `onSchedule` | `firebase-functions/v2/scheduler` |
| ファイルアップロードを検知 | `onObjectFinalized` | `firebase-functions/v2/storage` |

---

## 次のステップ

- [Hosting・FCM・その他サービスガイド](07_Hosting・FCM・その他サービスガイド.md) → Web 公開・プッシュ通知・分析
