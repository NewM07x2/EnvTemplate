# Flutter 入門ガイド

> **対象者**: Flutter・Dart を初めて使う開発者  
> **関連テンプレート**: `flutter/flutter_application_sample/`  
> **所要時間**: 約 60 分

---

## 📚 目次

1. [Flutter とは](#1-flutter-とは)
2. [環境構築](#2-環境構築)
3. [新規アプリの作成（テンプレートから）](#3-新規アプリの作成テンプレートから)
4. [Dart の基本構文](#4-dart-の基本構文)
5. [Widget の基本](#5-widget-の基本)
6. [よく使う Widget 一覧](#6-よく使う-widget-一覧)
7. [状態管理（StatefulWidget / Provider）](#7-状態管理statefulwidget--provider)
8. [ナビゲーション（画面遷移）](#8-ナビゲーション画面遷移)
9. [Firebase との連携](#9-firebase-との連携)
10. [ビルド・リリース](#10-ビルドリリース)

---

## 1. Flutter とは

**Flutter** は Google が開発した **クロスプラットフォームアプリ開発フレームワーク**です。  
1 つのコードベースで **iOS・Android・Web・Desktop** のアプリを作れます。

```
1 つのコードで動く環境:
  ┌─────────────────────────────────────┐
  │            Flutter コード             │
  └──┬──────┬──────┬──────┬────────────┘
     │      │      │      │
   iOS  Android  Web  Desktop
                        (Windows/Mac/Linux)
```

### Flutter の特徴

| 特徴 | 説明 |
|------|------|
| **Dart 言語** | 型安全・async/await・シンプルな構文 |
| **Widget ベース** | UI のすべてが Widget で構成される |
| **高速描画** | Skia / Impeller エンジンで 60fps+ |
| **ホットリロード** | コード変更が即座にアプリに反映 |
| **Firebase との相性◎** | Google 製同士で公式サポートが充実 |

---

## 2. 環境構築

### Flutter SDK のインストール

**Windows の場合:**

```powershell
# winget でインストール
winget install Flutter.Flutter

# パスを確認
flutter --version
```

または [flutter.dev](https://flutter.dev/docs/get-started/install) からインストーラーをダウンロード。

**Mac の場合:**

```bash
# Homebrew でインストール
brew install --cask flutter

flutter --version
```

### 環境チェック

```bash
# 不足しているツールをリストアップ
flutter doctor

# 出力例（✅ がついていれば OK）
[✓] Flutter (Channel stable, 3.x.x)
[✓] Android toolchain
[✓] Xcode（Mac の場合）
[✓] VS Code
[✓] Connected device
```

### VS Code の拡張機能

1. **Flutter**（`Dart-Code.flutter`）をインストール
2. **Dart**（`Dart-Code.dart-code`）をインストール

---

## 3. 新規アプリの作成（テンプレートから）

このリポジトリには `flutter/setup_new_app.ps1` という専用スクリプトがあります。

### テンプレートスクリプトを使う方法（推奨）

```powershell
cd flutter

# スクリプトを実行（パラメータを指定）
.\setup_new_app.ps1 `
  -AppName "my_todo_app" `
  -DisplayName "My Todo App" `
  -PackageId "com.yourcompany.mytodoapp"
```

**実行後に生成されるもの:**

```
flutter/
└── my_todo_app/          ← flutter_application_sample をコピーしたもの
    ├── lib/
    │   └── main.dart
    ├── android/
    ├── ios/
    ├── pubspec.yaml       ← アプリ名が自動更新済み
    └── ...
```

### 手動でゼロから作る場合

```bash
# Flutter プロジェクトを新規作成
flutter create --org com.yourcompany my_app

# アプリを起動（エミュレーターまたは実機が必要）
cd my_app
flutter run
```

---

## 4. Dart の基本構文

Flutter は **Dart** 言語で書きます。TypeScript に似た構文です。

### 変数・型

```dart
// 型推論
var name = 'Alice';           // String と推論
var age = 25;                 // int と推論

// 明示的な型指定
String name = 'Alice';
int age = 25;
double price = 9.99;
bool isLoggedIn = false;

// Null 安全（? をつけると null 許容）
String? nullableName = null;
String nonNullName = 'Bob';   // null は代入不可
```

### 関数

```dart
// 通常の関数
String greet(String name) {
  return 'Hello, $name!';
}

// アロー関数（1 行の場合）
String greet(String name) => 'Hello, $name!';

// 名前付き引数（Flutter Widget では多用）
void showInfo({ required String name, int age = 0 }) {
  print('$name: $age 歳');
}
showInfo(name: 'Alice', age: 25);
```

### クラス

```dart
class User {
  final String id;
  String name;
  
  // コンストラクタ
  User({ required this.id, required this.name });
  
  // メソッド
  String greet() => 'こんにちは、$name です';
}

final user = User(id: '1', name: 'Alice');
print(user.greet());
```

### async / await

```dart
// 非同期関数（API 呼び出し等）
Future<String> fetchUser(String id) async {
  final response = await http.get(Uri.parse('/api/users/$id'));
  return response.body;
}

// 使う側
void loadUser() async {
  final user = await fetchUser('user-123');
  print(user);
}
```

---

## 5. Widget の基本

Flutter の UI はすべて **Widget** で構成されます。

```dart
// main.dart のエントリポイント
void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'My App',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.blue),
        useMaterial3: true,         // Material 3 デザイン
      ),
      home: const HomePage(),      // 最初に表示する画面
    );
  }
}
```

### StatelessWidget vs StatefulWidget

```dart
// StatelessWidget: 状態を持たない（表示だけ）
class HelloCard extends StatelessWidget {
  final String name;
  const HelloCard({ super.key, required this.name });

  @override
  Widget build(BuildContext context) {
    return Card(
      child: Text('こんにちは、$name さん'),
    );
  }
}

// StatefulWidget: 状態を持つ（インタラクティブな UI）
class Counter extends StatefulWidget {
  const Counter({super.key});
  @override
  State<Counter> createState() => _CounterState();
}

class _CounterState extends State<Counter> {
  int _count = 0;  // 状態変数

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Text('$_count'),
        ElevatedButton(
          onPressed: () {
            setState(() {          // setState で UI を更新
              _count++;
            });
          },
          child: const Text('+1'),
        ),
      ],
    );
  }
}
```

---

## 6. よく使う Widget 一覧

### レイアウト

```dart
// 縦方向に並べる
Column(
  mainAxisAlignment: MainAxisAlignment.center,    // 縦方向の位置揃え
  crossAxisAlignment: CrossAxisAlignment.start,   // 横方向の位置揃え
  children: [Widget1(), Widget2()],
)

// 横方向に並べる
Row(
  children: [Widget1(), Widget2()],
)

// 重ねて表示
Stack(
  children: [
    Image.network('...'),     // 下
    Positioned(               // 上（絶対位置）
      bottom: 8, right: 8,
      child: Text('Caption'),
    ),
  ],
)

// スクロール可能なリスト（大量データは ListView.builder を使う）
ListView.builder(
  itemCount: items.length,
  itemBuilder: (context, index) {
    return ListTile(title: Text(items[index]));
  },
)
```

### 余白・装飾

```dart
// パディング（内側の余白）
Padding(
  padding: const EdgeInsets.all(16),
  child: Text('Hello'),
)

// マージン・背景色・角丸（Container で指定）
Container(
  margin: const EdgeInsets.symmetric(horizontal: 16),
  padding: const EdgeInsets.all(12),
  decoration: BoxDecoration(
    color: Colors.blue.shade50,
    borderRadius: BorderRadius.circular(8),
    border: Border.all(color: Colors.blue),
  ),
  child: Text('カード'),
)
```

### 入力・ボタン

```dart
// テキスト入力
final controller = TextEditingController();
TextField(
  controller: controller,
  decoration: const InputDecoration(
    labelText: 'メールアドレス',
    border: OutlineInputBorder(),
  ),
  keyboardType: TextInputType.emailAddress,
)

// ボタン
ElevatedButton(
  onPressed: () { /* 処理 */ },
  child: const Text('送信'),
)

TextButton(onPressed: () {}, child: const Text('キャンセル'))
IconButton(onPressed: () {}, icon: const Icon(Icons.add))
```

---

## 7. 状態管理（StatefulWidget / Provider）

### Provider パッケージ（推奨）

```bash
# pubspec.yaml に追加
flutter pub add provider
```

```dart
// 状態クラスを定義（ChangeNotifier を継承）
class CounterModel extends ChangeNotifier {
  int _count = 0;
  int get count => _count;

  void increment() {
    _count++;
    notifyListeners();   // 変更を通知（UI が再描画される）
  }
}

// main.dart でプロバイダーを提供
void main() {
  runApp(
    ChangeNotifierProvider(
      create: (_) => CounterModel(),
      child: const MyApp(),
    ),
  );
}

// 使いたい Widget で読み取る
class CounterPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    final counter = context.watch<CounterModel>();  // 変更を購読

    return Column(
      children: [
        Text('${counter.count}'),
        ElevatedButton(
          onPressed: context.read<CounterModel>().increment,  // 変更のみ（再描画しない）
          child: const Text('+1'),
        ),
      ],
    );
  }
}
```

---

## 8. ナビゲーション（画面遷移）

```dart
// 別の画面に遷移（スタックに push）
Navigator.push(
  context,
  MaterialPageRoute(builder: (context) => const DetailPage()),
)

// 遷移先から戻る
Navigator.pop(context)

// 値を返しながら戻る
Navigator.pop(context, 'result')

// 現在の画面を置き換えて遷移（ログイン後など）
Navigator.pushReplacement(
  context,
  MaterialPageRoute(builder: (context) => const HomePage()),
)

// named routes（大規模アプリ向け）
MaterialApp(
  routes: {
    '/': (context) => const HomePage(),
    '/detail': (context) => const DetailPage(),
    '/login': (context) => const LoginPage(),
  },
)
Navigator.pushNamed(context, '/detail')
```

---

## 9. Firebase との連携

Flutter + Firebase の詳細は [`docs/Firebase/`](../Firebase/README.md) シリーズを参照してください。

### 簡易セットアップ手順

```bash
# FlutterFire CLI のインストール
dart pub global activate flutterfire_cli

# Firebase プロジェクトと連携
flutterfire configure

# 必要なパッケージを追加
flutter pub add firebase_core firebase_auth cloud_firestore
```

```dart
// main.dart に初期化を追加
import 'package:firebase_core/firebase_core.dart';
import 'firebase_options.dart';   // flutterfire configure で自動生成

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Firebase.initializeApp(
    options: DefaultFirebaseOptions.currentPlatform,
  );
  runApp(const MyApp());
}
```

---

## 10. ビルド・リリース

### デバッグビルド（開発時）

```bash
# 接続済みデバイスで実行
flutter run

# 特定デバイスで実行
flutter run -d emulator-5554   # Android エミュレーター
flutter run -d iPhone          # iOS シミュレーター
```

### リリースビルド

```bash
# Android APK
flutter build apk --release

# Android App Bundle（Google Play 用）
flutter build appbundle --release

# iOS（Mac のみ・要 Xcode）
flutter build ios --release

# Web
flutter build web --release
```

### よく使うコマンド

```bash
flutter pub get           # パッケージをインストール
flutter pub upgrade       # パッケージを更新
flutter clean             # ビルドキャッシュを削除
flutter analyze           # 静的解析
flutter test              # テストを実行
flutter devices           # 接続済みデバイス一覧
```

---

## 📌 まとめ

| 概念 | 説明 |
|------|------|
| **Widget** | Flutter の UI の最小単位 |
| **StatelessWidget** | 状態を持たない Widget |
| **StatefulWidget** | 状態を持つ Widget（`setState` で更新） |
| **Provider** | 状態管理パッケージ（推奨） |
| **BuildContext** | Widget ツリー上の位置情報 |
| **pubspec.yaml** | パッケージ管理ファイル（npm の package.json 相当） |

### 次のステップ

- [`flutter/docs/flutter_state.md`](../../flutter/docs/flutter_state.md) — 状態管理の詳細
- [`flutter/docs/flutter_navigation.md`](../../flutter/docs/flutter_navigation.md) — ナビゲーション詳細
- [`flutter/docs/flutter_widget.md`](../../flutter/docs/flutter_widget.md) — Widget カタログ
- [`docs/Firebase/`](../Firebase/README.md) — Firebase 連携
