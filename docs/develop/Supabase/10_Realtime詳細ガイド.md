# 10. Realtime 詳細ガイド

> **レベル**: ★★★☆☆（中級）  
> **前提知識**: [01_クイックスタート](01_クイックスタート.md)・[03_REST_APIガイド](03_REST_APIガイド.md) の完了  
> **所要時間**: 約 50 分

---

## 📚 目次

1. [Supabase Realtime とは](#1-supabase-realtime-とは)
2. [3 つの機能の概要](#2-3-つの機能の概要)
3. [Postgres Changes（DB 変更の購読）](#3-postgres-changesdb-変更の購読)
4. [Broadcast（任意のメッセージ送受信）](#4-broadcast任意のメッセージ送受信)
5. [Presence（オンライン状態の共有）](#5-presenceオンライン状態の共有)
6. [チャンネルの管理](#6-チャンネルの管理)
7. [実装例：リアルタイムチャット](#7-実装例リアルタイムチャット)
8. [実装例：オンラインユーザー一覧](#8-実装例オンラインユーザー一覧)
9. [パフォーマンスとベストプラクティス](#9-パフォーマンスとベストプラクティス)

---

## 1. Supabase Realtime とは

**Supabase Realtime** は、**WebSocket を使ってサーバーからクライアントへリアルタイムにデータを配信**する機能です。

```
仕組み:

クライアント A ──WebSocket── Supabase Realtime サーバー
クライアント B ──WebSocket──         │
クライアント C ──WebSocket──         │
                              ┌──────┘
                         PostgreSQL DB
                         （変更を検知）
```

ポーリング（定期的な API 呼び出し）とは異なり、変更があったときだけ通知されるため、**効率的かつ低レイテンシ**でリアルタイム性を実現できます。

---

## 2. 3 つの機能の概要

| 機能 | 用途 | 仕組み |
|------|------|--------|
| **Postgres Changes** | DB テーブルの変更を受け取る | PostgreSQL の WAL（Write-Ahead Log）を監視 |
| **Broadcast** | クライアント間で任意のメッセージを送受信 | Supabase サーバーが中継 |
| **Presence** | 接続中のユーザーの状態を共有 | 各クライアントの状態をサーバーが集約 |

---

## 3. Postgres Changes（DB 変更の購読）

DB テーブルへの INSERT・UPDATE・DELETE をリアルタイムで受け取ります。

### 有効化（テーブルの Replication を設定）

```sql
-- Supabase Console > Database > Replication で設定するか、SQL で実行
ALTER PUBLICATION supabase_realtime ADD TABLE public.messages;
ALTER PUBLICATION supabase_realtime ADD TABLE public.posts;
```

または Supabase Console > **Database** > **Replication** > テーブルを選択して有効化。

### 基本的な購読

```typescript
import { createClient } from '@/lib/supabase/client'

const supabase = createClient()

// INSERT イベントを購読
const channel = supabase
  .channel('messages-changes')  // チャンネル名（任意の文字列）
  .on(
    'postgres_changes',
    {
      event: 'INSERT',        // 'INSERT' | 'UPDATE' | 'DELETE' | '*'
      schema: 'public',
      table: 'messages',
    },
    (payload) => {
      console.log('新しいメッセージ:', payload.new)
    }
  )
  .subscribe()

// 購読を停止（コンポーネントのアンマウント時）
supabase.removeChannel(channel)
```

### すべてのイベントを購読

```typescript
const channel = supabase
  .channel('posts-all-changes')
  .on(
    'postgres_changes',
    { event: '*', schema: 'public', table: 'posts' },
    (payload) => {
      switch (payload.eventType) {
        case 'INSERT':
          console.log('追加:', payload.new)
          break
        case 'UPDATE':
          console.log('変更前:', payload.old)
          console.log('変更後:', payload.new)
          break
        case 'DELETE':
          console.log('削除:', payload.old)
          break
      }
    }
  )
  .subscribe()
```

### フィルタリング（特定の行だけ購読）

```typescript
// room_id が特定の値の行だけ受け取る
const channel = supabase
  .channel('room-messages')
  .on(
    'postgres_changes',
    {
      event: 'INSERT',
      schema: 'public',
      table: 'messages',
      filter: 'room_id=eq.room_001',  // フィルタ条件
    },
    (payload) => {
      console.log('ルームへの新着メッセージ:', payload.new)
    }
  )
  .subscribe()
```

### 利用できるフィルタ

| フィルタ | 例 | 説明 |
|---------|-----|------|
| `eq` | `user_id=eq.xxx` | 等値 |
| `neq` | `status=neq.deleted` | 不等値 |
| `lt` / `lte` | `price=lt.1000` | 未満 / 以下 |
| `gt` / `gte` | `price=gt.500` | より大きい / 以上 |
| `in` | `status=in.(active,pending)` | いずれかに一致 |

> ⚠️ **RLS に注意**: Postgres Changes は RLS ポリシーを尊重します。ユーザーが SELECT できないデータは変更通知も届きません。

---

## 4. Broadcast（任意のメッセージ送受信）

DB を経由せずに、**クライアント間で任意のメッセージをリアルタイムに送受信**できます。  
カーソルの位置・タイピング状態・ゲームの操作など、DB に保存する必要がないイベントに適しています。

### 送信と受信

```typescript
// チャンネルを作成して参加
const channel = supabase.channel('cursor-positions')

// メッセージの受信（subscribe 前に登録）
channel.on(
  'broadcast',
  { event: 'cursor_move' },
  (payload) => {
    console.log('カーソル位置を受信:', payload.payload)
    // payload.payload = { userId: 'xxx', x: 120, y: 340 }
  }
)

// チャンネルに参加
await channel.subscribe()

// メッセージを送信（参加後に実行）
await channel.send({
  type: 'broadcast',
  event: 'cursor_move',
  payload: {
    userId: currentUserId,
    x: mouseX,
    y: mouseY,
  },
})
```

### マウスカーソル共有の例

```typescript
'use client'

import { useEffect, useState, useRef } from 'react'
import { createClient } from '@/lib/supabase/client'

type CursorPosition = { userId: string; x: number; y: number }

export function CollaborativeCanvas({ roomId }: { roomId: string }) {
  const [cursors, setCursors] = useState<Record<string, CursorPosition>>({})
  const channelRef = useRef<ReturnType<typeof supabase.channel> | null>(null)
  const supabase = createClient()

  useEffect(() => {
    const channel = supabase.channel(`cursor-${roomId}`)

    channel
      .on('broadcast', { event: 'cursor' }, ({ payload }) => {
        setCursors((prev) => ({
          ...prev,
          [payload.userId]: payload,
        }))
      })
      .subscribe()

    channelRef.current = channel

    return () => {
      supabase.removeChannel(channel)
    }
  }, [roomId])

  const handleMouseMove = async (e: React.MouseEvent) => {
    await channelRef.current?.send({
      type: 'broadcast',
      event: 'cursor',
      payload: { userId: 'my-user-id', x: e.clientX, y: e.clientY },
    })
  }

  return (
    <div className="w-full h-screen relative" onMouseMove={handleMouseMove}>
      {Object.values(cursors).map((cursor) => (
        <div
          key={cursor.userId}
          className="absolute w-4 h-4 rounded-full bg-blue-500 pointer-events-none"
          style={{ left: cursor.x, top: cursor.y }}
        />
      ))}
    </div>
  )
}
```

---

## 5. Presence（オンライン状態の共有）

**接続中のすべてのクライアントの状態**（オンライン・閲覧ページ等）をリアルタイムで共有できます。

```typescript
'use client'

import { useEffect, useState } from 'react'
import { createClient } from '@/lib/supabase/client'

type UserPresence = {
  userId: string
  username: string
  onlineAt: string
}

export function OnlineUsers({ roomId }: { roomId: string }) {
  const [onlineUsers, setOnlineUsers] = useState<UserPresence[]>([])
  const supabase = createClient()

  useEffect(() => {
    const channel = supabase.channel(`room-presence-${roomId}`)

    channel
      // 参加・退出・更新イベントを購読
      .on('presence', { event: 'sync' }, () => {
        // 現在の全参加者の状態を取得
        const state = channel.presenceState<UserPresence>()
        const users = Object.values(state).flat()
        setOnlineUsers(users)
      })
      .on('presence', { event: 'join' }, ({ newPresences }) => {
        console.log('参加:', newPresences)
      })
      .on('presence', { event: 'leave' }, ({ leftPresences }) => {
        console.log('退出:', leftPresences)
      })
      .subscribe(async (status) => {
        if (status === 'SUBSCRIBED') {
          // 自分の状態を登録
          await channel.track({
            userId: 'current-user-id',
            username: 'ユーザー名',
            onlineAt: new Date().toISOString(),
          })
        }
      })

    return () => {
      supabase.removeChannel(channel)
    }
  }, [roomId])

  return (
    <div>
      <p>オンライン: {onlineUsers.length} 人</p>
      <ul>
        {onlineUsers.map((user) => (
          <li key={user.userId}>{user.username}</li>
        ))}
      </ul>
    </div>
  )
}
```

---

## 6. チャンネルの管理

### 購読状態の確認

```typescript
const channel = supabase
  .channel('my-channel')
  .on('postgres_changes', { event: '*', schema: 'public', table: 'posts' }, () => {})
  .subscribe((status, error) => {
    switch (status) {
      case 'SUBSCRIBED':
        console.log('接続成功')
        break
      case 'CHANNEL_ERROR':
        console.error('接続エラー:', error)
        break
      case 'TIMED_OUT':
        console.warn('接続タイムアウト')
        break
      case 'CLOSED':
        console.log('接続終了')
        break
    }
  })
```

### 再接続の実装

```typescript
// ネットワーク切断時の再接続
function subscribeWithRetry(tableName: string, callback: (payload: unknown) => void) {
  let retryCount = 0
  const maxRetries = 5

  function createSubscription() {
    return supabase
      .channel(`${tableName}-${Date.now()}`)
      .on('postgres_changes', { event: '*', schema: 'public', table: tableName }, callback)
      .subscribe((status) => {
        if (status === 'CHANNEL_ERROR' && retryCount < maxRetries) {
          retryCount++
          const delay = Math.min(1000 * 2 ** retryCount, 30000)  // 指数バックオフ
          console.log(`${delay}ms 後に再接続 (${retryCount}/${maxRetries})`)
          setTimeout(() => createSubscription(), delay)
        }
      })
  }

  return createSubscription()
}
```

---

## 7. 実装例：リアルタイムチャット

```typescript
'use client'

import { useEffect, useState, useRef } from 'react'
import { createClient } from '@/lib/supabase/client'

type Message = {
  id: string
  user_id: string
  room_id: string
  content: string
  created_at: string
  profiles: { display_name: string; avatar_url: string | null }
}

export function ChatRoom({ roomId, currentUserId }: { roomId: string; currentUserId: string }) {
  const [messages, setMessages] = useState<Message[]>([])
  const [newMessage, setNewMessage] = useState('')
  const [sending, setSending] = useState(false)
  const bottomRef = useRef<HTMLDivElement>(null)
  const supabase = createClient()

  // 初回: 過去のメッセージを取得
  useEffect(() => {
    const fetchMessages = async () => {
      const { data } = await supabase
        .from('messages')
        .select('*, profiles(display_name, avatar_url)')
        .eq('room_id', roomId)
        .order('created_at', { ascending: true })
        .limit(50)

      if (data) setMessages(data as Message[])
    }

    fetchMessages()
  }, [roomId])

  // リアルタイム購読
  useEffect(() => {
    const channel = supabase
      .channel(`chat-${roomId}`)
      .on(
        'postgres_changes',
        {
          event: 'INSERT',
          schema: 'public',
          table: 'messages',
          filter: `room_id=eq.${roomId}`,
        },
        async (payload) => {
          // 新着メッセージにプロフィール情報を JOIN して追加
          const { data } = await supabase
            .from('messages')
            .select('*, profiles(display_name, avatar_url)')
            .eq('id', payload.new.id)
            .single()

          if (data) {
            setMessages((prev) => [...prev, data as Message])
          }
        }
      )
      .subscribe()

    return () => {
      supabase.removeChannel(channel)
    }
  }, [roomId])

  // メッセージが追加されたら末尾にスクロール
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const sendMessage = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!newMessage.trim() || sending) return

    setSending(true)
    const { error } = await supabase.from('messages').insert({
      room_id: roomId,
      user_id: currentUserId,
      content: newMessage.trim(),
    })

    if (!error) setNewMessage('')
    setSending(false)
  }

  return (
    <div className="flex flex-col h-screen">
      {/* メッセージ一覧 */}
      <div className="flex-1 overflow-y-auto p-4 space-y-2">
        {messages.map((msg) => (
          <div
            key={msg.id}
            className={`flex gap-2 ${msg.user_id === currentUserId ? 'flex-row-reverse' : ''}`}
          >
            <div className="max-w-xs bg-white rounded-lg p-3 shadow-sm">
              <p className="text-xs text-gray-500">{msg.profiles?.display_name}</p>
              <p>{msg.content}</p>
            </div>
          </div>
        ))}
        <div ref={bottomRef} />
      </div>

      {/* 入力フォーム */}
      <form onSubmit={sendMessage} className="p-4 border-t flex gap-2">
        <input
          value={newMessage}
          onChange={(e) => setNewMessage(e.target.value)}
          placeholder="メッセージを入力..."
          className="flex-1 border rounded-lg px-3 py-2"
          disabled={sending}
        />
        <button
          type="submit"
          disabled={sending || !newMessage.trim()}
          className="bg-blue-500 text-white px-4 py-2 rounded-lg disabled:opacity-50"
        >
          送信
        </button>
      </form>
    </div>
  )
}
```

---

## 8. 実装例：オンラインユーザー一覧

```typescript
'use client'

import { useEffect, useState } from 'react'
import { createClient } from '@/lib/supabase/client'
import { useUser } from '@/hooks/useUser'

type PresenceUser = {
  userId: string
  username: string
  avatarUrl?: string
  currentPage?: string
}

export function OnlineUsersSidebar() {
  const { user } = useUser()
  const [onlineUsers, setOnlineUsers] = useState<PresenceUser[]>([])
  const supabase = createClient()

  useEffect(() => {
    if (!user) return

    const channel = supabase.channel('global-presence')

    channel
      .on('presence', { event: 'sync' }, () => {
        const state = channel.presenceState<PresenceUser>()
        setOnlineUsers(Object.values(state).flat())
      })
      .subscribe(async (status) => {
        if (status === 'SUBSCRIBED') {
          await channel.track({
            userId: user.id,
            username: user.email ?? '匿名',
            currentPage: window.location.pathname,
          })
        }
      })

    return () => {
      supabase.removeChannel(channel)
    }
  }, [user])

  return (
    <aside className="w-64 p-4">
      <h3 className="font-semibold mb-3">
        オンライン <span className="text-green-500">● {onlineUsers.length}</span>
      </h3>
      <ul className="space-y-2">
        {onlineUsers.map((u) => (
          <li key={u.userId} className="flex items-center gap-2 text-sm">
            <span className="w-2 h-2 bg-green-400 rounded-full" />
            {u.username}
          </li>
        ))}
      </ul>
    </aside>
  )
}
```

---

## 9. パフォーマンスとベストプラクティス

### チャンネル数を抑える

```typescript
// ❌ 複数のチャンネルを無駄に作る
const ch1 = supabase.channel('posts').on(...)
const ch2 = supabase.channel('comments').on(...)

// ✅ 1 つのチャンネルに複数の購読をまとめる（接続数を節約）
const channel = supabase
  .channel('room-updates')
  .on('postgres_changes', { event: '*', schema: 'public', table: 'posts' }, handlePost)
  .on('postgres_changes', { event: '*', schema: 'public', table: 'comments' }, handleComment)
  .subscribe()
```

### 必ずクリーンアップを実装する

```typescript
useEffect(() => {
  const channel = supabase.channel('my-channel').on(...).subscribe()

  // ❌ クリーンアップを忘れると接続が増え続ける
  // return () => {} // 空の return は NG

  // ✅ コンポーネントアンマウント時に必ず削除
  return () => {
    supabase.removeChannel(channel)
  }
}, [])
```

### フリープランの制限

| 制限 | 上限 |
|------|------|
| 同時接続数 | 200 |
| チャンネル数（接続ごと） | 100 |
| メッセージ数 | 200 万 / 月 |

---

## 📌 まとめ

| 機能 | 使う場面 |
|------|---------|
| **Postgres Changes** | DB のデータ変更をリアルタイムで受け取る（通知・チャット等） |
| **Broadcast** | DB に保存しない一時的なメッセージ（カーソル位置・タイピング状態等） |
| **Presence** | 接続中ユーザーの状態を全員で共有（オンライン一覧・編集中表示等） |

---

## 次のステップ

- [Vector / AI 機能ガイド](11_Vector_AI機能ガイド.md) → pgvector を使った AI 検索の実装
