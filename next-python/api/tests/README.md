# FastAPI pytest テストガイド

FastAPI + Strawberry GraphQL プロジェクトの完全なテスト環境です。このガイドでは、すぐにテストコードを書いて実行できるようになります。

## 目次

- [クイックスタート](#クイックスタート)
- [テストの実行](#テストの実行)
- [テスト構成](#テスト構成)
- [ユニットテスト](#ユニットテスト)
- [APIテスト](#APIテスト)
- [GraphQL テスト](#graphql-テスト)
- [非同期テスト](#非同期テスト)
- [モックとフィクスチャ](#モックとフィクスチャ)
- [ベストプラクティス](#ベストプラクティス)
- [トラブルシューティング](#トラブルシューティング)

## クイックスタート

### インストール

依存パッケージはすでに `requirements.txt` に含まれています。

```bash
# 依存パッケージのインストール
pip install -r requirements.txt
```

### 最初のテスト実行

```bash
# すべてのテストを実行
pytest

# 詳細出力付きで実行
pytest -v

# 特定のテストファイルを実行
pytest tests/test_services_example.py

# 特定のテストクラスを実行
pytest tests/test_api_routes_example.py::TestUserAPI

# 特定のテストを実行
pytest tests/test_api_routes_example.py::TestUserAPI::test_get_users -v

# カバレッジ付きで実行
pytest --cov=app --cov-report=html

# ウォッチモード（ファイル変更時に自動実行）
pytest-watch
```

## テストの実行

### コマンドラインオプション

```bash
# 詳細出力
pytest -v

# 非常に詳細な出力
pytest -vv

# 最初の失敗で停止
pytest -x

# 2番目の失敗で停止
pytest --maxfail=2

# 前回失敗したテストから実行
pytest --lf

# 前回失敗したテストを最初に実行
pytest --ff

# 出力を表示（print文が見える）
pytest -s

# マーカーで実行（例: unitテストのみ）
pytest -m unit

# パターンマッチでテストを実行
pytest -k "test_user"

# 特定の時間より遅いテストを表示
pytest --durations=10

# キャッシュをクリアして実行
pytest --cache-clear
```

### カバレッジレポート

```bash
# HTML形式のカバレッジレポート生成
pytest --cov=app --cov-report=html

# ブラウザで表示（Linuxの場合）
open htmlcov/index.html

# 特定のディレクトリのカバレッジ
pytest --cov=app/services --cov-report=html

# カバレッジの最小値を指定
pytest --cov=app --cov-fail-under=80
```

## テスト構成

### ディレクトリ構造

```
FastAPI/
├── tests/
│   ├── conftest.py                    # 共有フィクスチャとセットアップ
│   ├── test_services_example.py       # ユニットテストテンプレート
│   ├── test_api_routes_example.py     # API ルートテストテンプレート
│   ├── test_graphql_example.py        # GraphQL テストテンプレート
│   └── unit/                          # ユニットテスト（オプション）
│   └── integration/                   # 統合テスト（オプション）
├── app/
│   ├── main.py
│   ├── api/                           # APIルート
│   ├── services/                      # ビジネスロジック
│   ├── repositories/                  # データアクセス層
│   ├── schemas/                       # Pydantic スキーマ
│   ├── graphql/                       # GraphQL リゾルバ
│   └── utils/                         # ユーティリティ関数
├── pytest.ini                         # pytest 設定
└── requirements.txt                   # 依存パッケージ
```

### pytest.ini の設定

`pytest.ini` には以下の設定が含まれています：

- **asyncio_mode = auto** - 非同期テストの自動検出
- **testpaths = tests** - テストディレクトリの指定
- **addopts** - デフォルトのオプション
- **Coverage 設定** - カバレッジ除外パターン

## ユニットテスト

ユニットテストはサービス層、リポジトリ層、ユーティリティ関数をテストします。

### サービステストの例

```python
@pytest.mark.asyncio
async def test_get_user_by_id(mock_prisma_client, sample_user_data):
    """ユーザーをID で取得するテスト"""
    # Arrange - テストデータの準備
    user_id = 1
    mock_prisma_client.user.find_unique = AsyncMock(
        return_value=sample_user_data
    )
    
    # Act - テスト対象の関数を実行
    from app.services.user_service import UserService
    service = UserService(db=mock_prisma_client)
    result = await service.get_user(user_id)
    
    # Assert - 結果を検証
    assert result is not None
    assert result["email"] == "test@example.com"
    mock_prisma_client.user.find_unique.assert_called_once_with(
        where={"id": user_id}
    )
```

### リポジトリテストの例

```python
def test_user_repository_find_by_email(mock_prisma_client):
    """メールアドレスでユーザーを検索するテスト"""
    # Arrange
    email = "test@example.com"
    mock_prisma_client.user.find_unique = AsyncMock(
        return_value={"id": 1, "email": email}
    )
    
    # Act
    from app.repositories.user_repository import UserRepository
    repo = UserRepository(db=mock_prisma_client)
    result = repo.find_by_email(email)
    
    # Assert
    assert result is not None
    assert result["email"] == email
```

### バリデーションテストの例

```python
def test_validate_email():
    """メール形式のバリデーション"""
    from app.utils.validators import validate_email
    
    # 有効なメール
    assert validate_email("test@example.com") is True
    assert validate_email("user.name@domain.co.uk") is True
    
    # 無効なメール
    assert validate_email("invalid") is False
    assert validate_email("@example.com") is False
```

## API テスト

REST API エンドポイントのテストです。

### GET リクエストのテスト

```python
def test_get_users(client):
    """全ユーザーを取得するテスト"""
    response = client.get("/api/users")
    
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_user_by_id(client):
    """特定のユーザーを取得するテスト"""
    response = client.get("/api/users/1")
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert "email" in data

def test_get_user_not_found(client):
    """存在しないユーザーを取得するテスト"""
    response = client.get("/api/users/999")
    
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()
```

### POST リクエストのテスト

```python
def test_create_user(client):
    """新規ユーザー作成のテスト"""
    user_data = {
        "email": "newuser@example.com",
        "username": "newuser",
        "password": "SecurePass123!",
        "full_name": "New User",
    }
    
    response = client.post("/api/users", json=user_data)
    
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == user_data["email"]
    assert "id" in data
    assert "password" not in data  # パスワードは返さない

def test_create_user_invalid_email(client):
    """無効なメールで作成するテスト"""
    user_data = {
        "email": "invalid-email",
        "username": "newuser",
        "password": "SecurePass123!",
    }
    
    response = client.post("/api/users", json=user_data)
    
    assert response.status_code == 422  # Unprocessable Entity
    error = response.json()
    assert "email" in str(error).lower()
```

### 認証付きリクエストのテスト

```python
def test_update_user(client, auth_headers):
    """認証付きでユーザーを更新するテスト"""
    update_data = {"full_name": "Updated Name"}
    
    response = client.put(
        "/api/users/1",
        json=update_data,
        headers=auth_headers,  # 認証ヘッダーを追加
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["full_name"] == "Updated Name"

def test_update_user_unauthorized(client):
    """認証なしでは更新できないテスト"""
    update_data = {"full_name": "Updated Name"}
    
    response = client.put("/api/users/1", json=update_data)
    
    assert response.status_code == 401
```

## GraphQL テスト

Strawberry GraphQL のクエリとミューテーションをテストします。

### GraphQL クエリのテスト

```python
def test_query_all_users(client, graphql_query):
    """全ユーザーを取得するGraphQL クエリ"""
    query = """
        query {
            users {
                id
                email
                username
                fullName
            }
        }
    """
    
    response = client.post(
        "/graphql",
        json=graphql_query(query),
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "errors" not in data
    assert "users" in data["data"]
    assert isinstance(data["data"]["users"], list)

def test_query_user_by_id(client, graphql_query):
    """特定ユーザーを取得するGraphQL クエリ（変数付き）"""
    query = """
        query GetUser($id: Int!) {
            user(id: $id) {
                id
                email
                username
                fullName
            }
        }
    """
    variables = {"id": 1}
    
    response = client.post(
        "/graphql",
        json={
            "query": query,
            "variables": variables,
        },
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "errors" not in data
    assert data["data"]["user"]["id"] == 1
```

### GraphQL ミューテーションのテスト

```python
def test_mutation_create_user(client, graphql_query):
    """ユーザー作成のGraphQL ミューテーション"""
    mutation = """
        mutation CreateUser($email: String!, $username: String!, $password: String!) {
            createUser(email: $email, username: $username, password: $password) {
                id
                email
                username
            }
        }
    """
    variables = {
        "email": "newuser@example.com",
        "username": "newuser",
        "password": "SecurePass123!",
    }
    
    response = client.post(
        "/graphql",
        json={
            "query": mutation,
            "variables": variables,
        },
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "errors" not in data
    user = data["data"]["createUser"]
    assert user["email"] == "newuser@example.com"
    assert "id" in user

def test_mutation_delete_user(client, graphql_query, auth_headers):
    """ユーザー削除のGraphQL ミューテーション（認証付き）"""
    mutation = """
        mutation DeleteUser($id: Int!) {
            deleteUser(id: $id) {
                success
                message
            }
        }
    """
    variables = {"id": 1}
    
    response = client.post(
        "/graphql",
        json={
            "query": mutation,
            "variables": variables,
        },
        headers=auth_headers,
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "errors" not in data
    assert data["data"]["deleteUser"]["success"] is True
```

## 非同期テスト

FastAPI の非同期関数のテストです。

### 基本的な非同期テスト

```python
@pytest.mark.asyncio
async def test_async_function():
    """非同期関数のテスト"""
    from app.services.some_service import fetch_data
    
    result = await fetch_data()
    
    assert result is not None
```

### 非同期テスト（モック付き）

```python
@pytest.mark.asyncio
async def test_async_with_mock(mock_email_service):
    """モック付き非同期テスト"""
    from app.services.notification_service import send_email
    
    result = await send_email("user@example.com", mock_email_service)
    
    mock_email_service.send.assert_called_once()
    assert result is True
```

### 並行非同期操作のテスト

```python
@pytest.mark.asyncio
async def test_concurrent_operations(mock_prisma_client):
    """複数の非同期操作を並行実行するテスト"""
    import asyncio
    from app.services.user_service import UserService
    
    service = UserService(db=mock_prisma_client)
    mock_prisma_client.user.find_many = AsyncMock(return_value=[
        {"id": 1, "email": "user1@example.com"},
        {"id": 2, "email": "user2@example.com"},
    ])
    
    results = await asyncio.gather(
        service.get_users(),
        service.get_users(),
        service.get_users(),
    )
    
    assert len(results) == 3
    assert all(len(r) == 2 for r in results)
```

## モックとフィクスチャ

conftest.py に定義された便利なフィクスチャを活用します。

### 利用可能なフィクスチャ

#### クライアントフィクスチャ

```python
# 同期APIテスト用
def test_get_users(client):
    response = client.get("/api/users")
    assert response.status_code == 200

# 非同期テスト用
@pytest.mark.asyncio
async def test_async_operations(async_client):
    async with async_client as client:
        response = await client.get("/api/users")
        assert response.status_code == 200
```

#### データフィクスチャ

```python
def test_with_sample_data(sample_user_data, sample_post_data):
    """サンプルデータを使用するテスト"""
    assert sample_user_data["email"] == "test@example.com"
    assert sample_post_data["title"] == "Test Post"
```

#### モックサービス

```python
def test_email_notification(mock_email_service):
    """メールサービスのモック"""
    mock_email_service.send = AsyncMock(return_value=True)
    
    # テスト実装
    result = mock_email_service.send("user@example.com")
    assert result is True

def test_cache_service(mock_cache_service):
    """キャッシュサービスのモック"""
    mock_cache_service.get = AsyncMock(return_value=None)
    mock_cache_service.set = AsyncMock(return_value=True)
    
    # テスト実装
```

#### 認証フィクスチャ

```python
def test_protected_endpoint(client, auth_headers):
    """認証ヘッダー付きのテスト"""
    response = client.get("/api/protected", headers=auth_headers)
    assert response.status_code == 200

def test_invalid_auth(client, invalid_auth_headers):
    """無効な認証のテスト"""
    response = client.get("/api/protected", headers=invalid_auth_headers)
    assert response.status_code == 401
```

### カスタムフィクスチャの作成

```python
# conftest.py に追加
@pytest.fixture
def custom_db():
    """カスタムデータベースフィクスチャ"""
    db = MockDatabase()
    yield db
    db.cleanup()

# テストで使用
def test_with_custom_db(custom_db):
    result = custom_db.query("SELECT * FROM users")
    assert len(result) > 0
```

## ベストプラクティス

### 1. AAA パターン（Arrange-Act-Assert）

すべてのテストは次の3つのセクションに分けます：

```python
def test_example(client):
    # Arrange - テストデータの準備
    user_data = {"email": "test@example.com", "password": "pass123"}
    
    # Act - テスト対象の実行
    response = client.post("/api/users", json=user_data)
    
    # Assert - 結果の検証
    assert response.status_code == 201
```

### 2. 明確なテスト名

テスト関数の名前は何をテストしているか明確にしましょう：

```python
# 良い例
def test_create_user_with_valid_email():
    pass

# 悪い例
def test_user():
    pass
```

### 3. One Assertion Per Test（推奨）

各テストは1つの動作をテストします：

```python
# 良い例
def test_status_code_is_201(client):
    response = client.post("/api/users", json=user_data)
    assert response.status_code == 201

def test_response_contains_user_id(client):
    response = client.post("/api/users", json=user_data)
    assert "id" in response.json()

# 悪い例
def test_create_user(client):
    response = client.post("/api/users", json=user_data)
    assert response.status_code == 201
    assert "id" in response.json()
    assert response.json()["email"] == user_data["email"]
    # 多すぎる検証...
```

### 4. テスト間の独立性

各テストは他のテストに依存しないようにしましょう：

```python
# 良い例 - 各テストが独立している
@pytest.fixture
def user_id():
    return create_test_user()

def test_get_user(client, user_id):
    response = client.get(f"/api/users/{user_id}")
    assert response.status_code == 200

def test_update_user(client, user_id):
    response = client.put(f"/api/users/{user_id}", json={"name": "New Name"})
    assert response.status_code == 200
```

### 5. エラーケースのテスト

各機能について、成功ケースとエラーケースの両方をテストしましょう：

```python
# 成功ケース
def test_create_user_success(client):
    response = client.post("/api/users", json=valid_user_data)
    assert response.status_code == 201

# エラーケース
def test_create_user_invalid_email(client):
    response = client.post("/api/users", json={"email": "invalid"})
    assert response.status_code == 422

def test_create_user_duplicate_email(client):
    response = client.post("/api/users", json=duplicate_email_data)
    assert response.status_code == 409
```

### 6. テストマーカーの使用

テストをカテゴリ分けします：

```python
@pytest.mark.unit
def test_validate_email():
    pass

@pytest.mark.integration
@pytest.mark.asyncio
async def test_create_user_in_database():
    pass

@pytest.mark.slow
def test_heavy_operation():
    pass

# 実行: pytest -m unit  # ユニットテストのみ
# 実行: pytest -m "not slow"  # 遅いテストを除外
```

### 7. パラメータ化されたテスト

複数のデータでテストを実行します：

```python
@pytest.mark.parametrize("email,should_pass", [
    ("valid@example.com", True),
    ("invalid.email", False),
    ("@example.com", False),
    ("user@domain.co.uk", True),
])
def test_email_validation(email, should_pass):
    from app.utils.validators import validate_email
    assert validate_email(email) == should_pass
```

## トラブルシューティング

### よくある問題と解決方法

#### 1. "ImportError: cannot import name..."

**問題**: テストで app をインポートできない

```python
# 解決策: PYTHONPATH に src を追加
# Linuxの場合
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# Windowsの場合
set PYTHONPATH=%CD%;%PYTHONPATH%

# または pytest.ini に追加
[pytest]
pythonpath = .
```

#### 2. "asyncio.InvalidStateError"

**問題**: 非同期テストが正しく実行されていない

```python
# 解決策: @pytest.mark.asyncio を追加
@pytest.mark.asyncio  # これを忘れずに
async def test_async_function():
    pass
```

#### 3. "fixture not found"

**問題**: conftest.py のフィクスチャが見つからない

```python
# 解決策: conftest.py がテストディレクトリにあるか確認
# 正しい構造:
FastAPI/
├── tests/
│   ├── conftest.py  # ここにあるべき
│   └── test_*.py
```

#### 4. "database is locked"

**問題**: 複数のテストが同時に database にアクセス

```python
# 解決策: トランザクション隔離を使用
@pytest.fixture
async def db_transaction():
    async with db.transaction():
        yield db
        # ロールバック
```

#### 5. テストが遅い

**問題**: テスト実行に時間がかかる

```bash
# 解決策: 遅いテストを特定
pytest --durations=10

# 並行実行（pytest-xdist をインストール）
pip install pytest-xdist
pytest -n auto

# 特定のテストのみ実行
pytest tests/test_services_example.py -k "test_get_user"
```

### デバッグのコツ

#### 1. print デバッグ

```python
def test_example(client):
    print("テスト開始")
    response = client.get("/api/users")
    print(f"ステータスコード: {response.status_code}")
    print(f"レスポンス: {response.json()}")
    assert response.status_code == 200

# 実行: pytest -s  # -s で print が表示される
```

#### 2. PDB デバッガー

```python
def test_example(client):
    response = client.get("/api/users")
    breakpoint()  # または pdb.set_trace()
    assert response.status_code == 200
```

#### 3. テストの詳細表示

```bash
# 非常に詳細な出力
pytest -vv

# スタックトレース完全表示
pytest --tb=long

# 最初の失敗で停止
pytest -x
```

## まとめ

このテストセットアップにより、以下が可能です：

✅ **すぐにテストが書ける** - テンプレートファイルで即座に開始
✅ **REST API のテスト** - TestClient で簡単にエンドポイント検証
✅ **GraphQL のテスト** - クエリとミューテーション対応
✅ **非同期処理のテスト** - pytest-asyncio で async/await 対応
✅ **モック不要** - 付属のフィクスチャで各種テストに対応
✅ **デバッグが簡単** - 詳細なエラー表示とログ機能

テンプレートファイルのコメント部分を解除して、実装に合わせてカスタマイズしてください。
