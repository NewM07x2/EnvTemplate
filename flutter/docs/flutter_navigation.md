# Flutter Navigation — 詳細ガイド

このドキュメントは、Flutterにおける画面遷移（Navigation）について諸学者（研究者・教育者・上級学習者）向けに体系的かつ詳細にまとめた資料です。  
画面遷移の基本概念、Navigator API、名前付きルート、高度なルーティングパターン、データ受け渡し、Deep Link、パフォーマンス最適化、テスト戦略、研究応用までを網羅します。

---

## 目次

1. [画面遷移の基礎概念](#1-画面遷移の基礎概念)
2. [基本的な画面遷移（Navigator 1.0）](#2-基本的な画面遷移navigator-10)
3. [名前付きルート（Named Routes）](#3-名前付きルートnamed-routes)
4. [高度なルーティング（Navigator 2.0 / Router API）](#4-高度なルーティングnavigator-20--router-api)
5. [パッケージによる高度なルーティング](#5-パッケージによる高度なルーティング)
6. [タブナビゲーション](#6-タブナビゲーション)
7. [カスタムトランジション](#7-カスタムトランジション)
8. [Deep Link対応](#8-deep-link対応)
9. [パフォーマンス最適化](#9-パフォーマンス最適化)
10. [テスト戦略](#10-テスト戦略)
11. [ベストプラクティス](#11-ベストプラクティス)
12. [研究・応用のヒント](#12-研究応用のヒント)
13. [参考文献](#13-参考文献)

---

## 1 画面遷移の基礎概念

### 1.1 画面遷移（Navigation）とは

Flutterにおける画面遷移は、ユーザーが異なる画面（Screen/Page）間を移動する仕組みです。モバイルアプリケーションでは、この遷移は通常「スタック」構造で管理され、新しい画面を積み重ね（push）、前の画面に戻る（pop）という操作で実現されます。

### 1.2 ルート（Route）の概念

Flutterでは、各画面を**Route**として扱います。Routeは、画面の内容だけでなく、遷移アニメーションや画面のライフサイクルも管理します。

- **Route**: 画面を表す抽象的な概念
- **MaterialPageRoute**: Material Designのトランジションを持つRoute
- **CupertinoPageRoute**: iOSスタイルのトランジションを持つRoute
- **PageRoute**: カスタムトランジションを定義可能な基底クラス

### 1.3 Navigator（ナビゲーター）

Navigatorは、Routeのスタックを管理するウィジェットです。アプリケーション全体で通常1つのNavigatorが存在し、画面遷移の履歴を保持します。

- **スタック構造**: 後入れ先出し（LIFO）で画面を管理
- **履歴管理**: ユーザーの遷移履歴を保持
- **アニメーション制御**: 遷移時のアニメーションを自動的に処理

---

## 2 基本的な画面遷移（Navigator 1.0）

### 2.1 命令的な画面遷移

Navigator 1.0は、命令的（imperative）なAPIで画面遷移を実行します。

#### 基本的なpush/pop

```dart
// 新しい画面へ遷移
Navigator.push(
  context,
  MaterialPageRoute(builder: (context) => SecondPage()),
);

// 前の画面に戻る
Navigator.pop(context);
```

#### 完全な例

```dart
class FirstPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('First Page')),
      body: Center(
        child: ElevatedButton(
          onPressed: () {
            Navigator.push(
              context,
              MaterialPageRoute(builder: (context) => SecondPage()),
            );
          },
          child: const Text('Go to Second Page'),
        ),
      ),
    );
  }
}

class SecondPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Second Page')),
      body: Center(
        child: ElevatedButton(
          onPressed: () {
            Navigator.pop(context);
          },
          child: const Text('Go Back'),
        ),
      ),
    );
  }
}
```

### 2.2 データの受け渡し

#### 遷移先にデータを渡す

```dart
// データを渡して画面遷移
class User {
  final String name;
  final int age;
  User(this.name, this.age);
}

// 遷移元
Navigator.push(
  context,
  MaterialPageRoute(
    builder: (context) => DetailPage(user: User('Alice', 25)),
  ),
);

// 遷移先
class DetailPage extends StatelessWidget {
  final User user;
  
  const DetailPage({Key? key, required this.user}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text(user.name)),
      body: Center(
        child: Text('Age: ${user.age}'),
      ),
    );
  }
}
```

#### 遷移先からデータを受け取る

```dart
// 遷移元でデータを待ち受ける
final result = await Navigator.push(
  context,
  MaterialPageRoute(builder: (context) => SelectionPage()),
);

if (result != null) {
  print('Selected: $result');
}

// 遷移先でデータを返す
class SelectionPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Select')),
      body: Center(
        child: ElevatedButton(
          onPressed: () {
            Navigator.pop(context, 'Option A'); // データを返す
          },
          child: const Text('Option A'),
        ),
      ),
    );
  }
}
```

### 2.3 様々なNavigatorメソッド

#### pushReplacement（現在の画面を置き換え）

```dart
// 現在の画面を新しい画面で置き換える（戻れない）
Navigator.pushReplacement(
  context,
  MaterialPageRoute(builder: (context) => HomePage()),
);
```

#### pushAndRemoveUntil（条件付きでスタックをクリア）

```dart
// 特定の画面まで戻り、新しい画面をpush
Navigator.pushAndRemoveUntil(
  context,
  MaterialPageRoute(builder: (context) => LoginPage()),
  (route) => false, // すべての画面を削除
);

// 最初の画面まで戻る
Navigator.pushAndRemoveUntil(
  context,
  MaterialPageRoute(builder: (context) => HomePage()),
  ModalRoute.withName('/'), // '/'まで削除
);
```

#### popUntil（特定の画面まで戻る）

```dart
// 名前付きルートまで戻る
Navigator.popUntil(context, ModalRoute.withName('/home'));

// 最初の画面まで戻る
Navigator.popUntil(context, (route) => route.isFirst);
```

#### canPop（戻れるか確認）

```dart
if (Navigator.canPop(context)) {
  Navigator.pop(context);
} else {
  // 最初の画面なので戻れない
  print('Cannot pop');
}
```

#### maybePop（可能なら戻る）

```dart
// 戻れる場合のみpop
await Navigator.maybePop(context);
```

---

## 3 名前付きルート（Named Routes）

### 3.1 名前付きルートの定義

名前付きルートを使用すると、画面を文字列で識別できます。

```dart
class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Navigation Demo',
      initialRoute: '/',
      routes: {
        '/': (context) => HomePage(),
        '/details': (context) => DetailsPage(),
        '/settings': (context) => SettingsPage(),
      },
    );
  }
}
```

### 3.2 名前付きルートでの遷移

```dart
// 画面遷移
Navigator.pushNamed(context, '/details');

// データを渡す
Navigator.pushNamed(
  context,
  '/details',
  arguments: {'id': 123, 'name': 'Item'},
);

// 画面を置き換え
Navigator.pushReplacementNamed(context, '/home');

// スタックをクリアして遷移
Navigator.pushNamedAndRemoveUntil(
  context,
  '/login',
  (route) => false,
);
```

### 3.3 引数の受け取り

```dart
class DetailsPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    // 引数を取得
    final args = ModalRoute.of(context)!.settings.arguments as Map<String, dynamic>;
    
    return Scaffold(
      appBar: AppBar(title: Text(args['name'])),
      body: Center(
        child: Text('ID: ${args['id']}'),
      ),
    );
  }
}
```

### 3.4 onGenerateRoute（動的ルート生成）

```dart
class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      onGenerateRoute: (settings) {
        // ルート名によって分岐
        if (settings.name == '/details') {
          final args = settings.arguments as Map<String, dynamic>;
          return MaterialPageRoute(
            builder: (context) => DetailsPage(
              id: args['id'],
              name: args['name'],
            ),
          );
        }
        
        // パスパラメータを解析
        if (settings.name?.startsWith('/user/') == true) {
          final userId = settings.name!.split('/').last;
          return MaterialPageRoute(
            builder: (context) => UserPage(userId: userId),
          );
        }
        
        // 未定義のルート
        return MaterialPageRoute(
          builder: (context) => NotFoundPage(),
        );
      },
    );
  }
}
```

### 3.5 onUnknownRoute（404ページ）

```dart
class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      onUnknownRoute: (settings) {
        return MaterialPageRoute(
          builder: (context) => NotFoundPage(),
        );
      },
    );
  }
}
```

---

## 4 高度なルーティング（Navigator 2.0 / Router API）

### 4.1 Navigator 2.0の背景

Navigator 1.0の課題:

- ブラウザの戻る/進むボタンに対応できない
- Deep Linkの処理が複雑
- 宣言的UIとの統合が不十分
- 状態管理との連携が困難

Navigator 2.0の特徴:

- **宣言的なルーティング**: 状態に基づいて画面スタックを構築
- **Deep Link対応**: URLから直接画面を復元
- **Web対応**: ブラウザのナビゲーションと統合
- **状態管理との統合**: アプリの状態とルーティングを同期

### 4.2 Navigator 2.0の構成要素

#### RouterDelegate

画面スタックを構築し、Navigatorを管理します。

```dart
class MyRouterDelegate extends RouterDelegate<AppRoutePath>
    with ChangeNotifier, PopNavigatorRouterDelegateMixin<AppRoutePath> {
  
  final GlobalKey<NavigatorState> navigatorKey;
  
  // アプリの状態
  bool _showDetails = false;
  int? _selectedId;

  MyRouterDelegate() : navigatorKey = GlobalKey<NavigatorState>();

  // 現在のルート設定を返す
  @override
  AppRoutePath get currentConfiguration {
    if (_showDetails) {
      return AppRoutePath.details(_selectedId!);
    } else {
      return AppRoutePath.home();
    }
  }

  // 新しい設定を適用
  @override
  Future<void> setNewRoutePath(AppRoutePath path) async {
    if (path.isDetailsPage) {
      _selectedId = path.id;
      _showDetails = true;
    } else {
      _showDetails = false;
    }
  }

  // Navigatorを構築
  @override
  Widget build(BuildContext context) {
    return Navigator(
      key: navigatorKey,
      pages: [
        MaterialPage(
          key: const ValueKey('HomePage'),
          child: HomePage(
            onItemTapped: (id) {
              _selectedId = id;
              _showDetails = true;
              notifyListeners();
            },
          ),
        ),
        if (_showDetails)
          MaterialPage(
            key: ValueKey('DetailsPage-$_selectedId'),
            child: DetailsPage(
              id: _selectedId!,
              onBack: () {
                _showDetails = false;
                notifyListeners();
              },
            ),
          ),
      ],
      onPopPage: (route, result) {
        if (!route.didPop(result)) {
          return false;
        }
        _showDetails = false;
        notifyListeners();
        return true;
      },
    );
  }
}
```

#### RouteInformationParser

URLをアプリの状態（ルート設定）に変換します。

```dart
class AppRoutePath {
  final int? id;
  final bool isUnknown;

  AppRoutePath.home()
      : id = null,
        isUnknown = false;

  AppRoutePath.details(this.id) : isUnknown = false;

  AppRoutePath.unknown()
      : id = null,
        isUnknown = true;

  bool get isHomePage => id == null;
  bool get isDetailsPage => id != null;
}

class MyRouteInformationParser extends RouteInformationParser<AppRoutePath> {
  @override
  Future<AppRoutePath> parseRouteInformation(RouteInformation routeInformation) async {
    final uri = Uri.parse(routeInformation.location!);

    // Handle '/'
    if (uri.pathSegments.isEmpty) {
      return AppRoutePath.home();
    }

    // Handle '/details/:id'
    if (uri.pathSegments.length == 2) {
      if (uri.pathSegments[0] != 'details') return AppRoutePath.unknown();
      final id = int.tryParse(uri.pathSegments[1]);
      if (id == null) return AppRoutePath.unknown();
      return AppRoutePath.details(id);
    }

    // Handle unknown routes
    return AppRoutePath.unknown();
  }

  @override
  RouteInformation? restoreRouteInformation(AppRoutePath path) {
    if (path.isUnknown) {
      return const RouteInformation(location: '/404');
    }
    if (path.isHomePage) {
      return const RouteInformation(location: '/');
    }
    if (path.isDetailsPage) {
      return RouteInformation(location: '/details/${path.id}');
    }
    return null;
  }
}
```

#### MaterialApp.router

RouterDelegateとRouteInformationParserを統合します。

```dart
class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp.router(
      title: 'Navigator 2.0 Demo',
      routerDelegate: MyRouterDelegate(),
      routeInformationParser: MyRouteInformationParser(),
    );
  }
}
```

---

## 5 パッケージによる高度なルーティング

### 5.1 go_router（推奨パッケージ）

go_routerは、Navigator 2.0を簡単に使えるようにした公式推奨パッケージです。

#### 基本的な使用例

```dart
final GoRouter _router = GoRouter(
  routes: [
    GoRoute(
      path: '/',
      builder: (context, state) => HomePage(),
    ),
    GoRoute(
      path: '/details/:id',
      builder: (context, state) {
        final id = state.pathParameters['id']!;
        return DetailsPage(id: id);
      },
    ),
    GoRoute(
      path: '/settings',
      builder: (context, state) => SettingsPage(),
    ),
  ],
);

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp.router(
      routerConfig: _router,
    );
  }
}
```

#### 画面遷移

```dart
// パスで遷移
context.go('/details/123');

// pushで遷移（スタックに追加）
context.push('/settings');

// 戻る
context.pop();

// 置き換え
context.replace('/home');
```

#### ネストされたルート

```dart
final router = GoRouter(
  routes: [
    GoRoute(
      path: '/',
      builder: (context, state) => HomePage(),
      routes: [
        GoRoute(
          path: 'details/:id',
          builder: (context, state) {
            final id = state.pathParameters['id']!;
            return DetailsPage(id: id);
          },
        ),
      ],
    ),
  ],
);
```

#### リダイレクト（認証制御）

```dart
final router = GoRouter(
  redirect: (context, state) {
    final loggedIn = authService.isLoggedIn;
    final loggingIn = state.location == '/login';

    if (!loggedIn && !loggingIn) {
      return '/login';
    }
    if (loggedIn && loggingIn) {
      return '/';
    }
    return null;
  },
  routes: [...],
);
```

#### エラーハンドリング

```dart
final router = GoRouter(
  errorBuilder: (context, state) => ErrorPage(error: state.error),
  routes: [...],
);
```

---

### 5.2 auto_route

コード生成を用いた型安全なルーティングパッケージです。

#### ルート定義

```dart
@MaterialAutoRouter(
  replaceInRouteName: 'Page,Route',
  routes: <AutoRoute>[
    AutoRoute(page: HomePage, initial: true),
    AutoRoute(page: DetailsPage),
    AutoRoute(page: SettingsPage),
  ],
)
class $AppRouter {}
```

#### 使用例

```dart
// 遷移
context.router.push(DetailsRoute(id: 123));

// 戻る
context.router.pop();

// 置き換え
context.router.replace(HomeRoute());
```

---

### 5.3 beamer

階層的なルーティングとDeep Linkに強いパッケージです。

```dart
final beamerDelegate = BeamerDelegate(
  locationBuilder: RoutesLocationBuilder(
    routes: {
      '/': (context, state, data) => HomePage(),
      '/details/:id': (context, state, data) {
        final id = state.pathParameters['id']!;
        return DetailsPage(id: id);
      },
    },
  ),
);

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp.router(
      routerDelegate: beamerDelegate,
      routeInformationParser: BeamerParser(),
    );
  }
}
```

---

## 6 タブナビゲーション

### 6.1 BottomNavigationBar

```dart
class MainPage extends StatefulWidget {
  @override
  _MainPageState createState() => _MainPageState();
}

class _MainPageState extends State<MainPage> {
  int _currentIndex = 0;
  
  final List<Widget> _pages = [
    HomePage(),
    SearchPage(),
    ProfilePage(),
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: _pages[_currentIndex],
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: _currentIndex,
        onTap: (index) {
          setState(() {
            _currentIndex = index;
          });
        },
        items: const [
          BottomNavigationBarItem(icon: Icon(Icons.home), label: 'Home'),
          BottomNavigationBarItem(icon: Icon(Icons.search), label: 'Search'),
          BottomNavigationBarItem(icon: Icon(Icons.person), label: 'Profile'),
        ],
      ),
    );
  }
}
```

### 6.2 各タブで独立したNavigatorを持つ

```dart
class MainPage extends StatefulWidget {
  @override
  _MainPageState createState() => _MainPageState();
}

class _MainPageState extends State<MainPage> {
  int _currentIndex = 0;
  
  final List<GlobalKey<NavigatorState>> _navigatorKeys = [
    GlobalKey<NavigatorState>(),
    GlobalKey<NavigatorState>(),
    GlobalKey<NavigatorState>(),
  ];

  Widget _buildNavigator(int index) {
    return Navigator(
      key: _navigatorKeys[index],
      onGenerateRoute: (settings) {
        WidgetBuilder builder;
        switch (index) {
          case 0:
            builder = (context) => HomePage();
            break;
          case 1:
            builder = (context) => SearchPage();
            break;
          case 2:
            builder = (context) => ProfilePage();
            break;
          default:
            builder = (context) => HomePage();
        }
        return MaterialPageRoute(builder: builder);
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    return WillPopScope(
      onWillPop: () async {
        // 現在のタブのNavigatorで戻れるか確認
        return !await _navigatorKeys[_currentIndex].currentState!.maybePop();
      },
      child: Scaffold(
        body: IndexedStack(
          index: _currentIndex,
          children: [
            _buildNavigator(0),
            _buildNavigator(1),
            _buildNavigator(2),
          ],
        ),
        bottomNavigationBar: BottomNavigationBar(
          currentIndex: _currentIndex,
          onTap: (index) {
            setState(() {
              _currentIndex = index;
            });
          },
          items: const [
            BottomNavigationBarItem(icon: Icon(Icons.home), label: 'Home'),
            BottomNavigationBarItem(icon: Icon(Icons.search), label: 'Search'),
            BottomNavigationBarItem(icon: Icon(Icons.person), label: 'Profile'),
          ],
        ),
      ),
    );
  }
}
```

---

## 7 カスタムトランジション

### 7.1 PageRouteBuilderを使用

```dart
Navigator.push(
  context,
  PageRouteBuilder(
    pageBuilder: (context, animation, secondaryAnimation) => SecondPage(),
    transitionsBuilder: (context, animation, secondaryAnimation, child) {
      // フェードトランジション
      return FadeTransition(
        opacity: animation,
        child: child,
      );
    },
  ),
);
```

### 7.2 様々なトランジション

#### スライドトランジション

```dart
transitionsBuilder: (context, animation, secondaryAnimation, child) {
  const begin = Offset(1.0, 0.0);
  const end = Offset.zero;
  const curve = Curves.easeInOut;

  var tween = Tween(begin: begin, end: end).chain(CurveTween(curve: curve));
  var offsetAnimation = animation.drive(tween);

  return SlideTransition(
    position: offsetAnimation,
    child: child,
  );
}
```

#### スケールトランジション

```dart
transitionsBuilder: (context, animation, secondaryAnimation, child) {
  return ScaleTransition(
    scale: animation,
    child: child,
  );
}
```

#### 回転トランジション

```dart
transitionsBuilder: (context, animation, secondaryAnimation, child) {
  return RotationTransition(
    turns: animation,
    child: child,
  );
}
```

#### 複合トランジション

```dart
transitionsBuilder: (context, animation, secondaryAnimation, child) {
  return FadeTransition(
    opacity: animation,
    child: ScaleTransition(
      scale: animation,
      child: child,
    ),
  );
}
```

### 7.3 カスタムPageRoute

```dart
class FadePageRoute<T> extends PageRoute<T> {
  final WidgetBuilder builder;

  FadePageRoute({required this.builder});

  @override
  Color? get barrierColor => null;

  @override
  String? get barrierLabel => null;

  @override
  Widget buildPage(BuildContext context, Animation<double> animation,
      Animation<double> secondaryAnimation) {
    return builder(context);
  }

  @override
  Widget buildTransitions(BuildContext context, Animation<double> animation,
      Animation<double> secondaryAnimation, Widget child) {
    return FadeTransition(
      opacity: animation,
      child: child,
    );
  }

  @override
  bool get maintainState => true;

  @override
  Duration get transitionDuration => const Duration(milliseconds: 300);
}

// 使用例
Navigator.push(
  context,
  FadePageRoute(builder: (context) => SecondPage()),
);
```

---

## 8 Deep Link対応

### 8.1 Deep Linkとは

Deep Linkは、アプリ外部（Web URL、プッシュ通知、他のアプリ）からアプリ内の特定の画面に直接遷移する仕組みです。

### 8.2 Androidの設定（AndroidManifest.xml）

```xml
<activity
    android:name=".MainActivity"
    android:launchMode="singleTop">
    <intent-filter>
        <action android:name="android.intent.action.VIEW" />
        <category android:name="android.intent.category.DEFAULT" />
        <category android:name="android.intent.category.BROWSABLE" />
        <data
            android:scheme="myapp"
            android:host="example.com" />
    </intent-filter>
</activity>
```

### 8.3 iOSの設定（Info.plist）

```xml
<key>CFBundleURLTypes</key>
<array>
    <dict>
        <key>CFBundleURLSchemes</key>
        <array>
            <string>myapp</string>
        </array>
    </dict>
</array>
```

### 8.4 uni_linksパッケージを使用

```dart
import 'package:uni_links/uni_links.dart';

class MyApp extends StatefulWidget {
  @override
  _MyAppState createState() => _MyAppState();
}

class _MyAppState extends State<MyApp> {
  StreamSubscription? _sub;

  @override
  void initState() {
    super.initState();
    _handleIncomingLinks();
    _handleInitialUri();
  }

  void _handleIncomingLinks() {
    _sub = uriLinkStream.listen((Uri? uri) {
      if (uri != null) {
        _navigateToPage(uri);
      }
    });
  }

  Future<void> _handleInitialUri() async {
    try {
      final uri = await getInitialUri();
      if (uri != null) {
        _navigateToPage(uri);
      }
    } catch (e) {
      print('Failed to get initial URI: $e');
    }
  }

  void _navigateToPage(Uri uri) {
    // myapp://example.com/details/123
    if (uri.pathSegments.isNotEmpty && uri.pathSegments[0] == 'details') {
      final id = uri.pathSegments.length > 1 ? uri.pathSegments[1] : null;
      if (id != null) {
        Navigator.pushNamed(context, '/details', arguments: {'id': id});
      }
    }
  }

  @override
  void dispose() {
    _sub?.cancel();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      routes: {
        '/': (context) => HomePage(),
        '/details': (context) => DetailsPage(),
      },
    );
  }
}
```

### 8.5 go_routerでのDeep Link対応

go_routerを使用すると、Deep Linkが自動的に処理されます。

```dart
final router = GoRouter(
  routes: [
    GoRoute(
      path: '/',
      builder: (context, state) => HomePage(),
    ),
    GoRoute(
      path: '/details/:id',
      builder: (context, state) {
        final id = state.pathParameters['id']!;
        return DetailsPage(id: id);
      },
    ),
  ],
);

// myapp://example.com/details/123 が自動的に処理される
```

---

## 9 パフォーマンス最適化

### 9.1 遅延ロード（Lazy Loading）

```dart
// ✅ 良い例: 必要になるまで画面を構築しない
Navigator.push(
  context,
  MaterialPageRoute(builder: (context) => HeavyPage()),
);

// ❌ 悪い例: 事前にインスタンス化
final heavyPage = HeavyPage(); // メモリを消費
Navigator.push(
  context,
  MaterialPageRoute(builder: (context) => heavyPage),
);
```

### 9.2 画面の事前キャッシュ

```dart
// 次の画面を事前に準備
void precacheNextPage(BuildContext context) {
  precacheImage(AssetImage('assets/next_page_background.png'), context);
}
```

### 9.3 トランジションの最適化

```dart
// transitionDurationを調整
class FastPageRoute<T> extends MaterialPageRoute<T> {
  FastPageRoute({required WidgetBuilder builder}) : super(builder: builder);

  @override
  Duration get transitionDuration => const Duration(milliseconds: 200);
}
```

### 9.4 メモリ管理

```dart
class HeavyPage extends StatefulWidget {
  @override
  _HeavyPageState createState() => _HeavyPageState();
}

class _HeavyPageState extends State<HeavyPage> {
  late StreamSubscription _subscription;

  @override
  void initState() {
    super.initState();
    _subscription = someStream.listen((data) {
      // データ処理
    });
  }

  @override
  void dispose() {
    // リソースを解放
    _subscription.cancel();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(/* ... */);
  }
}
```

---

## 10 テスト戦略

### 10.1 ナビゲーションのテスト

```dart
testWidgets('Navigate to details page', (tester) async {
  await tester.pumpWidget(MaterialApp(home: HomePage()));

  // ボタンをタップ
  await tester.tap(find.text('Go to Details'));
  await tester.pumpAndSettle();

  // 遷移先の画面が表示されているか確認
  expect(find.byType(DetailsPage), findsOneWidget);
});
```

### 10.2 データ受け渡しのテスト

```dart
testWidgets('Pass data to details page', (tester) async {
  await tester.pumpWidget(MaterialApp(home: HomePage()));

  await tester.tap(find.text('Item 123'));
  await tester.pumpAndSettle();

  // データが正しく表示されているか確認
  expect(find.text('ID: 123'), findsOneWidget);
});
```

### 10.3 戻る操作のテスト

```dart
testWidgets('Navigate back', (tester) async {
  await tester.pumpWidget(MaterialApp(
    routes: {
      '/': (context) => HomePage(),
      '/details': (context) => DetailsPage(),
    },
  ));

  // 詳細画面へ遷移
  await tester.tap(find.text('Go to Details'));
  await tester.pumpAndSettle();
  expect(find.byType(DetailsPage), findsOneWidget);

  // 戻るボタンをタップ
  await tester.tap(find.byType(BackButton));
  await tester.pumpAndSettle();

  // ホーム画面に戻ったか確認
  expect(find.byType(HomePage), findsOneWidget);
});
```

### 10.4 Navigator 2.0のテスト

```dart
testWidgets('Navigator 2.0 routing', (tester) async {
  final routerDelegate = MyRouterDelegate();
  final routeInformationParser = MyRouteInformationParser();

  await tester.pumpWidget(
    MaterialApp.router(
      routerDelegate: routerDelegate,
      routeInformationParser: routeInformationParser,
    ),
  );

  // 初期状態の確認
  expect(find.byType(HomePage), findsOneWidget);

  // 状態を変更してナビゲーション
  routerDelegate.showDetails(123);
  await tester.pumpAndSettle();

  // 詳細画面が表示されているか確認
  expect(find.byType(DetailsPage), findsOneWidget);
});
```

---

## 11 ベストプラクティス

### 11.1 ルート管理の原則

- **小規模アプリ**: Navigator 1.0で十分
- **中規模アプリ**: 名前付きルートまたはgo_router
- **大規模アプリ**: Navigator 2.0またはgo_router/auto_route
- **Web対応アプリ**: 必ずNavigator 2.0または対応パッケージを使用

### 11.2 状態管理との統合

```dart
// ProviderとNavigatorの統合例
class AppState extends ChangeNotifier {
  int? _selectedItemId;
  
  int? get selectedItemId => _selectedItemId;
  
  void selectItem(int id) {
    _selectedItemId = id;
    notifyListeners();
  }
  
  void clearSelection() {
    _selectedItemId = null;
    notifyListeners();
  }
}

// RouterDelegateで状態を監視
class MyRouterDelegate extends RouterDelegate<AppRoutePath>
    with ChangeNotifier, PopNavigatorRouterDelegateMixin<AppRoutePath> {
  
  final AppState appState;
  
  MyRouterDelegate(this.appState) {
    appState.addListener(notifyListeners);
  }
  
  @override
  Widget build(BuildContext context) {
    return Navigator(
      pages: [
        MaterialPage(child: HomePage()),
        if (appState.selectedItemId != null)
          MaterialPage(child: DetailsPage(id: appState.selectedItemId!)),
      ],
      onPopPage: (route, result) {
        if (!route.didPop(result)) return false;
        appState.clearSelection();
        return true;
      },
    );
  }
}
```

### 11.3 認証フロー

```dart
// go_routerでの認証制御
final router = GoRouter(
  refreshListenable: authService, // 認証状態が変わったら再評価
  redirect: (context, state) {
    final loggedIn = authService.isLoggedIn;
    final loggingIn = state.location == '/login';

    // 未ログインでログイン画面以外にアクセスしようとした場合
    if (!loggedIn && !loggingIn) {
      return '/login';
    }

    // ログイン済みでログイン画面にアクセスしようとした場合
    if (loggedIn && loggingIn) {
      return '/';
    }

    // リダイレクト不要
    return null;
  },
  routes: [
    GoRoute(path: '/login', builder: (context, state) => LoginPage()),
    GoRoute(path: '/', builder: (context, state) => HomePage()),
    GoRoute(path: '/profile', builder: (context, state) => ProfilePage()),
  ],
);
```

### 11.4 エラーハンドリング

```dart
class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      onGenerateRoute: (settings) {
        try {
          // ルート生成ロジック
          return MaterialPageRoute(builder: (context) => SomePage());
        } catch (e) {
          // エラーページを表示
          return MaterialPageRoute(
            builder: (context) => ErrorPage(error: e.toString()),
          );
        }
      },
      onUnknownRoute: (settings) {
        return MaterialPageRoute(builder: (context) => NotFoundPage());
      },
    );
  }
}
```

---

## 12 研究・応用のヒント

### 12.1 ナビゲーショングラフの形式化

- 画面遷移を有向グラフとしてモデル化
- 到達可能性や循環の検出
- 最適な遷移パスの計算

### 12.2 ユーザー行動分析

- 画面遷移パターンの記録と分析
- ファネル分析による離脱ポイントの特定
- A/Bテストによる最適な遷移フローの検証

### 12.3 アクセシビリティ研究

- スクリーンリーダーでのナビゲーション体験の最適化
- キーボードナビゲーションの実装
- フォーカス管理の自動化

### 12.4 パフォーマンス研究

- 遷移アニメーションのフレームレート測定
- メモリ使用量の最適化
- 大規模アプリでのルーティングパフォーマンス

---

## 13 参考文献

- Flutter公式ドキュメント: [Navigation and routing](https://flutter.dev/docs/development/ui/navigation)
- Navigator 2.0: [Learning Flutter's new navigation and routing system](https://medium.com/flutter/learning-flutters-new-navigation-and-routing-system-7c9068155ade)
- go_router: [pub.dev/packages/go_router](https://pub.dev/packages/go_router)
- auto_route: [pub.dev/packages/auto_route](https://pub.dev/packages/auto_route)
- beamer: [pub.dev/packages/beamer](https://pub.dev/packages/beamer)
- uni_links: [pub.dev/packages/uni_links](https://pub.dev/packages/uni_links)
- Deep Links: [flutter.dev/docs/development/ui/navigation/deep-linking](https://flutter.dev/docs/development/ui/navigation/deep-linking)

---

作成者: 自動生成ドキュメント

最終更新: 2025-10-21
