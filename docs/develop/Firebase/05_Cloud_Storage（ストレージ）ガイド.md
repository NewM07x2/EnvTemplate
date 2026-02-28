# Cloud Storage（ストレージ）ガイド

> **所要時間**: 約 30 分  
> **対象レベル**: 初心者～中級者  
> **前提**: [Firebase とは何か](01_Firebaseとは.md)・[Authentication ガイド](03_Authentication（認証）ガイド.md) を読んでいること  
> **目標**: Cloud Storage を使って画像・ファイルのアップロード・ダウンロード・削除ができるようになる

---

## 📚 目次

1. [Cloud Storage とは](#cloud-storageとは)
2. [セットアップ](#セットアップ)
3. [ファイルのアップロード](#ファイルのアップロード)
4. [アップロード進捗の表示](#アップロード進捗の表示)
5. [ダウンロード URL の取得](#ダウンロードurlの取得)
6. [ファイルの一覧取得](#ファイルの一覧取得)
7. [ファイルの削除](#ファイルの削除)
8. [セキュリティルール](#セキュリティルール)
9. [よくあるユースケース](#よくあるユースケース)
10. [よくあるミスとベストプラクティス](#よくあるミスとベストプラクティス)

---

## Cloud Storage とは

**Cloud Storage for Firebase** は、**Google Cloud Storage** をバックエンドとした、ファイル保存・配信サービスです。

```
【できること】

✅ 画像・動画・PDF・音声などあらゆるファイルを保存
✅ アップロードの進捗をリアルタイムで取得
✅ ネットワーク接続が不安定でも自動リトライ
✅ ユーザーごとのアクセス制御（セキュリティルール）
✅ CDN による高速配信
✅ Firebase Authentication と連携した権限管理
```

### ストレージの構造

```
Firebase Storage バケット（bucket）
└── フォルダ（Folder）
    └── ファイル（File）

例：
my-app.appspot.com/
├── users/
│   ├── user_001/
│   │   ├── avatar.jpg        ← プロフィール画像
│   │   └── resume.pdf        ← 添付ファイル
│   └── user_002/
│       └── avatar.png
└── products/
    ├── prod_001_main.jpg
    └── prod_001_thumb.jpg
```

> 💡 **初心者向けポイント**  
> ストレージはパソコンの「フォルダ構造」と同じイメージです。  
> パスで場所を指定してファイルを保存・取得します。

---

## セットアップ

### ステップ 1: Firebase Console でストレージを有効化

1. [Firebase Console](https://console.firebase.google.com/) を開く
2. 左メニュー → 「Storage」
3. 「始める」をクリック
4. セキュリティルールのモードを選択（開発中は「テストモード」）
5. ロケーションを選択（`asia-northeast1` = 東京 推奨）

### ステップ 2: SDK のインストール（インストール済みなら不要）

```bash
npm install firebase
```

### ステップ 3: Storage の初期化

`lib/firebase.ts` に Storage を追加：

```typescript
import { initializeApp, getApps } from "firebase/app";
import { getStorage } from "firebase/storage";

const firebaseConfig = { /* ... */ };

const app = getApps().length === 0 ? initializeApp(firebaseConfig) : getApps()[0];

export const storage = getStorage(app);
export default app;
```

---

## ファイルのアップロード

### 基本的なアップロード

```typescript
import { ref, uploadBytes, getDownloadURL } from "firebase/storage";
import { storage } from "@/lib/firebase";

async function uploadFile(file: File, path: string) {
  // ① ストレージの参照（保存先パス）を作成
  const storageRef = ref(storage, path);

  // ② ファイルをアップロード
  const snapshot = await uploadBytes(storageRef, file);
  console.log("✅ アップロード完了:", snapshot.metadata.fullPath);

  // ③ ダウンロード URL を取得
  const downloadURL = await getDownloadURL(snapshot.ref);
  console.log("URL:", downloadURL);

  return downloadURL;
}

// 使用例
const file = event.target.files[0]; // input[type="file"] から取得
await uploadFile(file, `users/${userId}/avatar.jpg`);
```

### ユーザーのプロフィール画像をアップロード（実践例）

```typescript
import { ref, uploadBytes, getDownloadURL } from "firebase/storage";
import { updateProfile } from "firebase/auth";
import { storage, auth } from "@/lib/firebase";

async function uploadAvatar(file: File): Promise<string> {
  const user = auth.currentUser;
  if (!user) throw new Error("ログインが必要です");

  // ファイル拡張子を取得
  const extension = file.name.split(".").pop();
  // 保存パス: users/{uid}/avatar.{ext}
  const path = `users/${user.uid}/avatar.${extension}`;

  const storageRef = ref(storage, path);
  await uploadBytes(storageRef, file);
  const downloadURL = await getDownloadURL(storageRef);

  // Firebase Authentication のプロフィール写真も更新
  await updateProfile(user, { photoURL: downloadURL });

  return downloadURL;
}
```

### ファイルタイプを指定してアップロード

```typescript
import { ref, uploadBytes } from "firebase/storage";
import { storage } from "@/lib/firebase";

async function uploadWithMetadata(file: File, path: string) {
  const storageRef = ref(storage, path);

  // メタデータを指定（キャッシュ制御など）
  const metadata = {
    contentType: file.type,          // 例: "image/jpeg"
    cacheControl: "public,max-age=3600", // 1 時間キャッシュ
  };

  await uploadBytes(storageRef, file, metadata);
}
```

---

## アップロード進捗の表示

大きなファイルのアップロード時に、進捗バーを表示したい場合は `uploadBytesResumable` を使います。

```typescript
import { ref, uploadBytesResumable, getDownloadURL } from "firebase/storage";
import { storage } from "@/lib/firebase";

async function uploadWithProgress(
  file: File,
  path: string,
  onProgress: (progress: number) => void
): Promise<string> {
  const storageRef = ref(storage, path);
  const uploadTask = uploadBytesResumable(storageRef, file);

  return new Promise((resolve, reject) => {
    uploadTask.on(
      "state_changed",
      // ① 進捗更新
      (snapshot) => {
        const progress = (snapshot.bytesTransferred / snapshot.totalBytes) * 100;
        onProgress(Math.round(progress));
      },
      // ② エラー
      (error) => {
        console.error("アップロードエラー:", error);
        reject(error);
      },
      // ③ 完了
      async () => {
        const downloadURL = await getDownloadURL(uploadTask.snapshot.ref);
        resolve(downloadURL);
      }
    );
  });
}

// React コンポーネントでの使用例
function UploadButton() {
  const [progress, setProgress] = useState(0);
  const [url, setUrl] = useState("");

  const handleUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    const downloadURL = await uploadWithProgress(
      file,
      `uploads/${file.name}`,
      (p) => setProgress(p)
    );
    setUrl(downloadURL);
  };

  return (
    <div>
      <input type="file" onChange={handleUpload} />
      {progress > 0 && <p>アップロード中: {progress}%</p>}
      {url && <img src={url} alt="アップロード済み画像" />}
    </div>
  );
}
```

---

## ダウンロード URL の取得

```typescript
import { ref, getDownloadURL } from "firebase/storage";
import { storage } from "@/lib/firebase";

async function getFileURL(path: string): Promise<string> {
  const storageRef = ref(storage, path);
  const url = await getDownloadURL(storageRef);
  return url;
}

// 使用例
const avatarURL = await getFileURL("users/user_001/avatar.jpg");
// → "https://firebasestorage.googleapis.com/v0/b/..."
```

---

## ファイルの一覧取得

```typescript
import { ref, listAll, getDownloadURL } from "firebase/storage";
import { storage } from "@/lib/firebase";

async function listUserFiles(userId: string) {
  const dirRef = ref(storage, `users/${userId}`);

  // フォルダ内の全ファイルを取得
  const result = await listAll(dirRef);

  const files = await Promise.all(
    result.items.map(async (itemRef) => ({
      name: itemRef.name,           // ファイル名
      fullPath: itemRef.fullPath,   // フルパス
      url: await getDownloadURL(itemRef), // ダウンロード URL
    }))
  );

  console.log("ファイル一覧:", files);
  return files;
}
```

---

## ファイルの削除

```typescript
import { ref, deleteObject } from "firebase/storage";
import { storage } from "@/lib/firebase";

async function deleteFile(path: string) {
  const storageRef = ref(storage, path);
  try {
    await deleteObject(storageRef);
    console.log("✅ ファイル削除完了");
  } catch (error: any) {
    if (error.code === "storage/object-not-found") {
      console.log("ファイルが存在しません");
    } else {
      console.error("削除エラー:", error);
    }
  }
}

// 使用例
await deleteFile("users/user_001/avatar.jpg");
```

---

## セキュリティルール

Storage のセキュリティルールは Firebase Console の「Storage」→「ルール」タブから設定します。

### 基本構文

```javascript
rules_version = '2';
service firebase.storage {
  match /b/{bucket}/o {

    // すべてのアクセスを拒否（デフォルト）
    match /{allPaths=**} {
      allow read, write: if false;
    }

  }
}
```

### よくあるルールパターン

```javascript
rules_version = '2';
service firebase.storage {
  match /b/{bucket}/o {

    // ① ユーザーは自分のフォルダのみ読み書き可能
    match /users/{userId}/{allPaths=**} {
      allow read, write: if request.auth != null
                         && request.auth.uid == userId;
    }

    // ② 画像ファイルのみアップロード可（最大 5MB）
    match /images/{imageId} {
      allow read: if true; // 誰でも読み取り可
      allow write: if request.auth != null
                   && request.resource.size < 5 * 1024 * 1024  // 5MB 以下
                   && request.resource.contentType.matches('image/.*'); // 画像のみ
    }

    // ③ ログインユーザーのみ読み書き可
    match /files/{allPaths=**} {
      allow read, write: if request.auth != null;
    }

  }
}
```

> 💡 **主なルール変数**  
> - `request.auth`：現在のユーザー情報（未ログインなら `null`）  
> - `request.auth.uid`：現在のユーザー ID  
> - `request.resource.size`：アップロードしようとしているファイルのサイズ（バイト）  
> - `request.resource.contentType`：ファイルの MIME タイプ（例: `image/jpeg`）

---

## よくあるユースケース

### ユースケース 1: ユーザーアイコンのアップロード

```
① ユーザーが画像ファイルを選択
② クライアントでプレビュー表示（URL.createObjectURL）
③ Firebase Storage にアップロード（users/{uid}/avatar.jpg）
④ ダウンロード URL を取得
⑤ Firestore の users ドキュメントに URL を保存
⑥ 画像を表示
```

### ユースケース 2: 投稿に画像を添付

```
① ユーザーが投稿フォームで画像を添付
② Storage にアップロード（posts/{postId}/{filename}）
③ ダウンロード URL を取得
④ Firestore の posts ドキュメントに URL の配列として保存
⑤ 投稿一覧で画像を表示
```

### ユースケース 3: PDF ドキュメントの管理

```
① 管理者が PDF をアップロード（documents/{docId}.pdf）
② Firestore にドキュメントのメタ情報（タイトル・URL）を保存
③ ユーザーは Firestore からメタ情報を取得し、Storage URL から PDF を表示
```

---

## よくあるミスとベストプラクティス

### ❌ よくあるミス

```typescript
// ❌ NG: 同じパスに上書きアップロード（古いファイルが消える）
// ユーザーが複数の画像をアップロードするとき、名前が重複する
await uploadBytes(ref(storage, `users/${uid}/image.jpg`), file);
// → 別のファイルでも同じパスなので常に上書きされる

// ❌ NG: ファイルを削除せず Firestore の参照だけ消す
// Storage にゴミファイルが溜まりコスト増加の原因になる
await deleteDoc(doc(db, "posts", postId));
// Storage の画像は消していない！

// ❌ NG: セキュリティルールを設定しない
// 誰でも全ファイルにアクセス・上書きできる状態になる
```

### ✅ ベストプラクティス

```typescript
// ✅ OK: ファイル名にタイムスタンプや UUID を含めて重複を避ける
import { v4 as uuidv4 } from "uuid";
const filename = `${uuidv4()}.${file.name.split(".").pop()}`;
await uploadBytes(ref(storage, `users/${uid}/${filename}`), file);

// ✅ OK: Firestore のドキュメント削除時にストレージも合わせて削除
async function deletePost(postId: string, imageUrl: string) {
  // 画像パスを URL から抽出して削除
  const imagePath = decodeURIComponent(
    imageUrl.split("/o/")[1].split("?")[0]
  );
  await deleteObject(ref(storage, imagePath)); // Storage から削除
  await deleteDoc(doc(db, "posts", postId));   // Firestore から削除
}

// ✅ OK: アップロード前にファイルサイズ・タイプを検証
function validateFile(file: File): void {
  const MAX_SIZE = 5 * 1024 * 1024; // 5MB
  const ALLOWED_TYPES = ["image/jpeg", "image/png", "image/webp"];

  if (file.size > MAX_SIZE) throw new Error("5MB 以下のファイルを選択してください");
  if (!ALLOWED_TYPES.includes(file.type)) throw new Error("JPEG/PNG/WebP のみ対応しています");
}
```

---

## 📌 参考リンク

| リソース | URL |
|---------|-----|
| Cloud Storage 公式ドキュメント | https://firebase.google.com/docs/storage?hl=ja |
| ファイルのアップロード | https://firebase.google.com/docs/storage/web/upload-files?hl=ja |
| セキュリティルール | https://firebase.google.com/docs/storage/security?hl=ja |
| 料金の仕組み | https://firebase.google.com/docs/storage/billing-faq?hl=ja |

---

> 📝 **次のステップ**  
> ストレージを習得したら、サーバーレス関数でバックエンド処理を実装しましょう。  
> → [Cloud Functions ガイド](05_Cloud_Functions（サーバーレス関数）ガイド.md)
