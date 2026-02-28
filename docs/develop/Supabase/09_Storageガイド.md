# 09. Storage ガイド

> **レベル**: ★★☆☆☆（初中級）  
> **前提知識**: [01_クイックスタート](01_クイックスタート.md)・[02_認証ガイド](02_認証ガイド.md) の完了  
> **所要時間**: 約 45 分

---

## 📚 目次

1. [Supabase Storage とは](#1-supabase-storage-とは)
2. [バケットの作成と設定](#2-バケットの作成と設定)
3. [ファイルのアップロード](#3-ファイルのアップロード)
4. [ファイルの取得・URL 生成](#4-ファイルの取得url-生成)
5. [ファイルの削除・移動](#5-ファイルの削除移動)
6. [ストレージポリシー（アクセス制御）](#6-ストレージポリシーアクセス制御)
7. [画像の変換（Image Transformation）](#7-画像の変換image-transformation)
8. [React でのファイルアップロード実装例](#8-react-でのファイルアップロード実装例)

---

## 1. Supabase Storage とは

**Supabase Storage** は、画像・動画・PDF などのファイルを保存・配信するサービスです。  
内部的には **AWS S3** 互換のオブジェクトストレージを使用しています。

```
構成:

Supabase Storage
├── バケット（Bucket）  ← フォルダの最上位単位
│   ├── avatars/        ← パスで管理
│   │   ├── user_001/profile.jpg
│   │   └── user_002/profile.png
│   └── documents/
│       └── report_2026.pdf
└── バケット（Bucket）
    └── ...
```

| 概念 | 説明 |
|------|------|
| **バケット** | ファイルを格納する最上位のコンテナ。公開・非公開を設定できる |
| **オブジェクト** | バケット内の個々のファイル |
| **パス** | バケット内のファイルのパス（例: `user_001/avatar.jpg`） |

### 無料プランの制限

| リソース | 上限 |
|---------|------|
| ストレージ容量 | 1 GB |
| 転送量 | 2 GB / 月 |
| ファイルサイズ | 50 MB / ファイル |

---

## 2. バケットの作成と設定

### ダッシュボードから作成

1. Supabase Console > **Storage** > **New Bucket**
2. バケット名を入力（例: `avatars`）
3. **Public bucket** の設定:
   - **Public**: URL を知っていれば誰でも閲覧可能（プロフィール画像など）
   - **Private**: 認証が必要（個人ドキュメントなど）

### SQL / API から作成

```typescript
// バケットの作成
const { data, error } = await supabase.storage.createBucket('avatars', {
  public: true,               // 公開バケット
  allowedMimeTypes: ['image/jpeg', 'image/png', 'image/webp'],
  fileSizeLimit: 5 * 1024 * 1024,  // 5MB 上限
})
```

### バケットの使い分け

```
推奨構成:

avatars/         → public: true   （プロフィール画像。URL 共有が必要）
post_images/     → public: true   （投稿画像。公開前提）
documents/       → public: false  （契約書・請求書。認証が必要）
temp_uploads/    → public: false  （一時保存。処理後に削除）
```

---

## 3. ファイルのアップロード

### 基本的なアップロード

```typescript
import { createClient } from '@/lib/supabase/client'

const supabase = createClient()

// ① ファイルオブジェクトをアップロード（input[type=file] からの場合）
async function uploadAvatar(userId: string, file: File) {
  // パスは一意にする（ユーザーごとにフォルダを分ける）
  const filePath = `${userId}/avatar.${file.name.split('.').pop()}`

  const { data, error } = await supabase.storage
    .from('avatars')
    .upload(filePath, file, {
      cacheControl: '3600',  // キャッシュ: 1時間
      upsert: true,          // 同じパスのファイルがあれば上書き
    })

  if (error) throw error
  return data.path  // 保存されたパスを返す
}

// ② Base64 データをアップロード
async function uploadBase64Image(base64: string) {
  // "data:image/png;base64,xxxxx" 形式から変換
  const base64Data = base64.replace(/^data:image\/\w+;base64,/, '')
  const buffer = Buffer.from(base64Data, 'base64')
  const blob = new Blob([buffer], { type: 'image/png' })

  const { data, error } = await supabase.storage
    .from('post_images')
    .upload(`${Date.now()}.png`, blob)

  if (error) throw error
  return data.path
}
```

### ユニークなファイル名を生成する

```typescript
// ファイル名の衝突を防ぐユーティリティ
function generateUniqueFilePath(userId: string, file: File): string {
  const extension = file.name.split('.').pop() ?? 'bin'
  const uniqueId = crypto.randomUUID()
  return `${userId}/${uniqueId}.${extension}`
}

async function uploadPostImage(userId: string, file: File) {
  const filePath = generateUniqueFilePath(userId, file)

  const { data, error } = await supabase.storage
    .from('post_images')
    .upload(filePath, file)

  if (error) throw error
  return filePath
}
```

---

## 4. ファイルの取得・URL 生成

### 公開バケットの URL（Public Bucket）

```typescript
// 公開バケットは getPublicUrl で永続 URL を取得できる
function getPublicUrl(bucket: string, path: string): string {
  const { data } = supabase.storage.from(bucket).getPublicUrl(path)
  return data.publicUrl
}

// 使用例
const avatarUrl = getPublicUrl('avatars', 'user_001/avatar.jpg')
// https://xxxx.supabase.co/storage/v1/object/public/avatars/user_001/avatar.jpg
```

### 非公開バケットの署名付き URL（Private Bucket）

```typescript
// 署名付き URL（一定時間だけ有効なアクセス URL）
async function getSignedUrl(bucket: string, path: string, expiresIn = 3600) {
  const { data, error } = await supabase.storage
    .from(bucket)
    .createSignedUrl(path, expiresIn)  // 有効期限（秒）

  if (error) throw error
  return data.signedUrl
}

// 複数ファイルの署名付き URL を一括取得
async function getSignedUrls(bucket: string, paths: string[]) {
  const { data, error } = await supabase.storage
    .from(bucket)
    .createSignedUrls(paths, 3600)

  if (error) throw error
  return data
}

// ファイルをダウンロード（バイナリデータとして取得）
async function downloadFile(bucket: string, path: string) {
  const { data, error } = await supabase.storage
    .from(bucket)
    .download(path)

  if (error) throw error
  // data は Blob
  return URL.createObjectURL(data)
}
```

---

## 5. ファイルの削除・移動

```typescript
// 単一ファイルの削除
async function deleteFile(bucket: string, path: string) {
  const { error } = await supabase.storage
    .from(bucket)
    .remove([path])

  if (error) throw error
}

// 複数ファイルの一括削除
async function deleteFiles(bucket: string, paths: string[]) {
  const { error } = await supabase.storage
    .from(bucket)
    .remove(paths)

  if (error) throw error
}

// ファイルの移動（rename）
async function moveFile(bucket: string, fromPath: string, toPath: string) {
  const { error } = await supabase.storage
    .from(bucket)
    .move(fromPath, toPath)

  if (error) throw error
}

// ファイルのコピー
async function copyFile(bucket: string, fromPath: string, toPath: string) {
  const { error } = await supabase.storage
    .from(bucket)
    .copy(fromPath, toPath)

  if (error) throw error
}
```

---

## 6. ストレージポリシー（アクセス制御）

RLS（Row Level Security）と同様に、**誰がどのファイルにアクセスできるか**をポリシーで制御します。

### ダッシュボードでの設定

Supabase Console > Storage > バケット名 > **Policies** タブ

### SQL でポリシーを設定

```sql
-- ① 公開バケット: 誰でも読める
CREATE POLICY "アバターは誰でも閲覧可能"
  ON storage.objects FOR SELECT
  USING (bucket_id = 'avatars');

-- ② 認証済みユーザーのみアップロード可能
CREATE POLICY "認証済みユーザーはアップロード可能"
  ON storage.objects FOR INSERT
  WITH CHECK (
    bucket_id = 'avatars'
    AND auth.role() = 'authenticated'
  );

-- ③ 自分のフォルダにのみアップロード・削除可能
-- ファイルパスが "{ユーザーID}/" で始まることを確認
CREATE POLICY "自分のアバターのみ操作可能"
  ON storage.objects FOR ALL
  USING (
    bucket_id = 'avatars'
    AND auth.uid()::text = (storage.foldername(name))[1]
  )
  WITH CHECK (
    bucket_id = 'avatars'
    AND auth.uid()::text = (storage.foldername(name))[1]
  );

-- ④ 非公開バケット: 認証済みかつ自分のファイルのみ
CREATE POLICY "自分のドキュメントのみ閲覧可能"
  ON storage.objects FOR SELECT
  USING (
    bucket_id = 'documents'
    AND auth.uid()::text = (storage.foldername(name))[1]
  );
```

### storage.foldername / storage.filename ヘルパー

```sql
-- パス: "user_001/subfolder/file.pdf"
storage.foldername(name)  → ARRAY['user_001', 'subfolder']
storage.filename(name)    → 'file.pdf'

-- 最初のフォルダ（ユーザー ID）を取り出す
(storage.foldername(name))[1]  → 'user_001'
```

---

## 7. 画像の変換（Image Transformation）

Supabase Storage は、**URL パラメータで画像をリアルタイム変換**できます（Pro プラン以上）。

```typescript
// サムネイルサイズに変換して取得
function getThumbnailUrl(path: string): string {
  const { data } = supabase.storage
    .from('post_images')
    .getPublicUrl(path, {
      transform: {
        width: 400,
        height: 300,
        resize: 'cover',    // 'cover' | 'contain' | 'fill'
        quality: 80,        // 画質 1-100
        format: 'webp',     // 'webp' | 'avif' | 'origin'
      },
    })
  return data.publicUrl
}

// 使用例
// 元画像:      https://xxx.supabase.co/storage/v1/object/public/post_images/photo.jpg
// 変換後:      https://xxx.supabase.co/storage/v1/render/image/public/post_images/photo.jpg?width=400&height=300&resize=cover&quality=80&format=webp
```

```typescript
// Next.js の Image コンポーネントと組み合わせる
import Image from 'next/image'

function PostThumbnail({ imagePath }: { imagePath: string }) {
  const thumbnailUrl = getThumbnailUrl(imagePath)

  return (
    <Image
      src={thumbnailUrl}
      alt="投稿画像"
      width={400}
      height={300}
      className="rounded-lg object-cover"
    />
  )
}
```

---

## 8. React でのファイルアップロード実装例

### アバター画像のアップロードコンポーネント

```typescript
'use client'

import { useState, useRef } from 'react'
import { createClient } from '@/lib/supabase/client'
import Image from 'next/image'

type AvatarUploadProps = {
  userId: string
  currentAvatarUrl?: string | null
  onUpload: (url: string) => void
}

export function AvatarUpload({ userId, currentAvatarUrl, onUpload }: AvatarUploadProps) {
  const supabase = createClient()
  const [uploading, setUploading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [preview, setPreview] = useState<string | null>(currentAvatarUrl ?? null)
  const inputRef = useRef<HTMLInputElement>(null)

  const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (!file) return

    // バリデーション
    if (!['image/jpeg', 'image/png', 'image/webp'].includes(file.type)) {
      setError('JPEG・PNG・WebP 形式のみアップロード可能です')
      return
    }
    if (file.size > 5 * 1024 * 1024) {
      setError('ファイルサイズは 5MB 以下にしてください')
      return
    }

    // プレビュー表示
    const objectUrl = URL.createObjectURL(file)
    setPreview(objectUrl)

    // アップロード
    setUploading(true)
    setError(null)

    try {
      const extension = file.name.split('.').pop()
      const filePath = `${userId}/avatar.${extension}`

      const { error: uploadError } = await supabase.storage
        .from('avatars')
        .upload(filePath, file, { upsert: true })

      if (uploadError) throw uploadError

      // 公開 URL を取得してコールバックで返す
      const { data } = supabase.storage
        .from('avatars')
        .getPublicUrl(filePath)

      // キャッシュバスター付きで返す（同じ URL でも再取得させる）
      onUpload(`${data.publicUrl}?t=${Date.now()}`)
    } catch (err) {
      setError('アップロードに失敗しました。再試行してください。')
      setPreview(currentAvatarUrl ?? null)
    } finally {
      setUploading(false)
    }
  }

  return (
    <div className="flex flex-col items-center gap-4">
      {/* プレビュー */}
      <div
        className="relative w-24 h-24 rounded-full overflow-hidden bg-gray-200 cursor-pointer"
        onClick={() => inputRef.current?.click()}
      >
        {preview ? (
          <Image src={preview} alt="アバター" fill className="object-cover" />
        ) : (
          <div className="flex items-center justify-center h-full text-gray-400">
            画像なし
          </div>
        )}
        {uploading && (
          <div className="absolute inset-0 bg-black/50 flex items-center justify-center">
            <span className="text-white text-xs">アップロード中...</span>
          </div>
        )}
      </div>

      <input
        ref={inputRef}
        type="file"
        accept="image/jpeg,image/png,image/webp"
        onChange={handleFileChange}
        className="hidden"
        disabled={uploading}
      />

      <button
        type="button"
        onClick={() => inputRef.current?.click()}
        disabled={uploading}
        className="text-sm text-blue-600 hover:underline"
      >
        {uploading ? 'アップロード中...' : '画像を変更'}
      </button>

      {error && <p className="text-red-500 text-sm">{error}</p>}
    </div>
  )
}
```

---

## 📌 まとめ

| 操作 | メソッド |
|------|---------|
| アップロード | `storage.from('bucket').upload(path, file)` |
| 公開 URL 取得 | `storage.from('bucket').getPublicUrl(path)` |
| 署名付き URL 取得 | `storage.from('bucket').createSignedUrl(path, seconds)` |
| ダウンロード | `storage.from('bucket').download(path)` |
| 削除 | `storage.from('bucket').remove([path])` |
| 移動 | `storage.from('bucket').move(from, to)` |
| 一覧取得 | `storage.from('bucket').list(prefix)` |

---

## 次のステップ

- [Realtime 詳細ガイド](10_Realtime詳細ガイド.md) → リアルタイムデータ同期の詳細
