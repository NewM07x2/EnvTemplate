# 11. Vector / AI 機能ガイド（pgvector）

> **レベル**: ★★★★☆（上級）  
> **前提知識**: [01_クイックスタート](01_クイックスタート.md)・[08_PostgreSQL機能ガイド](08_PostgreSQL機能ガイド.md) の完了  
> **所要時間**: 約 60 分

---

## 📚 目次

1. [pgvector とは](#1-pgvector-とは)
2. [pgvector の有効化](#2-pgvector-の有効化)
3. [ベクトルデータの保存](#3-ベクトルデータの保存)
4. [類似度検索](#4-類似度検索)
5. [埋め込み（Embedding）の生成](#5-埋め込みembeddingの生成)
6. [RAG（検索拡張生成）の実装](#6-rag検索拡張生成の実装)
7. [Next.js + Supabase + OpenAI の統合例](#7-nextjs--supabase--openai-の統合例)
8. [インデックスとパフォーマンス](#8-インデックスとパフォーマンス)
9. [Supabase AI Helpers](#9-supabase-ai-helpers)

---

## 1. pgvector とは

**pgvector** は PostgreSQL の拡張機能で、**ベクトルデータ（多次元の数値配列）を保存・検索**できます。

### ベクトルと AI の関係

AI モデル（OpenAI など）は、テキスト・画像・音声などを**数値の配列（埋め込み / Embedding）** に変換できます。  
意味が近いテキストほど、ベクトルが近い位置に来る性質があります。

```
「犬が走る」  → [0.12, -0.34, 0.89, ...]  ← 近い
「猫が走る」  → [0.11, -0.30, 0.91, ...]  ← 近い
「経済成長率」→ [0.87,  0.22, -0.51, ...] ← 遠い
```

この性質を使って：
- **類似文書の検索**（FAQ・ドキュメント検索）
- **レコメンド**（類似商品・関連記事）
- **RAG**（AI が自社データを参照して回答する仕組み）

が実装できます。

---

## 2. pgvector の有効化

Supabase のプロジェクトでは pgvector がプリインストールされています。SQL で有効化するだけです。

```sql
-- Supabase Dashboard > SQL Editor で実行
CREATE EXTENSION IF NOT EXISTS vector;
```

確認：

```sql
SELECT * FROM pg_extension WHERE extname = 'vector';
```

---

## 3. ベクトルデータの保存

### テーブル定義

```sql
-- ドキュメント（FAQ・マニュアル等）のテーブル
CREATE TABLE documents (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  content     TEXT NOT NULL,                          -- 元のテキスト
  metadata    JSONB,                                  -- タイトル・カテゴリ等
  embedding   VECTOR(1536),                           -- OpenAI text-embedding-3-small の次元数
  created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
```

> **次元数の目安**  
> | モデル | 次元数 |  
> |--------|--------|  
> | OpenAI `text-embedding-3-small` | 1536 |  
> | OpenAI `text-embedding-3-large` | 3072 |  
> | OpenAI `text-embedding-ada-002` | 1536 |  
> | Google `text-embedding-004` | 768 |  
> | Cohere `embed-multilingual-v3.0` | 1024 |

### データの挿入

```typescript
import { createClient } from '@supabase/supabase-js'
import OpenAI from 'openai'

const supabase = createClient(process.env.SUPABASE_URL!, process.env.SUPABASE_SERVICE_ROLE_KEY!)
const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY! })

async function storeDocument(content: string, metadata: Record<string, unknown>) {
  // 1. テキストを埋め込みベクトルに変換
  const embeddingResponse = await openai.embeddings.create({
    model: 'text-embedding-3-small',
    input: content,
  })
  const embedding = embeddingResponse.data[0].embedding

  // 2. Supabase に保存
  const { data, error } = await supabase.from('documents').insert({
    content,
    metadata,
    embedding,  // number[] をそのまま渡す
  })

  if (error) throw error
  return data
}

// 使用例
await storeDocument('Supabase は PostgreSQL ベースの BaaS です。', {
  title: 'Supabase 概要',
  category: 'intro',
})
```

---

## 4. 類似度検索

### 3 種類の距離計算方法

| 演算子 | 意味 | 特徴 |
|--------|------|------|
| `<->` | L2 距離（ユークリッド距離） | 一般的な「距離」 |
| `<#>` | 内積（Inner Product） | 正規化済みベクトルに適する |
| `<=>` | コサイン距離 | テキスト類似度に最も適する |

### SQL による類似度検索

```sql
-- クエリベクトルに近いドキュメントを上位 5 件取得
SELECT
  id,
  content,
  metadata,
  1 - (embedding <=> '[0.12, -0.34, 0.89, ...]'::vector) AS similarity
FROM documents
ORDER BY embedding <=> '[0.12, -0.34, 0.89, ...]'::vector
LIMIT 5;
```

### PostgreSQL 関数として定義（推奨）

```sql
CREATE OR REPLACE FUNCTION match_documents(
  query_embedding VECTOR(1536),
  match_threshold FLOAT  DEFAULT 0.5,
  match_count     INT    DEFAULT 5
)
RETURNS TABLE (
  id         UUID,
  content    TEXT,
  metadata   JSONB,
  similarity FLOAT
)
LANGUAGE SQL STABLE
AS $$
  SELECT
    id,
    content,
    metadata,
    1 - (embedding <=> query_embedding) AS similarity
  FROM documents
  WHERE 1 - (embedding <=> query_embedding) > match_threshold
  ORDER BY embedding <=> query_embedding
  LIMIT match_count;
$$;
```

### TypeScript から呼び出す

```typescript
async function searchDocuments(queryText: string, matchCount = 5) {
  // クエリをベクトルに変換
  const { data: embeddingData } = await openai.embeddings.create({
    model: 'text-embedding-3-small',
    input: queryText,
  })
  const queryEmbedding = embeddingData[0].embedding

  // Supabase の関数を呼び出す
  const { data, error } = await supabase.rpc('match_documents', {
    query_embedding: queryEmbedding,
    match_threshold: 0.5,
    match_count: matchCount,
  })

  if (error) throw error
  return data  // { id, content, metadata, similarity }[]
}

// 使用例
const results = await searchDocuments('Supabase の認証方法を教えて')
console.log(results)
```

---

## 5. 埋め込み（Embedding）の生成

### バッチ処理でまとめて変換

```typescript
// 複数ドキュメントを一括で埋め込み
async function batchStoreDocuments(
  documents: Array<{ content: string; metadata: Record<string, unknown> }>
) {
  // テキストをまとめてバッチ処理（API コールを削減）
  const { data: embeddingData } = await openai.embeddings.create({
    model: 'text-embedding-3-small',
    input: documents.map((d) => d.content),  // 配列で渡す
  })

  const rows = documents.map((doc, i) => ({
    content: doc.content,
    metadata: doc.metadata,
    embedding: embeddingData[i].embedding,
  }))

  // Supabase に一括挿入
  const { error } = await supabase.from('documents').insert(rows)
  if (error) throw error
}
```

### テキストの前処理

長いドキュメントは**チャンキング（分割）**してから保存します。

```typescript
// 文書をチャンクに分割するユーティリティ
function splitIntoChunks(text: string, chunkSize = 500, overlap = 50): string[] {
  const chunks: string[] = []
  let start = 0

  while (start < text.length) {
    const end = Math.min(start + chunkSize, text.length)
    chunks.push(text.slice(start, end))
    start += chunkSize - overlap  // オーバーラップにより文脈を保持
  }

  return chunks
}

// 長いドキュメントを分割して保存
async function storeLargeDocument(fullText: string, documentTitle: string) {
  const chunks = splitIntoChunks(fullText)

  const documents = chunks.map((chunk, i) => ({
    content: chunk,
    metadata: { title: documentTitle, chunkIndex: i, totalChunks: chunks.length },
  }))

  await batchStoreDocuments(documents)
}
```

---

## 6. RAG（検索拡張生成）の実装

**RAG（Retrieval Augmented Generation）** は、AI が回答を生成する際に自社データを参照させる手法です。

```
ユーザーの質問
     ↓
1. 質問をベクトル化
     ↓
2. Supabase で類似ドキュメントを検索
     ↓
3. 検索結果 + 質問を OpenAI に送信
     ↓
4. AI が自社データに基づいて回答
```

### Edge Function での実装

```typescript
// supabase/functions/ask/index.ts
import { createClient } from '@supabase/supabase-js'
import OpenAI from 'openai'

const supabase = createClient(
  Deno.env.get('SUPABASE_URL')!,
  Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!
)
const openai = new OpenAI({ apiKey: Deno.env.get('OPENAI_API_KEY')! })

Deno.serve(async (req) => {
  if (req.method === 'OPTIONS') {
    return new Response(null, {
      headers: { 'Access-Control-Allow-Origin': '*', 'Access-Control-Allow-Headers': '*' },
    })
  }

  const { question } = await req.json()

  // ステップ 1: 質問をベクトル化
  const { data: embeddingData } = await openai.embeddings.create({
    model: 'text-embedding-3-small',
    input: question,
  })
  const queryEmbedding = embeddingData[0].embedding

  // ステップ 2: 類似ドキュメントを検索
  const { data: documents, error } = await supabase.rpc('match_documents', {
    query_embedding: queryEmbedding,
    match_threshold: 0.5,
    match_count: 3,
  })

  if (error) throw error

  // ステップ 3: コンテキストを作成
  const context = documents
    .map((doc: { content: string }) => doc.content)
    .join('\n\n---\n\n')

  // ステップ 4: OpenAI に質問 + コンテキストを送信
  const completion = await openai.chat.completions.create({
    model: 'gpt-4o-mini',
    messages: [
      {
        role: 'system',
        content: `あなたは親切なアシスタントです。
以下のコンテキストに基づいて質問に回答してください。
コンテキストにない情報は「情報がありません」と答えてください。

コンテキスト:
${context}`,
      },
      { role: 'user', content: question },
    ],
    temperature: 0.2,
  })

  const answer = completion.choices[0].message.content

  return new Response(
    JSON.stringify({ answer, sources: documents }),
    {
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
      },
    }
  )
})
```

---

## 7. Next.js + Supabase + OpenAI の統合例

### API Route（Server Side）

```typescript
// app/api/chat/route.ts
import { NextRequest, NextResponse } from 'next/server'
import { createClient } from '@/lib/supabase/server'
import OpenAI from 'openai'

const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY! })

export async function POST(req: NextRequest) {
  const supabase = await createClient()
  const { question } = await req.json()

  // 埋め込みベクトル生成
  const { data: embed } = await openai.embeddings.create({
    model: 'text-embedding-3-small',
    input: question,
  })

  // 類似ドキュメントを検索
  const { data: docs } = await supabase.rpc('match_documents', {
    query_embedding: embed[0].embedding,
    match_threshold: 0.5,
    match_count: 5,
  })

  const context = (docs as Array<{ content: string }>)
    ?.map((d) => d.content)
    .join('\n\n')

  // ストリーミングで回答を返す
  const stream = await openai.chat.completions.create({
    model: 'gpt-4o-mini',
    stream: true,
    messages: [
      {
        role: 'system',
        content: `以下のコンテキストに基づいて回答してください:\n\n${context}`,
      },
      { role: 'user', content: question },
    ],
  })

  // ReadableStream に変換してストリーミングレスポンス
  const readable = new ReadableStream({
    async start(controller) {
      for await (const chunk of stream) {
        const text = chunk.choices[0]?.delta?.content ?? ''
        controller.enqueue(new TextEncoder().encode(text))
      }
      controller.close()
    },
  })

  return new NextResponse(readable, {
    headers: { 'Content-Type': 'text/plain; charset=utf-8' },
  })
}
```

### フロントエンドコンポーネント

```typescript
'use client'

import { useState } from 'react'

export function AIChat() {
  const [question, setQuestion] = useState('')
  const [answer, setAnswer] = useState('')
  const [loading, setLoading] = useState(false)

  const askQuestion = async () => {
    if (!question.trim()) return

    setLoading(true)
    setAnswer('')

    const res = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question }),
    })

    // ストリーミングレスポンスを受け取る
    const reader = res.body!.getReader()
    const decoder = new TextDecoder()

    while (true) {
      const { done, value } = await reader.read()
      if (done) break
      setAnswer((prev) => prev + decoder.decode(value))
    }

    setLoading(false)
  }

  return (
    <div className="p-4 space-y-4">
      <div className="flex gap-2">
        <input
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && askQuestion()}
          placeholder="質問を入力..."
          className="flex-1 border rounded px-3 py-2"
        />
        <button
          onClick={askQuestion}
          disabled={loading}
          className="bg-blue-500 text-white px-4 py-2 rounded disabled:opacity-50"
        >
          {loading ? '回答中...' : '質問する'}
        </button>
      </div>

      {answer && (
        <div className="bg-gray-50 rounded p-4 whitespace-pre-wrap">
          {answer}
        </div>
      )}
    </div>
  )
}
```

---

## 8. インデックスとパフォーマンス

大量のベクトルデータを高速に検索するために**近似最近傍（ANN）インデックス**を作成します。

### IVFFlat インデックス（推奨：〜100 万件）

```sql
-- 10 万〜100 万件に適したインデックス
-- lists の目安 = データ件数 / 1000（最大 = sqrt(データ件数)）
CREATE INDEX ON documents
  USING ivfflat (embedding vector_cosine_ops)
  WITH (lists = 100);
```

### HNSW インデックス（推奨：高精度・〜数百万件）

```sql
-- 精度が高く更新にも強いインデックス（pgvector 0.5.0+）
CREATE INDEX ON documents
  USING hnsw (embedding vector_cosine_ops)
  WITH (m = 16, ef_construction = 64);
```

| パラメータ | 説明 | デフォルト |
|-----------|------|-----------|
| `m` | 各ノードの接続数。大きいほど精度↑・メモリ↑ | 16 |
| `ef_construction` | 構築時の探索幅。大きいほど精度↑・構築時間↑ | 64 |

### 検索時の精度チューニング

```sql
-- HNSW: 検索時の探索幅（大きいほど精度↑・速度↓）
SET hnsw.ef_search = 100;

-- IVFFlat: 検索時に調べるリスト数（大きいほど精度↑・速度↓）
SET ivfflat.probes = 10;
```

---

## 9. Supabase AI Helpers

Supabase は pgvector をより使いやすくするヘルパー関数を提供しています。

### `ai.session()` を使った Embedding 生成（Edge Function 内）

```typescript
// supabase/functions/embed/index.ts
Deno.serve(async (req) => {
  const { text } = await req.json()

  // Supabase 提供の AI セッション（外部 API 不要）
  const session = new Supabase.ai.Session('gte-small')
  const embedding = await session.run(text, { mean_pool: true, normalize: true })

  return new Response(JSON.stringify({ embedding }), {
    headers: { 'Content-Type': 'application/json' },
  })
})
```

> **`Supabase.ai.Session`** はエッジ関数内で使えるビルトイン AI セッションです。  
> `gte-small` などの小型モデルを無料で利用でき、外部 API キーが不要です。

---

## 📌 まとめ

| ステップ | 内容 |
|---------|------|
| 1. 拡張有効化 | `CREATE EXTENSION vector` |
| 2. テーブル定義 | `embedding VECTOR(1536)` カラムを追加 |
| 3. データ保存 | テキスト → Embedding → INSERT |
| 4. 検索関数 | `match_documents()` を SQL で定義 |
| 5. RAG 実装 | 検索結果をコンテキストとして OpenAI に渡す |
| 6. インデックス | IVFFlat または HNSW で検索を高速化 |

---

## 次のステップ

- [Supabase 公式 AI ガイド](https://supabase.com/docs/guides/ai)
- [pgvector ドキュメント](https://github.com/pgvector/pgvector)
- [OpenAI Embeddings ガイド](https://platform.openai.com/docs/guides/embeddings)
