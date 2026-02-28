# Go + Echo API ガイド

> **対象者**: Go・Echo を初めて使う開発者  
> **関連テンプレート**: `go/echo-app/`・`next-go/echo-app/`  
> **所要時間**: 約 60 分

---

## 📚 目次

1. [Go と Echo とは](#1-go-と-echo-とは)
2. [環境構築](#2-環境構築)
3. [テンプレートの構造](#3-テンプレートの構造)
4. [Go の基本構文](#4-go-の基本構文)
5. [Echo の基本](#5-echo-の基本)
6. [レイヤードアーキテクチャ](#6-レイヤードアーキテクチャ)
7. [ミドルウェア](#7-ミドルウェア)
8. [バリデーション・エラーハンドリング](#8-バリデーションエラーハンドリング)
9. [Docker での起動](#9-docker-での起動)
10. [よく使うコマンド](#10-よく使うコマンド)

---

## 1. Go と Echo とは

### Go（Golang）

**Go** は Google が開発したシンプルで高速なプログラミング言語です。

```
特徴:
  ✅ コンパイル型 → バイナリ 1 つで動く（デプロイが簡単）
  ✅ 並行処理が得意（goroutine）
  ✅ メモリ消費が少ない
  ✅ 静的型付けで型安全
  ✅ ビルドが高速
```

### Echo

**Echo** は Go 向けの高パフォーマンスな Web フレームワークです。

```
特徴:
  ✅ シンプルな API
  ✅ ミドルウェアが充実（Logger / CORS / JWT 等）
  ✅ ルーティングが高速
  ✅ バリデーション組み込み
```

---

## 2. 環境構築

### Go のインストール

```bash
# Windows（winget）
winget install GoLang.Go

# Mac（Homebrew）
brew install go

# バージョン確認
go version
# go version go1.22.x
```

### VS Code 拡張機能

- **Go**（`golang.go`）をインストール
- インストール後、`Go: Install/Update Tools` コマンドを実行してツールをインストール

---

## 3. テンプレートの構造

```
go/echo-app/
├── cmd/
│   └── api/
│       └── main.go          ← エントリポイント
├── internal/
│   ├── config/              ← 環境変数の読み込み
│   ├── domain/              ← ドメインモデル（型定義）
│   ├── handler/             ← HTTP ハンドラー（Controller 相当）
│   ├── repository/          ← データアクセス層
│   ├── router/              ← ルーティング定義
│   └── service/             ← ビジネスロジック
├── docker/
│   └── Dockerfile
├── docker-compose.yml
├── go.mod                   ← モジュール定義（npm の package.json 相当）
└── go.sum                   ← 依存関係のハッシュ（package-lock.json 相当）
```

### リクエストの流れ

```
HTTP リクエスト
    ↓
Router（ルーティング）
    ↓
Handler（入力バリデーション・レスポンス組み立て）
    ↓
Service（ビジネスロジック）
    ↓
Repository（データアクセス）
    ↓
DB / インメモリストア
```

---

## 4. Go の基本構文

### 変数・型

```go
// 変数宣言（型推論）
name := "Alice"        // string
age := 25              // int
price := 9.99          // float64
isActive := true       // bool

// 明示的な型指定
var name string = "Alice"

// 複数宣言
var (
    host string = "localhost"
    port int    = 8080
)
```

### 構造体（TypeScript の interface / type に相当）

```go
// 構造体の定義
type User struct {
    ID        string    `json:"id"`
    Email     string    `json:"email"`
    Username  string    `json:"username"`
    CreatedAt time.Time `json:"created_at"`
}

// インスタンスの作成
user := User{
    ID:       "user-123",
    Email:    "alice@example.com",
    Username: "Alice",
}

// フィールドのアクセス
fmt.Println(user.Email)
```

### エラーハンドリング

Go では例外（try/catch）の代わりに **多値返却でエラーを返す**パターンを使います。

```go
// エラーを返す関数
func getUserByID(id string) (*User, error) {
    if id == "" {
        return nil, errors.New("id is required")
    }
    // ...処理
    return &user, nil
}

// 呼び出し側（必ずエラーチェックをする）
user, err := getUserByID("user-123")
if err != nil {
    log.Printf("Error: %v", err)
    return
}
fmt.Println(user.Email)
```

### スライス（配列）とマップ

```go
// スライス（動的配列）
names := []string{"Alice", "Bob", "Charlie"}
names = append(names, "Dave")   // 追加
fmt.Println(len(names))          // 長さ

// for range でループ
for i, name := range names {
    fmt.Printf("%d: %s\n", i, name)
}

// マップ（キーバリュー）
config := map[string]string{
    "host": "localhost",
    "port": "8080",
}
config["timeout"] = "30s"   // 追加・更新

value, ok := config["host"]  // ok = キーの存在確認
```

### インターフェース

```go
// インターフェース定義
type UserRepository interface {
    FindByID(ctx context.Context, id string) (*User, error)
    Create(ctx context.Context, user *User) error
}

// インターフェースを実装する構造体
type PostgresUserRepository struct {
    db *sql.DB
}

func (r *PostgresUserRepository) FindByID(ctx context.Context, id string) (*User, error) {
    // PostgreSQL から取得する実装
}

// テスト用のモック実装
type InMemoryUserRepository struct {
    users map[string]*User
}

func (r *InMemoryUserRepository) FindByID(ctx context.Context, id string) (*User, error) {
    user, ok := r.users[id]
    if !ok {
        return nil, errors.New("user not found")
    }
    return user, nil
}
```

---

## 5. Echo の基本

### ルーティング

```go
e := echo.New()

// HTTP メソッド別ルーティング
e.GET("/users", getUsers)
e.POST("/users", createUser)
e.PUT("/users/:id", updateUser)
e.DELETE("/users/:id", deleteUser)

// グループ化（プレフィックスをまとめる）
v1 := e.Group("/api/v1")
v1.GET("/users", getUsers)       // → /api/v1/users
v1.POST("/users", createUser)    // → /api/v1/users
```

### ハンドラーの書き方

```go
// GET /users → ユーザー一覧を返す
func getUsers(c echo.Context) error {
    users := []User{
        {ID: "1", Username: "Alice"},
        {ID: "2", Username: "Bob"},
    }
    return c.JSON(http.StatusOK, users)
}

// GET /users/:id → ID でユーザーを取得
func getUser(c echo.Context) error {
    id := c.Param("id")     // パスパラメータ
    
    user, err := userService.GetByID(c.Request().Context(), id)
    if err != nil {
        return c.JSON(http.StatusNotFound, map[string]string{"error": "user not found"})
    }
    return c.JSON(http.StatusOK, user)
}

// POST /users → ユーザーを作成
func createUser(c echo.Context) error {
    var input CreateUserInput
    
    // リクエストボディを構造体にバインド
    if err := c.Bind(&input); err != nil {
        return c.JSON(http.StatusBadRequest, map[string]string{"error": err.Error()})
    }
    
    // バリデーション
    if err := c.Validate(&input); err != nil {
        return c.JSON(http.StatusUnprocessableEntity, map[string]string{"error": err.Error()})
    }
    
    user, err := userService.Create(c.Request().Context(), &input)
    if err != nil {
        return c.JSON(http.StatusInternalServerError, map[string]string{"error": err.Error()})
    }
    return c.JSON(http.StatusCreated, user)
}
```

### クエリパラメータ

```go
// GET /users?page=1&limit=20&sort=name
func getUsers(c echo.Context) error {
    page, _ := strconv.Atoi(c.QueryParam("page"))
    if page <= 0 {
        page = 1
    }
    limit, _ := strconv.Atoi(c.QueryParam("limit"))
    if limit <= 0 {
        limit = 20
    }
    sort := c.QueryParam("sort")
    
    // ...
}
```

---

## 6. レイヤードアーキテクチャ

このテンプレートは Handler → Service → Repository の 3 層構造です。

### Domain（型定義）

```go
// internal/domain/sample.go
package domain

type Sample struct {
    ID          string `json:"id"`
    Name        string `json:"name"`
    Description string `json:"description,omitempty"`
}

type CreateSampleInput struct {
    Name        string `json:"name" validate:"required,min=1,max=100"`
    Description string `json:"description" validate:"max=500"`
}
```

### Repository（データアクセス層）

```go
// internal/repository/sample_repository.go
package repository

type SampleRepository interface {
    FindAll(ctx context.Context) ([]*domain.Sample, error)
    FindByID(ctx context.Context, id string) (*domain.Sample, error)
    Create(ctx context.Context, input *domain.CreateSampleInput) (*domain.Sample, error)
}

// インメモリ実装（テスト用）
type InMemorySampleRepository struct {
    data map[string]*domain.Sample
    mu   sync.RWMutex
}

func NewInMemorySampleRepository() *InMemorySampleRepository {
    return &InMemorySampleRepository{
        data: make(map[string]*domain.Sample),
    }
}
```

### Service（ビジネスロジック）

```go
// internal/service/sample_service.go
package service

type SampleService struct {
    repo repository.SampleRepository
}

func NewSampleService(repo repository.SampleRepository) *SampleService {
    return &SampleService{repo: repo}
}

func (s *SampleService) GetAll(ctx context.Context) ([]*domain.Sample, error) {
    return s.repo.FindAll(ctx)
}

func (s *SampleService) Create(ctx context.Context, input *domain.CreateSampleInput) (*domain.Sample, error) {
    // バリデーションやビジネスルールをここに書く
    return s.repo.Create(ctx, input)
}
```

---

## 7. ミドルウェア

```go
// router.go でのミドルウェア設定
e.Use(middleware.Logger())    // リクエストログ
e.Use(middleware.Recover())   // パニックからの回復
e.Use(middleware.CORS())      // CORS ヘッダー追加

// CORS の詳細設定
e.Use(middleware.CORSWithConfig(middleware.CORSConfig{
    AllowOrigins: []string{"http://localhost:3000", "https://example.com"},
    AllowMethods: []string{http.MethodGet, http.MethodPost, http.MethodPut, http.MethodDelete},
    AllowHeaders: []string{"Content-Type", "Authorization"},
}))

// レート制限
e.Use(middleware.RateLimiter(middleware.NewRateLimiterMemoryStore(20)))

// JWT 認証ミドルウェア（特定のルートに適用）
restricted := e.Group("/admin")
restricted.Use(middleware.JWT([]byte(os.Getenv("JWT_SECRET"))))
restricted.GET("/users", adminGetUsers)
```

---

## 8. バリデーション・エラーハンドリング

```go
// go-playground/validator を使ったバリデーション設定
import "github.com/go-playground/validator/v10"

type CustomValidator struct {
    validator *validator.Validate
}

func (cv *CustomValidator) Validate(i interface{}) error {
    return cv.validator.Struct(i)
}

// main.go で設定
e.Validator = &CustomValidator{validator: validator.New()}

// 入力構造体にタグでバリデーションを定義
type CreateUserInput struct {
    Email    string `json:"email" validate:"required,email"`
    Password string `json:"password" validate:"required,min=8"`
    Name     string `json:"name" validate:"required,min=1,max=50"`
}

// グローバルエラーハンドラー
e.HTTPErrorHandler = func(err error, c echo.Context) {
    code := http.StatusInternalServerError
    message := "Internal Server Error"

    if he, ok := err.(*echo.HTTPError); ok {
        code = he.Code
        message = fmt.Sprintf("%v", he.Message)
    }

    c.JSON(code, map[string]string{"error": message})
}
```

---

## 9. Docker での起動

```bash
cd go/echo-app

# コンテナを起動
docker compose up -d

# ログを確認
docker compose logs -f

# API の動作確認
curl http://localhost:8080/health
# → {"status":"ok"}

curl http://localhost:8080/api/v1/samples
# → []

curl -X POST http://localhost:8080/api/v1/samples \
  -H "Content-Type: application/json" \
  -d '{"name":"テスト","description":"サンプルデータ"}'
```

### Next.js との組み合わせ（`next-go/`）

```bash
cd next-go
docker compose up -d
# Next.js → http://localhost:3000
# Go API  → http://localhost:8080
```

Next.js から Go API を呼び出す：

```typescript
// next/src/lib/api.ts
const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8080'

export async function getSamples() {
  const res = await fetch(`${API_BASE}/api/v1/samples`)
  return res.json()
}
```

---

## 10. よく使うコマンド

```bash
# 依存関係をインストール
go mod tidy

# アプリを起動
go run ./cmd/api/main.go

# バイナリをビルド
go build -o bin/api ./cmd/api/main.go

# テストを実行
go test ./...

# テスト（詳細出力）
go test -v ./...

# カバレッジ
go test -cover ./...

# Lint（golangci-lint が必要）
golangci-lint run
```

---

## 📌 まとめ

| 概念 | Go の実装 | TypeScript の対応 |
|------|----------|----------------|
| 型定義 | `struct` | `interface` / `type` |
| モジュール | `go.mod` | `package.json` |
| 依存管理 | `go mod tidy` | `npm install` |
| エラー処理 | 多値返却 `(value, error)` | `try/catch` |
| 非同期 | goroutine / channel | Promise / async/await |
| テスト | `go test` | `vitest` / `jest` |
