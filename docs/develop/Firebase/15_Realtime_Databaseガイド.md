# Realtime Database ガイド

> **レベル**: ★★☆ / 所要時間: 約 30 分  
> **対象**: Realtime Database を使った既存システムの保守・Firebase サービスの使い分けを理解したい方

---

## 目次

1. [Realtime Database とは](#1-realtime-database-とは)
2. [Firestore との使い分け](#2-firestore-との使い分け)
3. [セットアップ](#3-セットアップ)
4. [データの読み書き（基本）](#4-データの読み書き基本)
5. [リアルタイム購読](#5-リアルタイム購読)
6. [オフラインサポート](#6-オフラインサポート)
7. [セキュリティルール](#7-セキュリティルール)
8. [Next.js での利用パターン](#8-nextjs-での利用パターン)
9. [Firestore への移行](#9-firestore-への移行)

---

## 1. Realtime Database とは

Firebase Realtime Database（RTDB）は Firebase の**初代データベース**サービスです。データは1つの大きな **JSON ツリー** として管理され、変更が即座にすべてのクライアントに同期されます。

```
Realtime Database のデータ構造（JSON ツリー）

{
  "users": {
    "uid-alice": { "name": "Alice", "status": "online" },
    "uid-bob":   { "name": "Bob",   "status": "offline" }
  },
  "messages": {
    "room-general": {
      "msg-001": { "text": "Hello!", "uid": "uid-alice", "time": 1700000000 },
      "msg-002": { "text": "Hi!",    "uid": "uid-bob",   "time": 1700000010 }
    }
  }
}
```

### 主な特徴

| 特徴 | 内容 |
|------|------|
| **超低レイテンシ** | ミリ秒単位のリアルタイム同期 |
| **JSON ツリー** | すべてのデータが1つの大きな JSON として管理 |
| **オフライン対応** | オフライン中の変更を自動でキューイング・再同期 |
| **シンプルな API** | Firestore より簡潔な API |
| **リージョン制限** | Firestore より選択できるリージョンが少ない |

---

## 2. Firestore との使い分け

> **新規開発では基本的に Firestore を選択してください。**  
> Realtime Database は既存システムの保守や、特定のユースケースでのみ使用します。

| 比較項目 | Realtime Database | Firestore |
|---------|-----------------|---------|
| **データ構造** | JSON ツリー（1つのルート） | コレクション/ドキュメント |
| **クエリ** | 単純（1フィールドのソート/フィルタ） | 複合クエリ・複数フィールドフィルタ |
| **スケール** | 同時接続数に上限あり | 自動スケール |
| **オフライン** | ✅ 完全サポート | ✅ 完全サポート |
| **レイテンシ** | ⚡ 超低遅延（数ms） | 低遅延（数十ms） |
| **料金** | 接続数・GB 転送量 | 読み書き回数・ストレージ |
| **推奨用途** | プレゼンス管理・チャット | 汎用データ |

### Realtime Database が今でも有効なケース

- **プレゼンス（オンライン状態）管理**: `onDisconnect()` API が強力
- **超低レイテンシが必要なゲームの状態同期**
- **既存の Realtime Database プロジェクトの保守**

---

## 3. セットアップ

### Firebase コンソールでの設定

1. Firebase コンソール → 「Realtime Database」→「データベースを作成」
2. リージョンを選択（`us-central1` または `asia-southeast1`）
3. セキュリティルールを選択（開発時は「テストモード」）

### SDK の初期化

```typescript
// src/lib/firebase/rtdb.ts
import { getApp } from 'firebase/app';
import { getDatabase, connectDatabaseEmulator } from 'firebase/database';

const db = getDatabase(getApp());

// エミュレーター接続（開発環境のみ）
if (
  process.env.NEXT_PUBLIC_USE_FIREBASE_EMULATOR === 'true' &&
  typeof window !== 'undefined'
) {
  connectDatabaseEmulator(db, '127.0.0.1', 9000);
}

export { db as rtdb };
```

### `firebase.json` にエミュレーター設定を追加

```json
{
  "emulators": {
    "database": {
      "port": 9000
    }
  }
}
```

---

## 4. データの読み書き（基本）

```typescript
import { rtdb } from '@/lib/firebase/rtdb';
import { ref, set, get, update, remove, push, child } from 'firebase/database';

// ── 書き込み ──────────────────────────────────────────────
// データを上書き（set）
await set(ref(rtdb, `users/${userId}`), {
  name:   'Alice',
  status: 'online',
});

// データを部分更新（update）
await update(ref(rtdb, `users/${userId}`), {
  status: 'offline',
});

// リストへの追加（push: 一意キーを自動生成）
const newMsgRef = push(ref(rtdb, 'messages/room-general'));
await set(newMsgRef, {
  text: 'Hello!',
  uid:  userId,
  time: Date.now(),
});
console.log('新規メッセージの key:', newMsgRef.key);

// ── 読み取り ──────────────────────────────────────────────
// 一度だけ読み取り
const snapshot = await get(ref(rtdb, `users/${userId}`));
if (snapshot.exists()) {
  console.log(snapshot.val()); // { name: 'Alice', status: 'online' }
}

// 削除
await remove(ref(rtdb, `users/${userId}`));
```

### アトミック操作（トランザクション）

```typescript
import { ref, runTransaction } from 'firebase/database';
import { rtdb } from '@/lib/firebase/rtdb';

// カウンターの競合なし更新
async function incrementLikes(postId: string) {
  const likesRef = ref(rtdb, `posts/${postId}/likes`);

  await runTransaction(likesRef, (currentValue) => {
    return (currentValue ?? 0) + 1; // null の場合は 0 からカウント
  });
}
```

---

## 5. リアルタイム購読

```typescript
import { ref, onValue, onChildAdded, onChildChanged, onChildRemoved, off } from 'firebase/database';
import { rtdb } from '@/lib/firebase/rtdb';

// ── 値全体を監視 ────────────────────────────────────────
const userRef = ref(rtdb, `users/${userId}`);
const unsubscribe = onValue(userRef, (snapshot) => {
  const data = snapshot.val();
  console.log('ユーザーデータ更新:', data);
});
// 購読解除
unsubscribe();

// ── 子要素の追加・変更・削除を個別に監視 ─────────────────
const messagesRef = ref(rtdb, 'messages/room-general');

const unsubAdd = onChildAdded(messagesRef, (snapshot) => {
  console.log('新規メッセージ:', snapshot.key, snapshot.val());
});

const unsubChange = onChildChanged(messagesRef, (snapshot) => {
  console.log('メッセージ変更:', snapshot.key, snapshot.val());
});

const unsubRemove = onChildRemoved(messagesRef, (snapshot) => {
  console.log('メッセージ削除:', snapshot.key);
});
```

### クエリ（並び替え・フィルタ）

```typescript
import { ref, query, orderByChild, equalTo, limitToLast, onValue } from 'firebase/database';
import { rtdb } from '@/lib/firebase/rtdb';

// status が 'online' のユーザーを取得
const onlineUsersRef = query(
  ref(rtdb, 'users'),
  orderByChild('status'),
  equalTo('online')
);
onValue(onlineUsersRef, (snapshot) => {
  snapshot.forEach((child) => {
    console.log(child.key, child.val());
  });
});

// 最新の10件のメッセージを取得
const recentMsgsRef = query(
  ref(rtdb, 'messages/room-general'),
  orderByChild('time'),
  limitToLast(10)
);
```

---

## 6. オフラインサポート

### プレゼンス管理（`onDisconnect`）

Realtime Database の最大の強みはオフライン検知です。

```typescript
import { ref, onDisconnect, onValue, serverTimestamp, set } from 'firebase/database';
import { rtdb } from '@/lib/firebase/rtdb';
import { auth } from '@/lib/firebase/client';

// ユーザーのオンライン状態を管理
async function setupPresence(userId: string) {
  // Firebase が管理するシステムパス（接続状態）
  const connectedRef = ref(rtdb, '.info/connected');
  const userStatusRef = ref(rtdb, `users/${userId}/status`);

  onValue(connectedRef, (snapshot) => {
    if (snapshot.val() === false) return; // まだ接続されていない

    // 切断時に自動で 'offline' に変更する予約
    onDisconnect(userStatusRef)
      .set({
        state:     'offline',
        lastSeen:  serverTimestamp(),
      })
      .then(() => {
        // 予約完了後にオンライン状態を設定
        set(userStatusRef, {
          state:    'online',
          lastSeen: serverTimestamp(),
        });
      });
  });
}
```

### オフライン時のデータ永続化

```typescript
import { getDatabase, enableLogging } from 'firebase/database';
import { initializeApp } from 'firebase/app';

// モバイルアプリや PWA でオフライン時のデータをキャッシュ
// ※ Web SDK では setPersistence は Firestore にしかない
// Realtime Database は自動的にメモリキャッシュを保持する

// デバッグ用ロギング（開発時のみ）
if (process.env.NODE_ENV === 'development') {
  enableLogging(true);
}
```

---

## 7. セキュリティルール

Realtime Database のルールは Firestore とは異なる書式です。

```json
// database.rules.json
{
  "rules": {
    // ── ユーザーデータ ─────────────────────────────────
    "users": {
      "$uid": {
        // 全員が読み取り可能
        ".read": true,
        // 本人のみ書き込み可能
        ".write": "$uid === auth.uid",
        // データの検証
        ".validate": "newData.hasChildren(['name', 'status'])",
        "name": {
          ".validate": "newData.isString() && newData.val().length <= 50"
        },
        "status": {
          ".validate": "newData.val() === 'online' || newData.val() === 'offline'"
        }
      }
    },

    // ── メッセージ ────────────────────────────────────
    "messages": {
      "$roomId": {
        // 認証済みユーザーのみ読み取り可能
        ".read": "auth !== null",
        "$messageId": {
          // 認証済みユーザーのみ書き込み可能
          ".write": "auth !== null",
          ".validate": "newData.hasChildren(['text', 'uid', 'time'])",
          "text": {
            ".validate": "newData.isString() && newData.val().length <= 500"
          },
          "uid": {
            // 送信者は自分自身の uid のみ設定可能
            ".validate": "newData.val() === auth.uid"
          },
          "time": {
            ".validate": "newData.isNumber()"
          }
        }
      }
    }
  }
}
```

### ルールのデプロイ

```bash
firebase deploy --only database
```

---

## 8. Next.js での利用パターン

```tsx
// components/ChatRoom.tsx
'use client';

import { useEffect, useRef, useState } from 'react';
import {
  ref, push, onChildAdded, query,
  orderByChild, limitToLast, set, serverTimestamp,
} from 'firebase/database';
import { rtdb } from '@/lib/firebase/rtdb';
import { auth } from '@/lib/firebase/client';

type Message = { id: string; text: string; uid: string; time: number };

export function ChatRoom({ roomId }: { roomId: string }) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput]       = useState('');
  const bottomRef               = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const messagesRef = query(
      ref(rtdb, `messages/${roomId}`),
      orderByChild('time'),
      limitToLast(50)
    );

    const unsubscribe = onChildAdded(messagesRef, (snapshot) => {
      setMessages((prev) => [
        ...prev,
        { id: snapshot.key!, ...(snapshot.val() as Omit<Message, 'id'>) },
      ]);
      // 最新メッセージへスクロール
      bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
    });

    return () => unsubscribe();
  }, [roomId]);

  async function sendMessage() {
    if (!input.trim() || !auth.currentUser) return;

    await push(ref(rtdb, `messages/${roomId}`), {
      text: input,
      uid:  auth.currentUser.uid,
      time: serverTimestamp(),
    });
    setInput('');
  }

  return (
    <div>
      <div style={{ height: '400px', overflowY: 'scroll' }}>
        {messages.map((msg) => (
          <div key={msg.id}>
            <span>{msg.text}</span>
          </div>
        ))}
        <div ref={bottomRef} />
      </div>
      <input
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
        placeholder="メッセージを入力..."
      />
      <button onClick={sendMessage}>送信</button>
    </div>
  );
}
```

---

## 9. Firestore への移行

Realtime Database から Firestore へ移行する際の対応表です。

### API 対応表

| Realtime Database | Firestore | 備考 |
|-----------------|---------|------|
| `set(ref, data)` | `setDoc(docRef, data)` | |
| `update(ref, data)` | `updateDoc(docRef, data)` | |
| `remove(ref)` | `deleteDoc(docRef)` | |
| `push(ref, data)` | `addDoc(collection, data)` | Firestore は自動 ID 生成 |
| `onValue(ref, cb)` | `onSnapshot(docRef, cb)` | |
| `onChildAdded(ref, cb)` | `onSnapshot(query, cb)` + 差分検出 | |
| `runTransaction(ref, cb)` | `runTransaction(db, cb)` | |
| `onDisconnect()` | ❌ なし | Firestore に同等機能はない |
| `serverTimestamp()` | `serverTimestamp()` | import 元が異なる |

### 移行スクリプト例

```typescript
// scripts/migrate-rtdb-to-firestore.ts
import { getDatabase, ref, get } from 'firebase-admin/database';
import { getFirestore, Timestamp } from 'firebase-admin/firestore';
// ... initializeApp

const rtdb = getDatabase();
const firestore = getFirestore();

async function migrateMessages(roomId: string) {
  const snapshot = await get(ref(rtdb, `messages/${roomId}`));
  if (!snapshot.exists()) return;

  const messages = snapshot.val() as Record<string, {
    text: string; uid: string; time: number;
  }>;

  let batch = firestore.batch();
  let count = 0;

  for (const [key, msg] of Object.entries(messages)) {
    const docRef = firestore.collection(`rooms/${roomId}/messages`).doc(key);
    batch.set(docRef, {
      text:      msg.text,
      authorId:  msg.uid,
      createdAt: Timestamp.fromMillis(msg.time),
    });
    count++;
    if (count % 500 === 0) {
      await batch.commit();
      batch = firestore.batch();
    }
  }
  if (count % 500 !== 0) await batch.commit();
  console.log(`✅ ${roomId}: ${count} 件移行完了`);
}
```

---

## まとめ

| 項目 | 内容 |
|------|------|
| 新規開発 | **Firestore を使用**（Realtime Database より機能が充実） |
| プレゼンス管理 | Realtime Database の `onDisconnect()` が最適 |
| 超低レイテンシ | Realtime Database が有利（数ms vs 数十ms） |
| 既存システム保守 | 現行のまま Realtime Database を使い続けるのも合理的 |
| 移行 | API の対応表を参考に段階的に移行 |

---

## 次のステップ

- [Firestore（データベース）ガイド](04_Firestore（データベース）ガイド.md) — 新規開発での標準 DB
- [マイグレーション・データ移行ガイド](13_マイグレーション・データ移行ガイド.md) — Firestore への移行方法
