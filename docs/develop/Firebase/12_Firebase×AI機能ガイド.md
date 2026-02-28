# Firebase × AI 機能ガイド

> **レベル**: ★★★ / 所要時間: 約 45 分  
> **前提**: [クイックスタート](02_クイックスタート.md) の完了推奨・Firebase Blaze プラン（従量課金）が必要

---

## 目次

1. [Firebase の AI 機能概要](#1-firebase-の-ai-機能概要)
2. [Vertex AI in Firebase（Gemini API）のセットアップ](#2-vertex-ai-in-firebasegemini-api-のセットアップ)
3. [テキスト生成（基本）](#3-テキスト生成基本)
4. [マルチターン会話（チャット）](#4-マルチターン会話チャット)
5. [マルチモーダル（画像・PDF の分析）](#5-マルチモーダル画像pdf-の分析)
6. [構造化出力（JSON レスポンス）](#6-構造化出力json-レスポンス)
7. [Function Calling（外部ツールとの連携）](#7-function-calling外部ツールとの連携)
8. [Firebase Extensions で AI を追加する](#8-firebase-extensions-で-ai-を追加する)
9. [Cloud Functions × Gemini API（サーバーサイド）](#9-cloud-functions--gemini-apiサーバーサイド)
10. [コスト管理と注意事項](#10-コスト管理と注意事項)

---

## 1. Firebase の AI 機能概要

Firebase では主に 2 つの方法で AI 機能を利用できます。

```
┌─────────────────────────────────────────────────────────────┐
│                    Firebase × AI                             │
│                                                               │
│  ① Vertex AI in Firebase（Firebase AI Logic）                │
│     ・Gemini モデルをクライアント/サーバーから直接利用        │
│     ・Firebase Auth と統合（ユーザー認証でアクセス制御）      │
│     ・App Check でボット対策                                  │
│                                                               │
│  ② Firebase Extensions（拡張機能）                           │
│     ・Firestore ドキュメントに AI 処理を自動追加              │
│     ・例: ドキュメント作成 → 自動でベクトル化・要約生成        │
└─────────────────────────────────────────────────────────────┘
```

### 利用可能なモデル（2025年時点）

| モデル | 特徴 | 主な用途 |
|-------|------|---------|
| `gemini-2.0-flash` | 高速・低コスト | チャット・テキスト生成・日常タスク |
| `gemini-2.0-flash-lite` | 超高速・最低コスト | 大量処理・リアルタイム補完 |
| `gemini-1.5-pro` | 高精度・長文対応（100万トークン） | 複雑な分析・長文書処理 |
| `gemini-1.5-flash` | バランス型 | 汎用 |

> **最新モデル一覧**: [Firebase AI モデルリスト](https://firebase.google.com/docs/ai-logic/gemini-models) を参照

---

## 2. Vertex AI in Firebase（Gemini API）のセットアップ

### Firebase コンソールでの設定

1. [Firebase コンソール](https://console.firebase.google.com/) → プロジェクトを選択
2. 左メニュー「AI」→「Firebase AI Logic」を開く
3. 「使ってみる」をクリック → Blaze プランへのアップグレードが求められる場合あり
4. API を有効化

### SDK のインストール

```bash
npm install firebase
# firebase パッケージ v11.1.0 以降に Vertex AI in Firebase が含まれる
```

### 初期化（`src/lib/firebase/ai.ts`）

```typescript
import { getApp } from 'firebase/app';
import {
  getAI,
  getGenerativeModel,
  GoogleAIBackend,
} from 'firebase/ai';

// firebase/client.ts で初期化済みの app を利用
const ai = getAI(getApp(), { backend: new GoogleAIBackend() });

// デフォルトモデル（用途に応じて変更）
export const geminiFlash = getGenerativeModel(ai, {
  model: 'gemini-2.0-flash',
});

export const geminiPro = getGenerativeModel(ai, {
  model: 'gemini-1.5-pro',
});
```

---

## 3. テキスト生成（基本）

### シンプルなテキスト生成

```typescript
import { geminiFlash } from '@/lib/firebase/ai';

export async function generateText(prompt: string): Promise<string> {
  const result = await geminiFlash.generateContent(prompt);
  return result.response.text();
}
```

### Next.js コンポーネントでの利用

```tsx
// components/TextGenerator.tsx
'use client';

import { useState } from 'react';
import { geminiFlash } from '@/lib/firebase/ai';

export function TextGenerator() {
  const [prompt, setPrompt]   = useState('');
  const [output, setOutput]   = useState('');
  const [loading, setLoading] = useState(false);

  async function handleGenerate() {
    if (!prompt.trim()) return;
    setLoading(true);
    setOutput('');

    try {
      const result = await geminiFlash.generateContent(prompt);
      setOutput(result.response.text());
    } catch (error) {
      console.error(error);
      setOutput('エラーが発生しました');
    } finally {
      setLoading(false);
    }
  }

  return (
    <div>
      <textarea
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
        placeholder="プロンプトを入力..."
        rows={4}
      />
      <button onClick={handleGenerate} disabled={loading}>
        {loading ? '生成中...' : '生成する'}
      </button>
      {output && <pre>{output}</pre>}
    </div>
  );
}
```

### ストリーミング出力（逐次表示）

```typescript
'use client';

import { useState } from 'react';
import { geminiFlash } from '@/lib/firebase/ai';

export function StreamingGenerator() {
  const [output, setOutput] = useState('');

  async function handleStream(prompt: string) {
    setOutput('');

    // generateContentStream でストリーミング取得
    const stream = await geminiFlash.generateContentStream(prompt);

    for await (const chunk of stream.stream) {
      const text = chunk.text();
      setOutput((prev) => prev + text);
    }
  }

  return (
    <div>
      <button onClick={() => handleStream('日本の四季について200字で説明してください')}>
        ストリーミング生成
      </button>
      <p style={{ whiteSpace: 'pre-wrap' }}>{output}</p>
    </div>
  );
}
```

---

## 4. マルチターン会話（チャット）

```typescript
import { geminiFlash } from '@/lib/firebase/ai';

// チャットセッションを開始（システムプロンプトを設定可能）
const chat = geminiFlash.startChat({
  history: [], // 過去の会話履歴
  systemInstruction: {
    parts: [{ text: 'あなたは親切な日本語アシスタントです。簡潔に回答してください。' }],
  },
});

// メッセージを送信
const response1 = await chat.sendMessage('Firebaseとは何ですか？');
console.log(response1.response.text());

// 続けて会話（前の文脈を引き継ぐ）
const response2 = await chat.sendMessage('料金はどうなっていますか？');
console.log(response2.response.text());
```

### チャット UI コンポーネント

```tsx
// components/ChatBot.tsx
'use client';

import { useState, useRef, useEffect } from 'react';
import { geminiFlash } from '@/lib/firebase/ai';
import type { ChatSession } from 'firebase/ai';

type Message = { role: 'user' | 'model'; text: string };

export function ChatBot() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput]       = useState('');
  const [loading, setLoading]   = useState(false);
  const chatRef                 = useRef<ChatSession | null>(null);

  // チャットセッションを初期化（コンポーネントマウント時に1回）
  useEffect(() => {
    chatRef.current = geminiFlash.startChat({
      systemInstruction: {
        parts: [{ text: 'あなたは Firebase の専門家アシスタントです。' }],
      },
    });
  }, []);

  async function handleSend() {
    if (!input.trim() || !chatRef.current) return;

    const userMessage = input;
    setInput('');
    setMessages((prev) => [...prev, { role: 'user', text: userMessage }]);
    setLoading(true);

    try {
      const result = await chatRef.current.sendMessage(userMessage);
      const modelText = result.response.text();
      setMessages((prev) => [...prev, { role: 'model', text: modelText }]);
    } catch {
      setMessages((prev) => [...prev, { role: 'model', text: 'エラーが発生しました' }]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div>
      <div>
        {messages.map((msg, i) => (
          <div key={i} style={{ textAlign: msg.role === 'user' ? 'right' : 'left' }}>
            <span>{msg.text}</span>
          </div>
        ))}
        {loading && <p>回答を生成中...</p>}
      </div>
      <input
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={(e) => e.key === 'Enter' && handleSend()}
        placeholder="メッセージを入力..."
      />
      <button onClick={handleSend} disabled={loading}>送信</button>
    </div>
  );
}
```

---

## 5. マルチモーダル（画像・PDF の分析）

Gemini はテキストだけでなく、画像・PDF・動画も入力として受け付けます。

### 画像の分析

```typescript
import { geminiFlash } from '@/lib/firebase/ai';

// URL から画像を分析
async function analyzeImageFromUrl(imageUrl: string, question: string): Promise<string> {
  const result = await geminiFlash.generateContent([
    { inlineData: { mimeType: 'image/jpeg', data: '' } }, // URL の場合は fileData を使用
    {
      fileData: {
        mimeType: 'image/jpeg',
        fileUri: imageUrl,
      },
    },
    question,
  ]);
  return result.response.text();
}

// File オブジェクト（アップロードファイル）を分析
async function analyzeUploadedImage(file: File, question: string): Promise<string> {
  // File を Base64 に変換
  const buffer = await file.arrayBuffer();
  const base64 = btoa(String.fromCharCode(...new Uint8Array(buffer)));

  const result = await geminiFlash.generateContent([
    {
      inlineData: {
        mimeType: file.type as 'image/jpeg' | 'image/png' | 'image/webp',
        data: base64,
      },
    },
    question,
  ]);
  return result.response.text();
}
```

### 画像アップロード & 分析コンポーネント

```tsx
'use client';

import { useState } from 'react';
import { geminiFlash } from '@/lib/firebase/ai';

export function ImageAnalyzer() {
  const [result, setResult]   = useState('');
  const [loading, setLoading] = useState(false);

  async function handleFileChange(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0];
    if (!file) return;

    setLoading(true);
    const buffer = await file.arrayBuffer();
    const base64 = btoa(String.fromCharCode(...new Uint8Array(buffer)));

    try {
      const response = await geminiFlash.generateContent([
        { inlineData: { mimeType: file.type as 'image/jpeg', data: base64 } },
        'この画像に何が写っていますか？日本語で説明してください。',
      ]);
      setResult(response.response.text());
    } finally {
      setLoading(false);
    }
  }

  return (
    <div>
      <input type="file" accept="image/*" onChange={handleFileChange} />
      {loading && <p>分析中...</p>}
      {result && <p>{result}</p>}
    </div>
  );
}
```

---

## 6. 構造化出力（JSON レスポンス）

Gemini に JSON 形式で返答させることで、フロントエンドでそのままデータとして利用できます。

```typescript
import { geminiFlash } from '@/lib/firebase/ai';
import { SchemaType } from 'firebase/ai';

// JSON スキーマを定義してレスポンスを型安全に取得
const result = await geminiFlash.generateContent({
  contents: [
    {
      role: 'user',
      parts: [{ text: '日本の主要都市を5つ挙げ、それぞれの特徴を教えてください' }],
    },
  ],
  generationConfig: {
    responseMimeType: 'application/json',
    responseSchema: {
      type: SchemaType.ARRAY,
      items: {
        type: SchemaType.OBJECT,
        properties: {
          name:     { type: SchemaType.STRING, description: '都市名' },
          region:   { type: SchemaType.STRING, description: '地方' },
          feature:  { type: SchemaType.STRING, description: '特徴' },
          population: { type: SchemaType.NUMBER, description: '人口（万人）' },
        },
        required: ['name', 'region', 'feature'],
      },
    },
  },
});

type City = { name: string; region: string; feature: string; population?: number };
const cities: City[] = JSON.parse(result.response.text());
console.log(cities);
// [{ name: '東京', region: '関東', feature: '日本の首都...', population: 1400 }, ...]
```

---

## 7. Function Calling（外部ツールとの連携）

Gemini が必要に応じて外部ツール（関数）を呼び出せる機能です。

```typescript
import { geminiFlash } from '@/lib/firebase/ai';
import { FunctionDeclarationSchemaType } from 'firebase/ai';

// ツール（関数）の定義
const tools = [
  {
    functionDeclarations: [
      {
        name: 'get_weather',
        description: '指定した都市の現在の天気を取得します',
        parameters: {
          type: FunctionDeclarationSchemaType.OBJECT,
          properties: {
            city: {
              type: FunctionDeclarationSchemaType.STRING,
              description: '都市名（例: 東京、大阪）',
            },
          },
          required: ['city'],
        },
      },
    ],
  },
];

// 実際の関数実装
async function get_weather(city: string) {
  // 実際には外部 API を呼び出す
  return { city, temperature: 20, condition: '晴れ', humidity: 60 };
}

// Function Calling の実行
async function chatWithTools(userMessage: string) {
  const chat = geminiFlash.startChat({ tools });
  const response = await chat.sendMessage(userMessage);

  // モデルが関数呼び出しを要求しているか確認
  const functionCall = response.response.functionCalls()?.[0];
  if (functionCall) {
    // 関数を実行
    const functionResult = await get_weather(
      (functionCall.args as { city: string }).city
    );

    // 関数の結果をモデルに返す
    const finalResponse = await chat.sendMessage([
      {
        functionResponse: {
          name: functionCall.name,
          response: functionResult,
        },
      },
    ]);
    return finalResponse.response.text();
  }

  return response.response.text();
}

const answer = await chatWithTools('東京の今日の天気を教えてください');
// → 「東京の現在の天気は晴れ、気温20℃、湿度60%です。」
```

---

## 8. Firebase Extensions で AI を追加する

Firebase Extensions は、設定だけで AI 機能を Firestore と連携させる仕組みです。コードを書かずに AI 機能を追加できます。

### 主要な AI 拡張機能

| 拡張機能 | 機能 |
|---------|------|
| **Firestore Gemini Chatbot** | Firestore ドキュメントをトリガーにチャット応答を生成 |
| **Translate Text in Firestore** | フィールドの内容を自動翻訳 |
| **Label Images with Cloud Vision AI** | 画像をラベリング |
| **Search with Algolia** | Firestore データを全文検索対応に |

### インストール手順

```bash
# Firebase CLI でインストール
firebase ext:install firebase/firestore-gemini-chatbot

# または Firebase コンソール: Extensions → Marketplace から検索
```

### Firestore Gemini Chatbot の動作例

```
Firestore の discussions/{discussionId}/messages コレクションに
メッセージを追加する
        ↓
拡張機能が自動的に Gemini API を呼び出す
        ↓
返答が同じコレクションの新しいドキュメントとして保存される
```

```typescript
// クライアント側はドキュメントを追加するだけ
import { collection, addDoc, onSnapshot } from 'firebase/firestore';
import { db } from '@/lib/firebase/client';

async function sendMessage(discussionId: string, text: string, userId: string) {
  await addDoc(collection(db, `discussions/${discussionId}/messages`), {
    prompt: text,
    userId,
    createTime: new Date(),
  });
  // 返答は自動で追加される → onSnapshot で受け取る
}
```

---

## 9. Cloud Functions × Gemini API（サーバーサイド）

サーバーサイドで Gemini を使うことで、API キーを安全に管理し、より複雑な処理を実装できます。

```typescript
// functions/src/ai.ts
import { onCall, HttpsError } from 'firebase-functions/v2/https';
import { GoogleGenerativeAI } from '@google/generative-ai';
import { defineSecret } from 'firebase-functions/params';

// API キーを Secret Manager で管理
const geminiApiKey = defineSecret('GEMINI_API_KEY');

export const generateSummary = onCall(
  { secrets: [geminiApiKey] },
  async (request) => {
    if (!request.auth) {
      throw new HttpsError('unauthenticated', 'ログインが必要です');
    }

    const { text } = request.data as { text: string };
    if (!text || text.length > 10000) {
      throw new HttpsError('invalid-argument', 'テキストが無効です');
    }

    const genAI = new GoogleGenerativeAI(geminiApiKey.value());
    const model = genAI.getGenerativeModel({ model: 'gemini-2.0-flash' });

    const result = await model.generateContent(
      `以下のテキストを200字以内で要約してください：\n\n${text}`
    );

    return { summary: result.response.text() };
  }
);
```

```typescript
// クライアント側
import { getFunctions, httpsCallable } from 'firebase/functions';

const functions = getFunctions();
const generateSummary = httpsCallable<{ text: string }, { summary: string }>(
  functions,
  'generateSummary'
);

const { data } = await generateSummary({ text: '長い記事のテキスト...' });
console.log(data.summary);
```

### Firestore トリガーで自動要約

```typescript
// functions/src/autoSummary.ts
import { onDocumentCreated } from 'firebase-functions/v2/firestore';
import { GoogleGenerativeAI } from '@google/generative-ai';
import { defineSecret } from 'firebase-functions/params';
import { getFirestore } from 'firebase-admin/firestore';

const geminiApiKey = defineSecret('GEMINI_API_KEY');

// 記事が作成されたら自動で要約を生成して保存
export const autoSummarize = onDocumentCreated(
  { document: 'articles/{articleId}', secrets: [geminiApiKey] },
  async (event) => {
    const article = event.data?.data();
    if (!article?.content || article.summary) return; // 本文がない or 既に要約済み

    const genAI = new GoogleGenerativeAI(geminiApiKey.value());
    const model = genAI.getGenerativeModel({ model: 'gemini-2.0-flash' });

    const result = await model.generateContent(
      `以下の記事を150字以内で要約してください：\n\n${article.content}`
    );

    await getFirestore()
      .collection('articles')
      .doc(event.params.articleId)
      .update({ summary: result.response.text() });
  }
);
```

---

## 10. コスト管理と注意事項

### 料金の仕組み

| モデル | 入力（1M トークン） | 出力（1M トークン） |
|-------|-----------------|-----------------|
| Gemini 2.0 Flash | $0.10 | $0.40 |
| Gemini 2.0 Flash-Lite | $0.075 | $0.30 |
| Gemini 1.5 Pro | $1.25（128K 以下） | $5.00（128K 以下） |

> **1トークン ≈ 日本語 1〜2 文字**。1,000 字の入力 ≈ 500〜1,000 トークン。

### コスト削減のポイント

| 対策 | 効果 |
|------|------|
| `gemini-2.0-flash-lite` を優先使用 | コストを最小化 |
| プロンプトを簡潔に | トークン数を削減 |
| レスポンスの `maxOutputTokens` を設定 | 不要な長文出力を防ぐ |
| クライアント側でキャッシュ | 同じプロンプトの重複呼び出しを防ぐ |
| Cloud Functions でレート制限を実装 | ユーザーによる大量消費を防ぐ |

```typescript
// maxOutputTokens でトークン上限を設定
const model = getGenerativeModel(ai, {
  model: 'gemini-2.0-flash',
  generationConfig: {
    maxOutputTokens: 500, // 出力は500トークン以内
    temperature: 0.7,     // 創造性（0=決定的, 1=ランダム）
  },
});
```

### セキュリティの注意事項

- **クライアント SDK でも利用可能**だが、Firebase App Check を有効にしてボットからの悪用を防ぐ
- **機密情報をプロンプトに含めない**（ユーザー入力をそのまま渡さない）
- **プロンプトインジェクション対策**: ユーザー入力をサニタイズするか、サーバーサイドで処理する

---

## まとめ

| 用途 | 推奨アプローチ |
|------|-------------|
| シンプルなチャット・テキスト生成 | Client SDK（`firebase/ai`） |
| 画像分析・マルチモーダル | Client SDK でインライン Base64 |
| API キーを隠したい・複雑な処理 | Cloud Functions + `@google/generative-ai` |
| コードなしで Firestore と連携 | Firebase Extensions |
| 自動要約・ラベリングなどのバックグラウンド処理 | Firestore トリガー + Cloud Functions |

---

## 次のステップ

- [Cloud Functions ガイド](06_Cloud_Functions（サーバーレス関数）ガイド.md) — サーバーサイドでの AI 処理実装
- [コスト・料金管理ガイド](10_コスト・料金管理ガイド.md) — AI 利用コストの管理方法
