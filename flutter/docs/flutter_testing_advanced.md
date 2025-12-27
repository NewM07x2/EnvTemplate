# Flutter Testing Advanced — 運用ガイド

このドキュメントは、Flutterにおける高度なテスト戦略とCI/CD運用について諸学者（研究者・教育者・上級学習者）向けに体系的かつ詳細にまとめた資料です。  
品質基準の維持、不具合の早期発見、自動化による継続的な品質保証、運用しやすいテスト設計までを網羅します。

---

## 目次

1. [テスト戦略の基礎概念](#1-テスト戦略の基礎概念)
2. [テストの種類と実装手法](#2-テストの種類と実装手法)
3. [CI/CD統合と自動化](#3-cicd統合と自動化)
4. [品質基準とメトリクス](#4-品質基準とメトリクス)
5. [テスト設計パターン](#5-テスト設計パターン)
6. [不具合防止の実践手法](#6-不具合防止の実践手法)
7. [ベストプラクティス](#7-ベストプラクティス)
8. [運用とメンテナンス](#8-運用とメンテナンス)
9. [参考文献](#9-参考文献)

---

## 1 テスト戦略の基礎概念

### 1.1 テストピラミッド

効果的なテスト戦略は、テストピラミッドに従います:

```text
       /\
      /  \     E2E/統合テスト (少数・高コスト)
     /────\
    /      \   ウィジェットテスト (中程度)
   /────────\
  /          \ ユニットテスト (多数・低コスト)
 /────────────\
```

**推奨比率:**

- ユニットテスト: 70%
- ウィジェットテスト: 20%
- 統合テスト: 10%

### 1.2 テストの目的

**品質保証の観点:**

- バグの早期発見
- リグレッション(機能退行)の防止
- コードの信頼性向上
- リファクタリングの安全性確保

**運用の観点:**

- 自動化による継続的な品質チェック
- レビュー負荷の軽減
- デプロイ前の自動検証
- 品質メトリクスの可視化

### 1.3 テストカバレッジの目標

**推奨カバレッジ:**

- ビジネスロジック: 80%以上
- UI層: 60%以上
- 統合フロー: 主要シナリオ100%

**カバレッジ測定:**

```bash
# カバレッジレポート生成
flutter test --coverage

# HTMLレポート生成（genhtml必要）
genhtml coverage/lcov.info -o coverage/html

# カバレッジ確認
open coverage/html/index.html
```

---

## 2 テストの種類と実装手法

### 2.1 ユニットテスト

#### ユニットテストの基本実装

```dart
// test/unit/calculator_test.dart
import 'package:flutter_test/flutter_test.dart';
import 'package:my_app/utils/calculator.dart';

void main() {
  group('Calculator', () {
    late Calculator calculator;

    setUp(() {
      calculator = Calculator();
    });

    test('add returns sum of two numbers', () {
      expect(calculator.add(2, 3), 5);
    });

    test('divide throws exception when divisor is zero', () {
      expect(
        () => calculator.divide(10, 0),
        throwsA(isA<ArgumentError>()),
      );
    });

    test('multiply handles negative numbers', () {
      expect(calculator.multiply(-2, 3), -6);
    });
  });
}
```

#### ビジネスロジックのテスト

```dart
// test/unit/user_service_test.dart
import 'package:flutter_test/flutter_test.dart';
import 'package:mockito/mockito.dart';
import 'package:mockito/annotations.dart';
import 'package:my_app/services/user_service.dart';
import 'package:my_app/repositories/user_repository.dart';

@GenerateMocks([UserRepository])
void main() {
  group('UserService', () {
    late UserService userService;
    late MockUserRepository mockRepository;

    setUp(() {
      mockRepository = MockUserRepository();
      userService = UserService(mockRepository);
    });

    test('getUser returns user when repository succeeds', () async {
      // Arrange
      final user = User(id: 1, name: 'Test User');
      when(mockRepository.fetchUser(1))
          .thenAnswer((_) async => user);

      // Act
      final result = await userService.getUser(1);

      // Assert
      expect(result, user);
      verify(mockRepository.fetchUser(1)).called(1);
    });

    test('getUser throws exception when repository fails', () async {
      // Arrange
      when(mockRepository.fetchUser(1))
          .thenThrow(Exception('Network error'));

      // Act & Assert
      expect(
        () => userService.getUser(1),
        throwsA(isA<Exception>()),
      );
    });
  });
}
```

---

### 2.2 ウィジェットテスト

#### 基本的なウィジェットテスト

```dart
// test/widget/login_form_test.dart
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:my_app/widgets/login_form.dart';

void main() {
  group('LoginForm Widget', () {
    testWidgets('displays email and password fields', (tester) async {
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: LoginForm(),
          ),
        ),
      );

      expect(find.byType(TextField), findsNWidgets(2));
      expect(find.text('Email'), findsOneWidget);
      expect(find.text('Password'), findsOneWidget);
    });

    testWidgets('shows error when email is invalid', (tester) async {
      await tester.pumpWidget(
        MaterialApp(home: Scaffold(body: LoginForm())),
      );

      // 無効なメールアドレスを入力
      await tester.enterText(
        find.byKey(Key('email_field')),
        'invalid-email',
      );
      await tester.tap(find.byType(ElevatedButton));
      await tester.pump();

      expect(find.text('Invalid email'), findsOneWidget);
    });

    testWidgets('calls onSubmit when form is valid', (tester) async {
      bool submitted = false;

      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: LoginForm(
              onSubmit: (email, password) {
                submitted = true;
              },
            ),
          ),
        ),
      );

      await tester.enterText(
        find.byKey(Key('email_field')),
        'test@example.com',
      );
      await tester.enterText(
        find.byKey(Key('password_field')),
        'password123',
      );
      await tester.tap(find.byType(ElevatedButton));
      await tester.pump();

      expect(submitted, true);
    });
  });
}
```

#### 非同期処理のテスト

```dart
testWidgets('shows loading indicator during async operation', (tester) async {
  await tester.pumpWidget(
    MaterialApp(home: UserProfilePage(userId: 1)),
  );

  // ローディングインジケータを確認
  expect(find.byType(CircularProgressIndicator), findsOneWidget);

  // 非同期処理完了まで待機
  await tester.pumpAndSettle();

  // データが表示されることを確認
  expect(find.byType(CircularProgressIndicator), findsNothing);
  expect(find.text('User Name'), findsOneWidget);
});
```

---

### 2.3 Goldenテスト(視覚的回帰テスト)

#### Goldenテストの実装

```dart
// test/golden/button_test.dart
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:my_app/widgets/custom_button.dart';

void main() {
  group('CustomButton Golden Tests', () {
    testWidgets('default state', (tester) async {
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: CustomButton(text: 'Click Me'),
          ),
        ),
      );

      await expectLater(
        find.byType(CustomButton),
        matchesGoldenFile('goldens/button_default.png'),
      );
    });

    testWidgets('disabled state', (tester) async {
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: CustomButton(
              text: 'Click Me',
              enabled: false,
            ),
          ),
        ),
      );

      await expectLater(
        find.byType(CustomButton),
        matchesGoldenFile('goldens/button_disabled.png'),
      );
    });
  });
}
```

#### Goldenファイルの更新

```bash
# Goldenファイルを生成/更新
flutter test --update-goldens

# 特定のテストのみ更新
flutter test test/golden/button_test.dart --update-goldens
```

---

### 2.4 統合テスト

#### 基本的な統合テスト

```dart
// integration_test/app_test.dart
import 'package:flutter_test/flutter_test.dart';
import 'package:integration_test/integration_test.dart';
import 'package:my_app/main.dart' as app;

void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  group('App Integration Tests', () {
    testWidgets('complete login flow', (tester) async {
      app.main();
      await tester.pumpAndSettle();

      // ログイン画面を確認
      expect(find.text('Login'), findsOneWidget);

      // メールアドレスとパスワードを入力
      await tester.enterText(
        find.byKey(Key('email_field')),
        'test@example.com',
      );
      await tester.enterText(
        find.byKey(Key('password_field')),
        'password123',
      );

      // ログインボタンをタップ
      await tester.tap(find.text('Login'));
      await tester.pumpAndSettle();

      // ホーム画面に遷移したことを確認
      expect(find.text('Home'), findsOneWidget);
    });

    testWidgets('navigation between screens', (tester) async {
      app.main();
      await tester.pumpAndSettle();

      // 設定画面へ遷移
      await tester.tap(find.byIcon(Icons.settings));
      await tester.pumpAndSettle();

      expect(find.text('Settings'), findsOneWidget);

      // 戻るボタンで戻る
      await tester.tap(find.byIcon(Icons.arrow_back));
      await tester.pumpAndSettle();

      expect(find.text('Home'), findsOneWidget);
    });
  });
}
```

---

### 2.5 モック（Mock）の活用

#### HTTPクライアントのモック

```dart
// test/mocks/mock_http_client.dart
import 'package:http/http.dart' as http;
import 'package:mockito/annotations.dart';
import 'package:mockito/mockito.dart';

@GenerateMocks([http.Client])
void main() {}

// test/services/api_service_test.dart
import 'package:flutter_test/flutter_test.dart';
import 'package:http/http.dart' as http;
import 'package:mockito/mockito.dart';
import 'package:my_app/services/api_service.dart';
import 'mocks/mock_http_client.mocks.dart';

void main() {
  group('ApiService', () {
    late ApiService apiService;
    late MockClient mockClient;

    setUp(() {
      mockClient = MockClient();
      apiService = ApiService(client: mockClient);
    });

    test('fetchUser returns User on successful response', () async {
      // Arrange
      when(mockClient.get(Uri.parse('https://api.example.com/users/1')))
          .thenAnswer(
        (_) async => http.Response(
          '{"id": 1, "name": "John Doe"}',
          200,
        ),
      );

      // Act
      final user = await apiService.fetchUser(1);

      // Assert
      expect(user.id, 1);
      expect(user.name, 'John Doe');
    });

    test('fetchUser throws exception on error response', () async {
      // Arrange
      when(mockClient.get(Uri.parse('https://api.example.com/users/1')))
          .thenAnswer((_) async => http.Response('Not Found', 404));

      // Act & Assert
      expect(() => apiService.fetchUser(1), throwsException);
    });
  });
}
```

#### Dioのモック

```dart
import 'package:dio/dio.dart';
import 'package:mockito/annotations.dart';

@GenerateMocks([Dio])
void main() {}

// テスト例
test('fetchData with Dio', () async {
  final mockDio = MockDio();
  when(mockDio.get('/data'))
      .thenAnswer((_) async => Response(
            data: {'key': 'value'},
            statusCode: 200,
            requestOptions: RequestOptions(path: '/data'),
          ));

  final result = await apiService.fetchData();
  expect(result['key'], 'value');
});
```

---

## 3 CI/CD統合と自動化

### 3.1 GitHub Actionsの設定

#### 基本的なワークフロー

```yaml
# .github/workflows/test.yml
name: Flutter Tests

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup Flutter
      uses: subosito/flutter-action@v2
      with:
        flutter-version: '3.16.0'
        channel: 'stable'
    
    - name: Install dependencies
      run: flutter pub get
    
    - name: Run analyzer
      run: flutter analyze
    
    - name: Run tests with coverage
      run: flutter test --coverage
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage/lcov.info
        fail_ci_if_error: true
    
    - name: Check coverage threshold
      run: |
        COVERAGE=$(lcov --summary coverage/lcov.info | grep lines | awk '{print $2}' | sed 's/%//')
        if (( $(echo "$COVERAGE < 80" | bc -l) )); then
          echo "Coverage is below 80%: $COVERAGE%"
          exit 1
        fi
```

#### Goldenテストの自動化

```yaml
# .github/workflows/golden_test.yml
name: Golden Tests

on:
  pull_request:
    branches: [ main ]

jobs:
  golden-test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup Flutter
      uses: subosito/flutter-action@v2
      with:
        flutter-version: '3.16.0'
    
    - name: Install dependencies
      run: flutter pub get
    
    - name: Run Golden Tests
      run: flutter test --update-goldens
    
    - name: Check for Golden file changes
      run: |
        if [[ -n $(git status --porcelain test/golden/goldens/) ]]; then
          echo "Golden files have changed. Please review."
          git diff test/golden/goldens/
          exit 1
        fi
```

---

### 3.2 品質ゲートの設定

#### 必須チェック項目

```yaml
# .github/workflows/quality_gate.yml
name: Quality Gate

on:
  pull_request:
    branches: [ main ]

jobs:
  quality-check:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup Flutter
      uses: subosito/flutter-action@v2
    
    - name: Install dependencies
      run: flutter pub get
    
    - name: Check formatting
      run: dart format --set-exit-if-changed .
    
    - name: Analyze code
      run: flutter analyze --fatal-infos
    
    - name: Run tests
      run: flutter test
    
    - name: Check test coverage
      run: |
        flutter test --coverage
        lcov --summary coverage/lcov.info
    
    - name: Build check (Android)
      run: flutter build apk --debug
    
    - name: Build check (iOS)
      run: flutter build ios --debug --no-codesign
```

---

### 3.3 自動デプロイの設定

#### Firebase App Distributionへの自動配布

```yaml
# .github/workflows/deploy_staging.yml
name: Deploy to Staging

on:
  push:
    branches: [ develop ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup Flutter
      uses: subosito/flutter-action@v2
    
    - name: Install dependencies
      run: flutter pub get
    
    - name: Run tests
      run: flutter test
    
    - name: Build APK
      run: flutter build apk --release
    
    - name: Upload to Firebase App Distribution
      uses: wzieba/Firebase-Distribution-Github-Action@v1
      with:
        appId: ${{ secrets.FIREBASE_APP_ID }}
        token: ${{ secrets.FIREBASE_TOKEN }}
        groups: testers
        file: build/app/outputs/flutter-apk/app-release.apk
```

---

## 4 品質基準とメトリクス

### 4.1 テストカバレッジ基準

#### カバレッジ目標

```dart
// coverage_threshold.dart
class CoverageThresholds {
  static const int minimumLineCoverage = 80;
  static const int minimumBranchCoverage = 70;
  static const int criticalPathCoverage = 100;
  
  static const Map<String, int> moduleCoverage = {
    'lib/services/': 90,
    'lib/repositories/': 85,
    'lib/models/': 70,
    'lib/ui/': 60,
  };
}
```

#### カバレッジレポートの自動生成

```bash
#!/bin/bash
# scripts/coverage_report.sh

# テスト実行とカバレッジ生成
flutter test --coverage

# HTMLレポート生成
genhtml coverage/lcov.info -o coverage/html

# カバレッジサマリー表示
echo "Coverage Summary:"
lcov --summary coverage/lcov.info

# 閾値チェック
COVERAGE=$(lcov --summary coverage/lcov.info | grep lines | awk '{print $2}' | sed 's/%//')
THRESHOLD=80

if (( $(echo "$COVERAGE < $THRESHOLD" | bc -l) )); then
  echo "❌ Coverage ($COVERAGE%) is below threshold ($THRESHOLD%)"
  exit 1
else
  echo "✅ Coverage ($COVERAGE%) meets threshold ($THRESHOLD%)"
fi
```

---

### 4.2 コード品質メトリクス

#### 静的解析の設定

```yaml
# analysis_options.yaml
include: package:flutter_lints/flutter.yaml

analyzer:
  exclude:
    - "**/*.g.dart"
    - "**/*.freezed.dart"
  errors:
    missing_required_param: error
    missing_return: error
    invalid_assignment: error
  language:
    strict-casts: true
    strict-raw-types: true

linter:
  rules:
    # エラー防止
    - always_declare_return_types
    - avoid_dynamic_calls
    - avoid_empty_else
    - avoid_return_types_on_setters
    - avoid_slow_async_io
    - avoid_type_to_string
    - cancel_subscriptions
    - close_sinks
    - literal_only_boolean_expressions
    - no_adjacent_strings_in_list
    - test_types_in_equals
    - throw_in_finally
    - unnecessary_statements
    - unrelated_type_equality_checks
    
    # スタイル
    - always_use_package_imports
    - avoid_print
    - prefer_const_constructors
    - prefer_const_declarations
    - prefer_final_fields
    - prefer_final_locals
    - unnecessary_this
    
    # ドキュメント
    - public_member_api_docs
```

---

### 4.3 パフォーマンステスト

#### ビルド時間の監視

```yaml
# .github/workflows/performance.yml
name: Performance Check

on:
  pull_request:
    branches: [ main ]

jobs:
  build-performance:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup Flutter
      uses: subosito/flutter-action@v2
    
    - name: Measure build time
      run: |
        START_TIME=$(date +%s)
        flutter build apk --release
        END_TIME=$(date +%s)
        BUILD_TIME=$((END_TIME - START_TIME))
        echo "Build time: ${BUILD_TIME}s"
        
        # 5分（300秒）を超えたら警告
        if [ $BUILD_TIME -gt 300 ]; then
          echo "⚠️  Build time exceeds 5 minutes"
          exit 1
        fi
```

---

## 5 テスト設計パターン

### 5.1 AAA（Arrange-Act-Assert）パターン

```dart
test('user authentication succeeds with valid credentials', () async {
  // Arrange（準備）
  final authService = AuthService();
  final email = 'test@example.com';
  final password = 'password123';
  
  // Act（実行）
  final result = await authService.login(email, password);
  
  // Assert（検証）
  expect(result.isSuccess, true);
  expect(result.user.email, email);
});
```

---

### 5.2 テストフィクスチャの再利用

```dart
// test/fixtures/user_fixtures.dart
class UserFixtures {
  static User createTestUser({
    int id = 1,
    String name = 'Test User',
    String email = 'test@example.com',
  }) {
    return User(id: id, name: name, email: email);
  }
  
  static List<User> createUserList(int count) {
    return List.generate(
      count,
      (index) => createTestUser(
        id: index + 1,
        name: 'User ${index + 1}',
        email: 'user${index + 1}@example.com',
      ),
    );
  }
}

// 使用例
test('displays user list', () async {
  final users = UserFixtures.createUserList(5);
  // テストコード...
});
```

---

### 5.3 ページオブジェクトパターン

```dart
// test/page_objects/login_page.dart
class LoginPage {
  final WidgetTester tester;
  
  LoginPage(this.tester);
  
  Future<void> enterEmail(String email) async {
    await tester.enterText(find.byKey(Key('email_field')), email);
  }
  
  Future<void> enterPassword(String password) async {
    await tester.enterText(find.byKey(Key('password_field')), password);
  }
  
  Future<void> tapLoginButton() async {
    await tester.tap(find.byType(ElevatedButton));
    await tester.pumpAndSettle();
  }
  
  Future<void> login(String email, String password) async {
    await enterEmail(email);
    await enterPassword(password);
    await tapLoginButton();
  }
}

// 使用例
testWidgets('login flow', (tester) async {
  await tester.pumpWidget(MyApp());
  
  final loginPage = LoginPage(tester);
  await loginPage.login('test@example.com', 'password123');
  
  expect(find.text('Home'), findsOneWidget);
});
```

---

## 6 不具合防止の実践手法

### 6.1 型安全性の強化

```dart
// ❌ 悪い例: 動的型の使用
dynamic fetchData() {
  return {'key': 'value'};
}

// ✅ 良い例: 明示的な型定義
Map<String, String> fetchData() {
  return {'key': 'value'};
}

// ✅ さらに良い例: カスタムクラスの使用
class ApiResponse {
  final String key;
  final String value;
  
  ApiResponse({required this.key, required this.value});
}

ApiResponse fetchData() {
  return ApiResponse(key: 'key', value: 'value');
}
```

---

### 6.2 Null安全性の徹底

```dart
// ✅ Null安全性を活用
String? getUserName(User? user) {
  return user?.name;
}

// ✅ 早期リターンでnullチェック
void processUser(User? user) {
  if (user == null) return;
  
  // この時点でuserはnon-null
  print(user.name);
}

// ✅ デフォルト値の提供
String getDisplayName(User? user) {
  return user?.name ?? 'Guest';
}
```

---

### 6.3 エラーハンドリングのテスト

```dart
test('handles network error gracefully', () async {
  // エラーケースのモック
  when(mockRepository.fetchData())
      .thenThrow(NetworkException('Connection failed'));
  
  // エラー時の動作を検証
  final result = await service.getData();
  
  expect(result.isError, true);
  expect(result.errorMessage, 'Connection failed');
});

test('retries on temporary failure', () async {
  var callCount = 0;
  when(mockRepository.fetchData()).thenAnswer((_) async {
    callCount++;
    if (callCount < 3) {
      throw NetworkException('Temporary error');
    }
    return TestData();
  });
  
  final result = await service.getDataWithRetry();
  
  expect(result.isSuccess, true);
  expect(callCount, 3);
});
```

---

### 6.4 境界値テスト

```dart
group('boundary value tests', () {
  test('handles empty list', () {
    final result = processItems([]);
    expect(result, isEmpty);
  });
  
  test('handles single item', () {
    final result = processItems([1]);
    expect(result.length, 1);
  });
  
  test('handles maximum allowed items', () {
    final items = List.generate(1000, (i) => i);
    final result = processItems(items);
    expect(result.length, 1000);
  });
  
  test('handles zero value', () {
    expect(calculator.divide(0, 5), 0);
  });
  
  test('handles negative values', () {
    expect(calculator.add(-5, -3), -8);
  });
});
```

---

## 7 ベストプラクティス

### 7.1 テストの命名規則

```dart
// ✅ 良い例: 明確で説明的な名前
test('calculateTotal returns sum of all items in cart', () {});
test('login throws exception when credentials are invalid', () {});
test('user profile updates successfully when all fields are valid', () {});

// ❌ 悪い例: 曖昧な名前
test('test1', () {});
test('it works', () {});
test('check function', () {});
```

---

### 7.2 テストの独立性

```dart
// ✅ 良い例: 各テストが独立
group('UserService', () {
  late UserService userService;
  late MockRepository mockRepository;
  
  setUp(() {
    mockRepository = MockRepository();
    userService = UserService(mockRepository);
  });
  
  test('test 1', () {
    // このテストの状態変更は他に影響しない
  });
  
  test('test 2', () {
    // 常に同じ初期状態から開始
  });
});

// ❌ 悪い例: テスト間で状態を共有
final sharedService = UserService(); // グローバル変数

test('test 1', () {
  sharedService.updateState(); // 他のテストに影響
});
```

---

### 7.3 テストデータの管理

```dart
// test/fixtures/test_data.dart
class TestData {
  static const validEmail = 'test@example.com';
  static const validPassword = 'password123';
  static const invalidEmail = 'invalid-email';
  
  static final sampleUser = User(
    id: 1,
    name: 'Test User',
    email: validEmail,
  );
  
  static final sampleUserList = [
    User(id: 1, name: 'User 1', email: 'user1@example.com'),
    User(id: 2, name: 'User 2', email: 'user2@example.com'),
    User(id: 3, name: 'User 3', email: 'user3@example.com'),
  ];
}
```

---

## 8 運用とメンテナンス

### 8.1 テストの定期実行

#### 夜間テストの自動実行

```yaml
# .github/workflows/nightly_tests.yml
name: Nightly Tests

on:
  schedule:
    - cron: '0 0 * * *'  # 毎日午前0時（UTC）

jobs:
  comprehensive-test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup Flutter
      uses: subosito/flutter-action@v2
    
    - name: Run all tests
      run: flutter test --coverage
    
    - name: Run integration tests
      run: flutter test integration_test/
    
    - name: Generate reports
      run: |
        flutter test --machine > test_results.json
        # レポート生成処理
    
    - name: Notify on failure
      if: failure()
      uses: 8398a7/action-slack@v3
      with:
        status: ${{ job.status }}
        text: 'Nightly tests failed'
        webhook_url: ${{ secrets.SLACK_WEBHOOK }}
```

---

### 8.2 テストメンテナンス戦略

#### フレーキーテストの検出

```bash
#!/bin/bash
# scripts/detect_flaky_tests.sh

# 各テストを10回実行
for i in {1..10}; do
  echo "Run $i"
  flutter test > "test_run_$i.log"
done

# 失敗したテストを抽出
grep "FAILED" test_run_*.log | sort | uniq -c | sort -nr
```

#### テストの定期レビュー

```dart
// テストメタデータの追加
// test/meta/test_metadata.dart
class TestMetadata {
  static const Map<String, DateTime> lastReviewed = {
    'user_service_test.dart': DateTime(2024, 10, 1),
    'login_flow_test.dart': DateTime(2024, 9, 15),
  };
  
  static bool needsReview(String testFile) {
    final lastReview = lastReviewed[testFile];
    if (lastReview == null) return true;
    
    final daysSinceReview = DateTime.now().difference(lastReview).inDays;
    return daysSinceReview > 90; // 90日以上経過したらレビュー
  }
}
```

---

### 8.3 テストドキュメントの整備

#### README.mdの例

```markdown
# テスト実行ガイド

## クイックスタート

```bash
# すべてのテストを実行
flutter test

# カバレッジ付きで実行
flutter test --coverage

# 特定のテストファイルのみ実行
flutter test test/services/user_service_test.dart
```

## テスト種別

### ユニットテスト

- 場所: `test/unit/`
- 実行: `flutter test test/unit/`
- 目的: ビジネスロジックの検証

### ウィジェットテスト

- 場所: `test/widget/`
- 実行: `flutter test test/widget/`
- 目的: UI コンポーネントの検証

### 統合テスト

- 場所: `integration_test/`
- 実行: `flutter test integration_test/`
- 目的: エンドツーエンドのシナリオ検証

## カバレッジの目標値

- 全体: 80%以上
- ビジネスロジック: 90%以上
- UI層: 60%以上

## CI/CD

- プルリクエスト作成時: すべてのテストを自動実行
- mainブランチへのマージ時: テスト + デプロイ
- 毎日深夜: 包括的なテストスイート実行

```markdown

---

## 9 参考文献

- Flutter公式テストガイド: [flutter.dev/docs/testing](https://flutter.dev/docs/testing)
- Mockito: [pub.dev/packages/mockito](https://pub.dev/packages/mockito)
- integration_test: [pub.dev/packages/integration_test](https://pub.dev/packages/integration_test)
- GitHub Actions for Flutter: [github.com/marketplace/actions/flutter-action](https://github.com/marketplace/actions/flutter-action)
- Flutter Test Best Practices: [flutter.dev/docs/cookbook/testing](https://flutter.dev/docs/cookbook/testing)
- Test-Driven Development: Kent Beck著

---

作成者: 自動生成ドキュメント

最終更新: 2025-10-22
