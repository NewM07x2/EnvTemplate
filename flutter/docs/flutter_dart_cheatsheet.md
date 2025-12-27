# Flutter/Dart よく使う構文まとめ

Flutterアプリを作る際によく登場する構文やWidgetの基本をまとめました。

---

## 目次

1. [Dartの基本構文](#dartの基本構文)
2. [Flutterでよく使うWidget構文](#flutterでよく使うwidget構文)
3. [よく使う組み合わせ（まとめ）](#common-combinations)

---

## Dartの基本構文

### ① 変数と定数

``` dart
var name = 'Masato';     // 型推論あり
String city = 'Tokyo';   // 明示的に型指定
const pi = 3.14;         // コンパイル時定数
final now = DateTime.now(); // 実行時に一度だけ設定される定数
```

### ② 条件分岐

``` dart
if (score > 80) {
  print('Good!');
} else if (score > 50) {
  print('OK');
} else {
  print('Bad');
}
```

``` dart
var message = score > 60 ? 'Pass' : 'Fail';
```

### ③ ループ処理

``` dart
for (var i = 0; i < 5; i++) {
  print(i);
}

for (var item in ['A', 'B', 'C']) {
  print(item);
}

while (condition) {
  // 繰り返し処理
}
```

### ④ 関数定義

``` dart
void greet(String name) {
  print('Hello $name');
}

int add(int a, int b) => a + b;
```

### ⑤ クラスとコンストラクタ

``` dart
class Person {
  final String name;
  int age;

  Person(this.name, this.age);

  void hello() {
    print('Hello, I am $name and I am $age years old');
  }
}

var p = Person('Masato', 30);
p.hello();
```

---

## Flutterでよく使うWidget構文

### ① StatelessWidget（状態を持たない）

``` dart
class HelloPage extends StatelessWidget {
  const HelloPage({super.key});

  @override
  Widget build(BuildContext context) {
    return const Scaffold(
      body: Center(child: Text('Hello Flutter!')),
    );
  }
}
```

### ② StatefulWidget（状態を持つ）

``` dart
class CounterPage extends StatefulWidget {
  const CounterPage({super.key});

  @override
  State<CounterPage> createState() => _CounterPageState();
}

class _CounterPageState extends State<CounterPage> {
  int count = 0;

  void _increment() {
    setState(() {
      count++;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Counter')),
      body: Center(
        child: Text(
          '$count',
          style: const TextStyle(fontSize: 40),
        ),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: _increment,
        child: const Icon(Icons.add),
      ),
    );
  }
}
```

### ③ 画面遷移（Navigator）

``` dart
Navigator.of(context).push(
  MaterialPageRoute(builder: (_) => const NextPage()),
);
Navigator.of(context).pop();
```

### ④ レイアウト構文

``` dart
Column(
  mainAxisAlignment: MainAxisAlignment.center,
  crossAxisAlignment: CrossAxisAlignment.start,
  children: const [
    Text('A'),
    Text('B'),
    Text('C'),
  ],
);
```

### ⑤ リスト・マップからWidgetを生成

``` dart
var items = ['Apple', 'Banana', 'Orange'];

Column(
  children: items.map((e) => Text(e)).toList(),
);
```

### ⑥ 非同期処理（async / await）

``` dart
Future<void> fetchData() async {
  var response = await http.get(Uri.parse('https://example.com'));
  print(response.body);
}
```

### ⑦ 条件付き表示（Widgetツリー内）

``` dart
isLoading
  ? const CircularProgressIndicator()
  : const Text('Done!');
```

``` dart
Column(
  children: [
    const Text('Header'),
    if (showList)
      ...items.map((e) => Text(e)).toList(),
  ],
);
```

### ⑧ const最適化

``` dart
const Text('Static text');
```

---

## common-combinations

## よく使う組み合わせ（まとめ）

構文/用途

| 構文 / API                          | 用途                             |
|------------------------------------|----------------------------------|
| `setState()`                       | UIの再描画（StatefulWidget内）   |
| `Navigator.push()` / `Navigator.pop()` | 画面遷移                        |
| `FutureBuilder` / `StreamBuilder` | 非同期データをUIに反映           |
| `TextEditingController`           | 入力フォームの値取得            |
| `ListView.builder()`              | 可変リスト表示                  |
| `const` 修飾子                    | 不変Widgetのパフォーマンス改善 |
| `Expanded` / `Flexible`           | レイアウト制御                  |
| `MediaQuery.of(context).size`     | 画面サイズ取得                  |


学んでおくと良い追加トピック（優先度付き）

高優先（まず押さえると効果が大きい）  
理由: 大規模アプリや研究での定量評価に必要。  
1.flutter_animation.md — UIリッチ化の基礎（Implicit/Explicit, AnimationController, Tween, Hero, パフォーマンス）  
理由: UX向上に直結。複雑な遷移や研究用途で多用。  
2.flutter_testing_advanced.md — Golden、モック、CI統合、統合テスト戦略  
理由: 品質担保の基盤。CIでの自動化は運用で必須。  
3.flutter_performance.md — プロファイリング、メモリ/描画最適化、DevToolsの実例  

中優先（実用性・運用で有益）  
4. flutter_native_integration.md — Platform Channels、ネイティブAPI呼び出し、プラグイン作成  
5. flutter_firebase_integration.md — Auth/Firestore/FCM等（サーバレス構成の実践）  
6. flutter_offline_and_sync.md — オフラインファースト、ローカルDBと同期戦略  
  
低〜中優先（専門性高め・チーム運用向け）  
7. flutter_security.md — トークン管理、secure_storage、脆弱性対策  
8. flutter_ci_cd.md — GitHub Actions, Codemagic, Bitrise のサンプルパイプライン  
9. flutter_plugins_and_packages.md — パッケージ選定、メンテ手法、pub.dev公開  
10. flutter_observability.md — ログ・エラー収集・トレーシング（Sentry, Crashlytics, OpenTelemetry）  
11. flutter_graphics_shaders.md — Skia/Fragment shader、カスタム描画（高度な研究向け）  
12. flutter_package_dev.md — 自作パッケージの設計・テスト・公開手順  