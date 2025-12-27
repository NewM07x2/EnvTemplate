# Flutter Backend Communication — 詳細ガイド

このドキュメントは、Flutterにおけるバックエンド通信（HTTP通信、REST API、GraphQL、WebSocketなど）について諸学者（研究者・教育者・上級学習者）向けに体系的かつ詳細にまとめた資料です。  
通信の基本概念、標準ライブラリ、主要パッケージ、認証・セキュリティ、エラーハンドリング、キャッシュ戦略、パフォーマンス最適化、テスト戦略、研究応用までを網羅します。

---

## 目次

1. [バックエンド通信の基礎概念](#1-バックエンド通信の基礎概念)
2. [HTTP通信の標準手法](#2-http通信の標準手法)
3. [主要な通信パッケージ](#3-主要な通信パッケージ)
4. [REST API連携](#4-rest-api連携)
5. [GraphQL連携](#5-graphql連携)
6. [WebSocket・リアルタイム通信](#6-websocketリアルタイム通信)
7. [認証とセキュリティ](#7-認証とセキュリティ)
8. [エラーハンドリング](#8-エラーハンドリング)
9. [キャッシュ戦略](#9-キャッシュ戦略)
10. [パフォーマンス最適化](#10-パフォーマンス最適化)
11. [テスト戦略](#11-テスト戦略)
12. [ベストプラクティス](#12-ベストプラクティス)
13. [研究・応用のヒント](#13-研究応用のヒント)
14. [参考文献](#14-参考文献)

---

## 1 バックエンド通信の基礎概念

### 1.1 通信の種類

Flutterアプリケーションとバックエンドサーバー間の通信には、主に以下の種類があります:

- **HTTP/HTTPS通信**: 最も一般的なRESTful API通信
- **WebSocket**: 双方向リアルタイム通信
- **gRPC**: 高性能なRPC（Remote Procedure Call）
- **GraphQL**: クエリベースの柔軟なデータ取得
- **Server-Sent Events (SSE)**: サーバーからクライアントへの一方向ストリーミング

### 1.2 通信の基本フロー

1. **リクエスト準備**: エンドポイント、ヘッダー、ボディの設定
2. **リクエスト送信**: HTTPメソッド（GET, POST, PUT, DELETE等）でサーバーへ送信
3. **レスポンス受信**: サーバーからのレスポンスを受信
4. **データ解析**: JSON等のフォーマットをDartオブジェクトに変換
5. **状態更新**: UIへの反映
6. **エラーハンドリング**: 通信エラーやサーバーエラーの処理

### 1.3 非同期処理

Flutterでは、ネットワーク通信は必ず非同期で行います。

```dart
// Future を使用した非同期処理
Future<User> fetchUser(int id) async {
  final response = await http.get(Uri.parse('https://api.example.com/users/$id'));
  if (response.statusCode == 200) {
    return User.fromJson(jsonDecode(response.body));
  } else {
    throw Exception('Failed to load user');
  }
}

// Stream を使用した連続データ
Stream<Message> getMessages() async* {
  while (true) {
    await Future.delayed(Duration(seconds: 1));
    yield Message(text: 'New message', timestamp: DateTime.now());
  }
}
```

---

## 2 HTTP通信の標準手法

### 2.1 dart:io の HttpClient

Dart標準ライブラリの低レベルHTTPクライアントです。

```dart
import 'dart:io';
import 'dart:convert';

Future<void> fetchData() async {
  final client = HttpClient();
  try {
    final request = await client.getUrl(Uri.parse('https://api.example.com/data'));
    final response = await request.close();
    
    if (response.statusCode == 200) {
      final responseBody = await response.transform(utf8.decoder).join();
      final data = jsonDecode(responseBody);
      print(data);
    }
  } finally {
    client.close();
  }
}
```

#### 利点と欠点

**利点:**

- 標準ライブラリで追加依存なし
- 低レベル制御が可能
- ストリーム対応

**欠点:**

- 冗長なコード
- エラーハンドリングが煩雑
- インターセプター等の高度な機能がない

### 2.2 http パッケージ

Dart公式の高レベルHTTPクライアントです。

```dart
import 'package:http/http.dart' as http;
import 'dart:convert';

Future<User> fetchUser(int id) async {
  final response = await http.get(
    Uri.parse('https://api.example.com/users/$id'),
  );

  if (response.statusCode == 200) {
    return User.fromJson(jsonDecode(response.body));
  } else {
    throw Exception('Failed to load user');
  }
}

// POSTリクエスト
Future<User> createUser(String name, String email) async {
  final response = await http.post(
    Uri.parse('https://api.example.com/users'),
    headers: {'Content-Type': 'application/json'},
    body: jsonEncode({
      'name': name,
      'email': email,
    }),
  );

  if (response.statusCode == 201) {
    return User.fromJson(jsonDecode(response.body));
  } else {
    throw Exception('Failed to create user');
  }
}

// PUTリクエスト
Future<User> updateUser(int id, String name) async {
  final response = await http.put(
    Uri.parse('https://api.example.com/users/$id'),
    headers: {'Content-Type': 'application/json'},
    body: jsonEncode({'name': name}),
  );

  if (response.statusCode == 200) {
    return User.fromJson(jsonDecode(response.body));
  } else {
    throw Exception('Failed to update user');
  }
}

// DELETEリクエスト
Future<void> deleteUser(int id) async {
  final response = await http.delete(
    Uri.parse('https://api.example.com/users/$id'),
  );

  if (response.statusCode != 204) {
    throw Exception('Failed to delete user');
  }
}
```

---

## 3 主要な通信パッケージ

### 3.1 Dio（推奨HTTPクライアント）

強力で柔軟なHTTPクライアントパッケージです。

#### 特徴

- インターセプター（リクエスト/レスポンスの前後処理）
- FormData、マルチパート対応
- リクエストキャンセル
- タイムアウト設定
- 自動リトライ
- キャッシュサポート

#### 基本的な使用例

```dart
import 'package:dio/dio.dart';

class ApiClient {
  final Dio _dio = Dio(
    BaseOptions(
      baseUrl: 'https://api.example.com',
      connectTimeout: Duration(seconds: 5),
      receiveTimeout: Duration(seconds: 3),
      headers: {
        'Content-Type': 'application/json',
      },
    ),
  );

  ApiClient() {
    // インターセプターの追加
    _dio.interceptors.add(LogInterceptor(
      requestBody: true,
      responseBody: true,
    ));
  }

  Future<User> getUser(int id) async {
    try {
      final response = await _dio.get('/users/$id');
      return User.fromJson(response.data);
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }

  Future<User> createUser(String name, String email) async {
    try {
      final response = await _dio.post(
        '/users',
        data: {
          'name': name,
          'email': email,
        },
      );
      return User.fromJson(response.data);
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }

  Exception _handleError(DioException e) {
    if (e.type == DioExceptionType.connectionTimeout) {
      return Exception('Connection timeout');
    } else if (e.type == DioExceptionType.receiveTimeout) {
      return Exception('Receive timeout');
    } else if (e.response != null) {
      return Exception('Server error: ${e.response?.statusCode}');
    } else {
      return Exception('Network error: ${e.message}');
    }
  }
}
```

#### インターセプターの活用

```dart
class AuthInterceptor extends Interceptor {
  final TokenStorage _tokenStorage;

  AuthInterceptor(this._tokenStorage);

  @override
  void onRequest(RequestOptions options, RequestInterceptorHandler handler) async {
    // リクエスト前にトークンを追加
    final token = await _tokenStorage.getToken();
    if (token != null) {
      options.headers['Authorization'] = 'Bearer $token';
    }
    handler.next(options);
  }

  @override
  void onError(DioException err, ErrorInterceptorHandler handler) async {
    // 401エラー時にトークンをリフレッシュ
    if (err.response?.statusCode == 401) {
      try {
        final newToken = await _tokenStorage.refreshToken();
        // リトライ
        final options = err.requestOptions;
        options.headers['Authorization'] = 'Bearer $newToken';
        final response = await Dio().fetch(options);
        handler.resolve(response);
      } catch (e) {
        handler.next(err);
      }
    } else {
      handler.next(err);
    }
  }
}

// 使用例
final dio = Dio();
dio.interceptors.add(AuthInterceptor(tokenStorage));
```

#### ファイルアップロード

```dart
Future<void> uploadFile(File file) async {
  final formData = FormData.fromMap({
    'file': await MultipartFile.fromFile(
      file.path,
      filename: 'upload.jpg',
    ),
    'description': 'My photo',
  });

  final response = await dio.post('/upload', data: formData);
  print('Uploaded: ${response.data}');
}
```

#### ダウンロード進捗

```dart
Future<void> downloadFile(String url, String savePath) async {
  await dio.download(
    url,
    savePath,
    onReceiveProgress: (received, total) {
      if (total != -1) {
        print('${(received / total * 100).toStringAsFixed(0)}%');
      }
    },
  );
}
```

---

### 3.2 Retrofit（型安全なAPIクライアント）

アノテーションベースの型安全なHTTPクライアント生成ツールです。

#### 定義

```dart
import 'package:dio/dio.dart';
import 'package:retrofit/retrofit.dart';

part 'api_client.g.dart';

@RestApi(baseUrl: 'https://api.example.com')
abstract class ApiClient {
  factory ApiClient(Dio dio, {String baseUrl}) = _ApiClient;

  @GET('/users/{id}')
  Future<User> getUser(@Path('id') int id);

  @GET('/users')
  Future<List<User>> getUsers(@Query('page') int page);

  @POST('/users')
  Future<User> createUser(@Body() User user);

  @PUT('/users/{id}')
  Future<User> updateUser(@Path('id') int id, @Body() User user);

  @DELETE('/users/{id}')
  Future<void> deleteUser(@Path('id') int id);
}
```

#### 使用例

```dart
final dio = Dio();
final apiClient = ApiClient(dio);

// GET
final user = await apiClient.getUser(1);

// POST
final newUser = User(name: 'John', email: 'john@example.com');
final created = await apiClient.createUser(newUser);

// GET with query parameters
final users = await apiClient.getUsers(2);
```

---

## 4 REST API連携

### 4.1 RESTful API の基本

REST（Representational State Transfer）は、HTTPメソッドとURLを組み合わせてリソースを操作するアーキテクチャスタイルです。

| HTTPメソッド | 用途 | 例 |
|-------------|------|-----|
| GET | リソースの取得 | `GET /users` |
| POST | リソースの作成 | `POST /users` |
| PUT | リソースの更新（全体） | `PUT /users/1` |
| PATCH | リソースの部分更新 | `PATCH /users/1` |
| DELETE | リソースの削除 | `DELETE /users/1` |

### 4.2 データモデルとシリアライゼーション

#### 手動シリアライゼーション

```dart
class User {
  final int id;
  final String name;
  final String email;

  User({required this.id, required this.name, required this.email});

  // JSONからDartオブジェクトへ
  factory User.fromJson(Map<String, dynamic> json) {
    return User(
      id: json['id'],
      name: json['name'],
      email: json['email'],
    );
  }

  // DartオブジェクトからJSONへ
  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'name': name,
      'email': email,
    };
  }
}
```

#### json_serializable を使用した自動生成

```dart
import 'package:json_annotation/json_annotation.dart';

part 'user.g.dart';

@JsonSerializable()
class User {
  final int id;
  final String name;
  final String email;
  
  @JsonKey(name: 'created_at')
  final DateTime createdAt;

  User({
    required this.id,
    required this.name,
    required this.email,
    required this.createdAt,
  });

  factory User.fromJson(Map<String, dynamic> json) => _$UserFromJson(json);
  Map<String, dynamic> toJson() => _$UserToJson(this);
}
```

### 4.3 リポジトリパターン

データソースを抽象化し、ビジネスロジックと分離します。

```dart
abstract class UserRepository {
  Future<List<User>> getUsers();
  Future<User> getUser(int id);
  Future<User> createUser(String name, String email);
  Future<User> updateUser(int id, String name);
  Future<void> deleteUser(int id);
}

class UserRepositoryImpl implements UserRepository {
  final ApiClient _apiClient;

  UserRepositoryImpl(this._apiClient);

  @override
  Future<List<User>> getUsers() async {
    try {
      return await _apiClient.getUsers();
    } catch (e) {
      throw RepositoryException('Failed to fetch users: $e');
    }
  }

  @override
  Future<User> getUser(int id) async {
    try {
      return await _apiClient.getUser(id);
    } catch (e) {
      throw RepositoryException('Failed to fetch user: $e');
    }
  }

  @override
  Future<User> createUser(String name, String email) async {
    try {
      final user = User(id: 0, name: name, email: email);
      return await _apiClient.createUser(user);
    } catch (e) {
      throw RepositoryException('Failed to create user: $e');
    }
  }

  @override
  Future<User> updateUser(int id, String name) async {
    try {
      final user = await _apiClient.getUser(id);
      final updated = User(id: id, name: name, email: user.email);
      return await _apiClient.updateUser(id, updated);
    } catch (e) {
      throw RepositoryException('Failed to update user: $e');
    }
  }

  @override
  Future<void> deleteUser(int id) async {
    try {
      await _apiClient.deleteUser(id);
    } catch (e) {
      throw RepositoryException('Failed to delete user: $e');
    }
  }
}
```

---

## 5 GraphQL連携

### 5.1 GraphQLとは

GraphQLは、クエリ言語とランタイムを提供するAPIのための仕様です。

**特徴:**

- 必要なデータのみ取得可能
- 複数リソースを1回のリクエストで取得
- 型システムによる厳密なスキーマ
- リアルタイム更新（Subscription）

### 5.2 graphql_flutter パッケージ

```dart
import 'package:graphql_flutter/graphql_flutter.dart';

// GraphQLクライアントの設定
final HttpLink httpLink = HttpLink('https://api.example.com/graphql');

final AuthLink authLink = AuthLink(
  getToken: () async => 'Bearer $token',
);

final Link link = authLink.concat(httpLink);

final GraphQLClient client = GraphQLClient(
  cache: GraphQLCache(),
  link: link,
);
```

### 5.3 クエリ（Query）

```dart
const String getUserQuery = r'''
  query GetUser($id: ID!) {
    user(id: $id) {
      id
      name
      email
      posts {
        id
        title
      }
    }
  }
''';

Future<User> fetchUser(int id) async {
  final QueryOptions options = QueryOptions(
    document: gql(getUserQuery),
    variables: {'id': id},
  );

  final QueryResult result = await client.query(options);

  if (result.hasException) {
    throw Exception(result.exception.toString());
  }

  return User.fromJson(result.data!['user']);
}
```

### 5.4 ミューテーション（Mutation）

```dart
const String createUserMutation = r'''
  mutation CreateUser($name: String!, $email: String!) {
    createUser(input: {name: $name, email: $email}) {
      id
      name
      email
    }
  }
''';

Future<User> createUser(String name, String email) async {
  final MutationOptions options = MutationOptions(
    document: gql(createUserMutation),
    variables: {
      'name': name,
      'email': email,
    },
  );

  final QueryResult result = await client.mutate(options);

  if (result.hasException) {
    throw Exception(result.exception.toString());
  }

  return User.fromJson(result.data!['createUser']);
}
```

### 5.5 サブスクリプション（Subscription）

```dart
const String messageSubscription = r'''
  subscription OnMessageAdded {
    messageAdded {
      id
      text
      user {
        id
        name
      }
    }
  }
''';

Stream<Message> subscribeToMessages() {
  final SubscriptionOptions options = SubscriptionOptions(
    document: gql(messageSubscription),
  );

  return client.subscribe(options).map((result) {
    if (result.hasException) {
      throw Exception(result.exception.toString());
    }
    return Message.fromJson(result.data!['messageAdded']);
  });
}
```

---

## 6 WebSocket・リアルタイム通信

### 6.1 web_socket_channel パッケージ

```dart
import 'package:web_socket_channel/web_socket_channel.dart';

class WebSocketService {
  WebSocketChannel? _channel;
  
  void connect(String url) {
    _channel = WebSocketChannel.connect(Uri.parse(url));
  }

  Stream get stream => _channel!.stream;

  void send(String message) {
    _channel?.sink.add(message);
  }

  void disconnect() {
    _channel?.sink.close();
  }
}

// 使用例
final wsService = WebSocketService();
wsService.connect('wss://api.example.com/ws');

wsService.stream.listen(
  (message) {
    print('Received: $message');
  },
  onError: (error) {
    print('Error: $error');
  },
  onDone: () {
    print('Connection closed');
  },
);

wsService.send('Hello Server!');
```

### 6.2 socket_io_client パッケージ

```dart
import 'package:socket_io_client/socket_io_client.dart' as IO;

class SocketService {
  late IO.Socket socket;

  void connect() {
    socket = IO.io('https://api.example.com', <String, dynamic>{
      'transports': ['websocket'],
      'autoConnect': false,
    });

    socket.connect();

    socket.on('connect', (_) {
      print('Connected');
    });

    socket.on('message', (data) {
      print('Received: $data');
    });

    socket.on('disconnect', (_) {
      print('Disconnected');
    });
  }

  void send(String event, dynamic data) {
    socket.emit(event, data);
  }

  void disconnect() {
    socket.disconnect();
  }
}
```

---

## 7 認証とセキュリティ

### 7.1 JWT（JSON Web Token）認証

```dart
class AuthService {
  final Dio _dio;
  final SecureStorage _storage;

  AuthService(this._dio, this._storage);

  Future<void> login(String email, String password) async {
    final response = await _dio.post('/auth/login', data: {
      'email': email,
      'password': password,
    });

    final token = response.data['token'];
    final refreshToken = response.data['refresh_token'];

    await _storage.saveToken(token);
    await _storage.saveRefreshToken(refreshToken);
  }

  Future<String?> getToken() async {
    return await _storage.getToken();
  }

  Future<void> refreshToken() async {
    final refreshToken = await _storage.getRefreshToken();
    
    final response = await _dio.post('/auth/refresh', data: {
      'refresh_token': refreshToken,
    });

    final newToken = response.data['token'];
    await _storage.saveToken(newToken);
  }

  Future<void> logout() async {
    await _storage.deleteToken();
    await _storage.deleteRefreshToken();
  }
}
```

### 7.2 OAuth 2.0

```dart
import 'package:oauth2/oauth2.dart' as oauth2;

class OAuthService {
  static const authorizationEndpoint = Uri.parse('https://example.com/oauth/authorize');
  static const tokenEndpoint = Uri.parse('https://example.com/oauth/token');
  static const identifier = 'client_id';
  static const secret = 'client_secret';

  Future<oauth2.Client> authenticate() async {
    final grant = oauth2.AuthorizationCodeGrant(
      identifier,
      authorizationEndpoint,
      tokenEndpoint,
      secret: secret,
    );

    final authorizationUrl = grant.getAuthorizationUrl(
      Uri.parse('https://myapp.com/callback'),
      scopes: ['read', 'write'],
    );

    // ブラウザでauthorizationUrlを開く
    // コールバックでauthorization codeを取得

    final client = await grant.handleAuthorizationResponse(
      {'code': 'authorization_code'},
    );

    return client;
  }
}
```

### 7.3 SSL証明書のピンニング

```dart
import 'dart:io';

class SecureHttpClient {
  static HttpClient createHttpClient() {
    final client = HttpClient();
    
    client.badCertificateCallback = (X509Certificate cert, String host, int port) {
      // 証明書の検証
      const expectedFingerprint = 'SHA256_FINGERPRINT';
      final actualFingerprint = cert.sha256.toString();
      
      return actualFingerprint == expectedFingerprint;
    };
    
    return client;
  }
}
```

---

## 8 エラーハンドリング

### 8.1 エラーの分類

```dart
abstract class ApiException implements Exception {
  final String message;
  ApiException(this.message);
}

class NetworkException extends ApiException {
  NetworkException(String message) : super(message);
}

class ServerException extends ApiException {
  final int statusCode;
  ServerException(this.statusCode, String message) : super(message);
}

class TimeoutException extends ApiException {
  TimeoutException(String message) : super(message);
}

class UnauthorizedException extends ApiException {
  UnauthorizedException() : super('Unauthorized');
}

class NotFoundException extends ApiException {
  NotFoundException(String resource) : super('$resource not found');
}
```

### 8.2 統一的なエラーハンドリング

```dart
class ApiErrorHandler {
  static Exception handleError(dynamic error) {
    if (error is DioException) {
      switch (error.type) {
        case DioExceptionType.connectionTimeout:
        case DioExceptionType.sendTimeout:
        case DioExceptionType.receiveTimeout:
          return TimeoutException('Request timeout');
        
        case DioExceptionType.badResponse:
          return _handleStatusCode(error.response?.statusCode, error.response?.data);
        
        case DioExceptionType.cancel:
          return ApiException('Request cancelled');
        
        default:
          return NetworkException('Network error');
      }
    }
    return ApiException('Unknown error: $error');
  }

  static Exception _handleStatusCode(int? statusCode, dynamic data) {
    switch (statusCode) {
      case 400:
        return ServerException(400, 'Bad request: ${data['message']}');
      case 401:
        return UnauthorizedException();
      case 403:
        return ServerException(403, 'Forbidden');
      case 404:
        return NotFoundException(data['resource'] ?? 'Resource');
      case 500:
        return ServerException(500, 'Internal server error');
      default:
        return ServerException(statusCode ?? 0, 'Server error');
    }
  }
}
```

### 8.3 リトライ戦略

```dart
class RetryInterceptor extends Interceptor {
  final int maxRetries;
  final Duration retryDelay;

  RetryInterceptor({this.maxRetries = 3, this.retryDelay = const Duration(seconds: 1)});

  @override
  void onError(DioException err, ErrorInterceptorHandler handler) async {
    if (_shouldRetry(err)) {
      int retryCount = 0;
      
      while (retryCount < maxRetries) {
        await Future.delayed(retryDelay * (retryCount + 1));
        
        try {
          final response = await Dio().fetch(err.requestOptions);
          handler.resolve(response);
          return;
        } catch (e) {
          retryCount++;
          if (retryCount >= maxRetries) {
            handler.next(err);
            return;
          }
        }
      }
    } else {
      handler.next(err);
    }
  }

  bool _shouldRetry(DioException err) {
    return err.type == DioExceptionType.connectionTimeout ||
           err.type == DioExceptionType.receiveTimeout ||
           (err.response?.statusCode ?? 0) >= 500;
  }
}
```

---

## 9 キャッシュ戦略

### 9.1 dio_cache_interceptor

```dart
import 'package:dio_cache_interceptor/dio_cache_interceptor.dart';

final cacheOptions = CacheOptions(
  store: MemCacheStore(),
  policy: CachePolicy.request,
  hitCacheOnErrorExcept: [401, 403],
  maxStale: Duration(days: 7),
  priority: CachePriority.normal,
  cipher: null,
  keyBuilder: CacheOptions.defaultCacheKeyBuilder,
  allowPostMethod: false,
);

final dio = Dio()..interceptors.add(DioCacheInterceptor(options: cacheOptions));

// キャッシュを強制的に使用
await dio.get('/users', options: cacheOptions.toOptions().copyWith(
  policy: CachePolicy.forceCache,
));

// キャッシュをリフレッシュ
await dio.get('/users', options: cacheOptions.toOptions().copyWith(
  policy: CachePolicy.refresh,
));
```

### 9.2 カスタムキャッシュ実装

```dart
class CacheManager {
  final Map<String, CacheEntry> _cache = {};

  Future<T?> get<T>(String key) async {
    final entry = _cache[key];
    if (entry == null) return null;
    
    if (entry.isExpired()) {
      _cache.remove(key);
      return null;
    }
    
    return entry.data as T;
  }

  Future<void> set<T>(String key, T data, {Duration? ttl}) async {
    _cache[key] = CacheEntry(
      data: data,
      expiresAt: ttl != null ? DateTime.now().add(ttl) : null,
    );
  }

  Future<void> remove(String key) async {
    _cache.remove(key);
  }

  Future<void> clear() async {
    _cache.clear();
  }
}

class CacheEntry {
  final dynamic data;
  final DateTime? expiresAt;

  CacheEntry({required this.data, this.expiresAt});

  bool isExpired() {
    if (expiresAt == null) return false;
    return DateTime.now().isAfter(expiresAt!);
  }
}
```

---

## 10 パフォーマンス最適化

### 10.1 接続プーリング

```dart
final dio = Dio()
  ..options.persistentConnection = true
  ..httpClientAdapter = IOHttpClientAdapter(
    createHttpClient: () {
      final client = HttpClient();
      client.maxConnectionsPerHost = 5;
      return client;
    },
  );
```

### 10.2 圧縮

```dart
// gzip圧縮を有効化
final dio = Dio()
  ..options.headers['Accept-Encoding'] = 'gzip, deflate';
```

### 10.3 並列リクエスト

```dart
Future<void> fetchMultipleResources() async {
  final results = await Future.wait([
    dio.get('/users'),
    dio.get('/posts'),
    dio.get('/comments'),
  ]);

  final users = results[0].data;
  final posts = results[1].data;
  final comments = results[2].data;
}
```

### 10.4 ページネーション

```dart
class PaginatedApi {
  final Dio _dio;
  
  PaginatedApi(this._dio);

  Future<PaginatedResponse<User>> getUsers({
    int page = 1,
    int perPage = 20,
  }) async {
    final response = await _dio.get('/users', queryParameters: {
      'page': page,
      'per_page': perPage,
    });

    return PaginatedResponse<User>(
      data: (response.data['data'] as List)
          .map((json) => User.fromJson(json))
          .toList(),
      currentPage: response.data['current_page'],
      totalPages: response.data['total_pages'],
      totalItems: response.data['total'],
    );
  }
}

class PaginatedResponse<T> {
  final List<T> data;
  final int currentPage;
  final int totalPages;
  final int totalItems;

  PaginatedResponse({
    required this.data,
    required this.currentPage,
    required this.totalPages,
    required this.totalItems,
  });

  bool get hasNextPage => currentPage < totalPages;
}
```

---

## 11 テスト戦略

### 11.1 モックHTTPクライアント

```dart
import 'package:mockito/mockito.dart';
import 'package:http/http.dart' as http;

class MockClient extends Mock implements http.Client {}

void main() {
  test('fetchUser returns User if http call succeeds', () async {
    final client = MockClient();

    when(client.get(Uri.parse('https://api.example.com/users/1')))
        .thenAnswer((_) async => http.Response('{"id": 1, "name": "John"}', 200));

    final user = await fetchUser(client, 1);

    expect(user.name, 'John');
  });

  test('fetchUser throws exception if http call fails', () async {
    final client = MockClient();

    when(client.get(Uri.parse('https://api.example.com/users/1')))
        .thenAnswer((_) async => http.Response('Not Found', 404));

    expect(() => fetchUser(client, 1), throwsException);
  });
}
```

### 11.2 http_mock_adapter（Dioモック）

```dart
import 'package:dio/dio.dart';
import 'package:http_mock_adapter/http_mock_adapter.dart';

void main() {
  test('Dio mock test', () async {
    final dio = Dio();
    final dioAdapter = DioAdapter(dio: dio);

    dioAdapter.onGet(
      '/users/1',
      (server) => server.reply(200, {'id': 1, 'name': 'John'}),
    );

    final response = await dio.get('/users/1');
    expect(response.data['name'], 'John');
  });
}
```

### 11.3 統合テスト

```dart
testWidgets('User list loads and displays data', (tester) async {
  // モックサーバーを起動
  final mockServer = MockWebServer();
  await mockServer.start();

  mockServer.enqueue(body: jsonEncode([
    {'id': 1, 'name': 'Alice'},
    {'id': 2, 'name': 'Bob'},
  ]));

  await tester.pumpWidget(MyApp(apiUrl: mockServer.url));
  await tester.pumpAndSettle();

  expect(find.text('Alice'), findsOneWidget);
  expect(find.text('Bob'), findsOneWidget);

  await mockServer.shutdown();
});
```

---

## 12 ベストプラクティス

### 12.1 APIクライアントの抽象化

```dart
// インターフェース
abstract class ApiService {
  Future<List<User>> getUsers();
  Future<User> getUser(int id);
}

// 実装
class ApiServiceImpl implements ApiService {
  final Dio _dio;
  
  ApiServiceImpl(this._dio);

  @override
  Future<List<User>> getUsers() async {
    final response = await _dio.get('/users');
    return (response.data as List).map((json) => User.fromJson(json)).toList();
  }

  @override
  Future<User> getUser(int id) async {
    final response = await _dio.get('/users/$id');
    return User.fromJson(response.data);
  }
}

// モック実装（テスト用）
class MockApiService implements ApiService {
  @override
  Future<List<User>> getUsers() async {
    return [User(id: 1, name: 'Test User')];
  }

  @override
  Future<User> getUser(int id) async {
    return User(id: id, name: 'Test User');
  }
}
```

### 12.2 環境別設定

```dart
class ApiConfig {
  static String get baseUrl {
    const env = String.fromEnvironment('ENV', defaultValue: 'dev');
    
    switch (env) {
      case 'prod':
        return 'https://api.example.com';
      case 'staging':
        return 'https://staging-api.example.com';
      default:
        return 'https://dev-api.example.com';
    }
  }

  static Duration get timeout {
    return const Duration(seconds: 30);
  }
}
```

### 12.3 ログとモニタリング

```dart
class LoggingInterceptor extends Interceptor {
  final Logger _logger;

  LoggingInterceptor(this._logger);

  @override
  void onRequest(RequestOptions options, RequestInterceptorHandler handler) {
    _logger.info('REQUEST[${options.method}] => PATH: ${options.path}');
    handler.next(options);
  }

  @override
  void onResponse(Response response, ResponseInterceptorHandler handler) {
    _logger.info('RESPONSE[${response.statusCode}] => PATH: ${response.requestOptions.path}');
    handler.next(response);
  }

  @override
  void onError(DioException err, ErrorInterceptorHandler handler) {
    _logger.error('ERROR[${err.response?.statusCode}] => PATH: ${err.requestOptions.path}');
    handler.next(err);
  }
}
```

---

## 13 研究・応用のヒント

### 13.1 通信パターンの最適化研究

- リクエスト頻度とバッテリー消費の関係分析
- 最適なポーリング間隔の決定アルゴリズム
- キャッシュヒット率の最大化戦略

### 13.2 セキュリティ研究

- 通信の暗号化強度とパフォーマンストレードオフ
- 証明書ピンニングの実装パターン
- トークンリフレッシュの最適タイミング

### 13.3 ネットワーク品質適応

- ネットワーク速度に応じた画質調整
- オフラインファーストアーキテクチャ
- 段階的データロード（Progressive Loading）

### 13.4 APIバージョニング戦略

- セマンティックバージョニングの適用
- 後方互換性の保証
- グレースフルデグラデーション

---

## 14 参考文献

- Flutter公式ドキュメント: [Networking & HTTP](https://flutter.dev/docs/development/data-and-backend/networking)
- Dio パッケージ: [pub.dev/packages/dio](https://pub.dev/packages/dio)
- http パッケージ: [pub.dev/packages/http](https://pub.dev/packages/http)
- Retrofit: [pub.dev/packages/retrofit](https://pub.dev/packages/retrofit)
- graphql_flutter: [pub.dev/packages/graphql_flutter](https://pub.dev/packages/graphql_flutter)
- web_socket_channel: [pub.dev/packages/web_socket_channel](https://pub.dev/packages/web_socket_channel)
- OAuth 2.0 RFC: [RFC 6749](https://tools.ietf.org/html/rfc6749)
- JSON Web Token: [jwt.io](https://jwt.io)

---

作成者: 自動生成ドキュメント

最終更新: 2025-10-21
