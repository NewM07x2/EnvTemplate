# 06. Edge Functions ガイド

> **レベル**: ★★★☆☆（中級）  
> **前提知識**: [01_クイックスタート](01_クイックスタート.md)・[02_認証ガイド](02_認証ガイド.md) の完了  
> **所要時間**: 約 50 分

---

## 📚 目次

1. [Edge Functions とは](#1-edge-functions-とは)
2. [ローカル開発環境のセットアップ](#2-ローカル開発環境のセットアップ)
3. [最初の Edge Function を作成する](#3-最初の-edge-function-を作成する)
4. [認証・JWT 検証](#4-認証jwt-検証)
5. [データベースへのアクセス](#5-データベースへのアクセス)
6. [外部 API との連携](#6-外部-api-との連携)
7. [クライアントからの呼び出し](#7-クライアントからの呼び出し)
8. [デプロイ](#8-デプロイ)
9. [よくあるユースケース](#9-よくあるユースケース)

---

## 1. Edge Functions とは

**Edge Functions** は、Supabase が提供する **サーバーレス関数** 機能です。

```
クライアント  →  Supabase Edge Functions  →  外部 API / DB
               （Deno ランタイム）
               （世界中のエッジで実行）
```

### 特徴

| 特徴 | 説明 |
|------|------|
| **Deno ランタイム** | TypeScript をそのまま実行（トランスパイル不要） |
| **エッジ実行** | 世界中の CDN エッジで実行 → 低レイテンシ |
| **サーバーレス** | サーバー管理不要。使った分だけ課金 |
| **環境変数** | 秘密情報をクライアントに漏らさず使える |
| **Deno 標準ライブラリ** | npm パッケージ・Deno モジュールを利用可能 |

### Edge Functions が必要な場面

- 外部 API の秘密キー（決済、SMS 等）を使う処理
- 複雑なビジネスロジック（割引計算、メール送信等）
- Webhook の受信（Stripe、GitHub 等）
- SERVICE_ROLE_KEY が必要な管理者操作
- 定期実行バッチ処理

---

## 2. ローカル開発環境のセットアップ

### Supabase CLI のインストール

```bash
# npm でインストール
npm install supabase --save-dev

# バージョン確認
npx supabase --version
```

### ローカル Supabase の起動

```bash
# プロジェクトを初期化（初回のみ）
npx supabase init

# ローカル環境を起動（Docker が必要）
npx supabase start
```

起動すると以下が利用可能になります：

```
API URL:     http://localhost:54321
DB URL:      postgresql://postgres:postgres@localhost:54322/postgres
Studio URL:  http://localhost:54323
```

---

## 3. 最初の Edge Function を作成する

### 関数の作成

```bash
# Edge Function を新規作成
npx supabase functions new hello-world
```

`supabase/functions/hello-world/index.ts` が生成されます：

```typescript
// supabase/functions/hello-world/index.ts
import { serve } from 'https://deno.land/std@0.177.0/http/server.ts'

serve(async (req) => {
  const { name } = await req.json()

  const data = {
    message: `Hello, ${name ?? 'World'}!`,
    timestamp: new Date().toISOString(),
  }

  return new Response(JSON.stringify(data), {
    headers: { 'Content-Type': 'application/json' },
  })
})
```

### ローカルで実行する

```bash
# 別ターミナルで Edge Function を起動
npx supabase functions serve hello-world --env-file .env.local

# テスト（curl）
curl -X POST http://localhost:54321/functions/v1/hello-world \
  -H "Content-Type: application/json" \
  -d '{"name": "Supabase"}'
```

**レスポンス例:**
```json
{
  "message": "Hello, Supabase!",
  "timestamp": "2026-02-28T00:00:00.000Z"
}
```

---

## 4. 認証・JWT 検証

多くのケースでは、Edge Function を呼び出すユーザーを認証する必要があります。

```typescript
// supabase/functions/protected-action/index.ts
import { serve } from 'https://deno.land/std@0.177.0/http/server.ts'
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'

serve(async (req) => {
  // Authorization ヘッダーから JWT を取得
  const authHeader = req.headers.get('Authorization')
  if (!authHeader) {
    return new Response(JSON.stringify({ error: '認証が必要です' }), {
      status: 401,
      headers: { 'Content-Type': 'application/json' },
    })
  }

  // ユーザーの JWT を使って Supabase クライアントを作成
  // → RLS が正しく適用される
  const supabase = createClient(
    Deno.env.get('SUPABASE_URL') ?? '',
    Deno.env.get('SUPABASE_ANON_KEY') ?? '',
    {
      global: { headers: { Authorization: authHeader } },
    }
  )

  // ユーザーを取得（JWT を検証）
  const { data: { user }, error: authError } = await supabase.auth.getUser()
  if (authError || !user) {
    return new Response(JSON.stringify({ error: '無効なトークンです' }), {
      status: 401,
      headers: { 'Content-Type': 'application/json' },
    })
  }

  // 認証済みユーザーのみが実行できる処理
  return new Response(JSON.stringify({ userId: user.id, email: user.email }), {
    headers: { 'Content-Type': 'application/json' },
  })
})
```

---

## 5. データベースへのアクセス

### ユーザー権限でのアクセス（RLS 適用）

```typescript
// ユーザーの JWT を使う → RLS ポリシーが適用される
const supabase = createClient(
  Deno.env.get('SUPABASE_URL') ?? '',
  Deno.env.get('SUPABASE_ANON_KEY') ?? '',
  { global: { headers: { Authorization: req.headers.get('Authorization')! } } }
)

const { data } = await supabase.from('posts').select('*')
// → ログインユーザーが見えるデータのみ返る（RLS による）
```

### 管理者権限でのアクセス（RLS バイパス）

```typescript
// SERVICE_ROLE_KEY を使う → RLS をバイパス（管理者操作に限定すること）
const adminSupabase = createClient(
  Deno.env.get('SUPABASE_URL') ?? '',
  Deno.env.get('SUPABASE_SERVICE_ROLE_KEY') ?? '' // ← クライアントに渡してはいけない
)

// すべてのユーザーのデータを取得可能
const { data } = await adminSupabase.from('users').select('*')
```

> ⚠️ **SERVICE_ROLE_KEY は Edge Function 内でのみ使うこと。** クライアントに渡すと全データにアクセスできる管理者権限が漏洩します。

---

## 6. 外部 API との連携

Edge Functions は、秘密キーを安全に管理しながら外部 API を呼び出せます。

### メール送信（Resend API の例）

```typescript
// supabase/functions/send-email/index.ts
import { serve } from 'https://deno.land/std@0.177.0/http/server.ts'

serve(async (req) => {
  const { to, subject, html } = await req.json()

  const res = await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${Deno.env.get('RESEND_API_KEY')}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      from: 'no-reply@example.com',
      to,
      subject,
      html,
    }),
  })

  const data = await res.json()

  return new Response(JSON.stringify(data), {
    headers: { 'Content-Type': 'application/json' },
  })
})
```

### Stripe Webhook の受信

```typescript
// supabase/functions/stripe-webhook/index.ts
import { serve } from 'https://deno.land/std@0.177.0/http/server.ts'
import Stripe from 'https://esm.sh/stripe@14.21.0?target=deno'

const stripe = new Stripe(Deno.env.get('STRIPE_SECRET_KEY') ?? '', {
  apiVersion: '2023-10-16',
  httpClient: Stripe.createFetchHttpClient(),
})

serve(async (req) => {
  const signature = req.headers.get('stripe-signature')
  const body = await req.text()

  // Webhook の署名を検証
  let event: Stripe.Event
  try {
    event = await stripe.webhooks.constructEventAsync(
      body,
      signature!,
      Deno.env.get('STRIPE_WEBHOOK_SECRET')!
    )
  } catch (err) {
    return new Response(`Webhook エラー: ${err.message}`, { status: 400 })
  }

  // イベントの種別に応じた処理
  switch (event.type) {
    case 'payment_intent.succeeded':
      const paymentIntent = event.data.object as Stripe.PaymentIntent
      console.log('支払い成功:', paymentIntent.id)
      // DB を更新する処理など
      break

    case 'customer.subscription.deleted':
      // サブスクリプション終了の処理
      break
  }

  return new Response(JSON.stringify({ received: true }), {
    headers: { 'Content-Type': 'application/json' },
  })
})
```

---

## 7. クライアントからの呼び出し

### Next.js / TypeScript から呼び出す

```typescript
// src/lib/supabase/functions.ts
import { createClient } from '@/lib/supabase/client'

// Edge Function を呼び出すユーティリティ
export async function invokeEdgeFunction<T>(
  functionName: string,
  body?: Record<string, unknown>
): Promise<T> {
  const supabase = createClient()

  const { data, error } = await supabase.functions.invoke<T>(functionName, {
    body,
  })

  if (error) throw error
  return data!
}
```

```typescript
// 使用例
import { invokeEdgeFunction } from '@/lib/supabase/functions'

// メール送信
await invokeEdgeFunction('send-email', {
  to: 'user@example.com',
  subject: '登録完了',
  html: '<h1>ようこそ！</h1>',
})

// カスタム計算
const result = await invokeEdgeFunction<{ total: number }>('calculate-discount', {
  userId: 'xxx',
  couponCode: 'SUMMER2026',
})
console.log(result.total)
```

### fetch で直接呼び出す（フレームワーク非依存）

```typescript
const session = await supabase.auth.getSession()
const token = session.data.session?.access_token

const res = await fetch(
  `${process.env.NEXT_PUBLIC_SUPABASE_URL}/functions/v1/hello-world`,
  {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ name: 'User' }),
  }
)

const data = await res.json()
```

---

## 8. デプロイ

### 環境変数の設定

```bash
# 本番環境に環境変数を設定
npx supabase secrets set RESEND_API_KEY=re_xxxxxxxxxxxx
npx supabase secrets set STRIPE_SECRET_KEY=sk_live_xxxx

# 設定済みシークレットの一覧
npx supabase secrets list
```

### 関数のデプロイ

```bash
# 特定の関数をデプロイ
npx supabase functions deploy hello-world

# すべての関数をデプロイ
npx supabase functions deploy

# JWT 検証を無効にする（公開 Webhook 等）
npx supabase functions deploy stripe-webhook --no-verify-jwt
```

### CI/CD での自動デプロイ（GitHub Actions の例）

```yaml
# .github/workflows/deploy-functions.yml
name: Deploy Edge Functions

on:
  push:
    branches: [main]
    paths:
      - 'supabase/functions/**'

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: supabase/setup-cli@v1
        with:
          version: latest

      - name: Deploy functions
        run: npx supabase functions deploy --project-ref ${{ secrets.SUPABASE_PROJECT_REF }}
        env:
          SUPABASE_ACCESS_TOKEN: ${{ secrets.SUPABASE_ACCESS_TOKEN }}
```

---

## 9. よくあるユースケース

### CORS 対応（ブラウザからの呼び出し）

```typescript
// supabase/functions/_shared/cors.ts（共有ヘッダー）
export const corsHeaders = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
}
```

```typescript
// 各関数での CORS 対応
import { corsHeaders } from '../_shared/cors.ts'

serve(async (req) => {
  // OPTIONS リクエストへの対応（プリフライト）
  if (req.method === 'OPTIONS') {
    return new Response('ok', { headers: corsHeaders })
  }

  // 通常の処理...
  return new Response(JSON.stringify(data), {
    headers: { ...corsHeaders, 'Content-Type': 'application/json' },
  })
})
```

### エラーハンドリング

```typescript
serve(async (req) => {
  try {
    // メイン処理
    const result = await doSomething()

    return new Response(JSON.stringify({ data: result }), {
      headers: { 'Content-Type': 'application/json' },
    })
  } catch (error) {
    console.error('Edge Function エラー:', error)

    return new Response(
      JSON.stringify({
        error: error instanceof Error ? error.message : '不明なエラー',
      }),
      {
        status: 500,
        headers: { 'Content-Type': 'application/json' },
      }
    )
  }
})
```

---

## 📌 まとめ

| シナリオ | 実装方法 |
|---------|---------|
| 外部 API キーを使う | Edge Function に秘密キーを設定、クライアントには渡さない |
| メール・SMS 送信 | Edge Function で外部サービスを呼び出す |
| Webhook 受信 | `--no-verify-jwt` で JWT 検証を無効にしてデプロイ |
| 管理者操作 | SERVICE_ROLE_KEY を Edge Function 内でのみ使用 |
| バッチ処理 | Supabase Dashboard から Cron で定期実行 |

---

## 次のステップ

- [マイグレーション管理](07_マイグレーション管理.md) → スキーマ変更を安全に運用する
