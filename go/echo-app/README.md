# Go API Sample

このプロジェクトは、Goのベストプラクティスに従った標準的なディレクトリ構造を持つREST APIのサンプルです。

## ディレクトリ構造

```
go-app/
├── cmd/
│   └── api/              # アプリケーションのエントリーポイント
│       └── main.go
├── internal/             # プライベートなアプリケーションコード
│   ├── config/           # 設定管理
│   │   └── config.go
│   ├── domain/           # ビジネスロジックとエンティティ
│   │   └── sample.go
│   ├── handler/          # HTTPハンドラー
│   │   ├── health_handler.go
│   │   └── sample_handler.go
│   ├── repository/       # データアクセス層
│   │   ├── sample_repository.go
│   │   └── sample_repository_memory.go
│   ├── router/           # ルーティング設定
│   │   └── router.go
│   └── service/          # ビジネスロジック層
│       └── sample_service.go
├── pkg/                  # 外部から利用可能なライブラリコード
│   └── graph/            # GraphQL関連（将来の拡張用）
├── go.mod
├── go.sum
└── README.md
```

## レイヤー構造

このプロジェクトは、クリーンアーキテクチャの原則に従っています：

1. **Domain Layer** (`internal/domain/`)
   - ビジネスエンティティと値オブジェクト
   - 他のレイヤーに依存しない

2. **Repository Layer** (`internal/repository/`)
   - データアクセスのインターフェースと実装
   - インメモリ実装を提供

3. **Service Layer** (`internal/service/`)
   - ビジネスロジック
   - Repositoryを使用してデータを操作

4. **Handler Layer** (`internal/handler/`)
   - HTTPリクエスト/レスポンスの処理
   - Serviceを呼び出してビジネスロジックを実行

5. **Router Layer** (`internal/router/`)
   - ルーティング設定とミドルウェア

## API エンドポイント

### ヘルスチェック
- `GET /health` - アプリケーションの状態確認

### Sample API
- `GET /api/v1/samples` - すべてのサンプルを取得
- `GET /api/v1/samples/:id` - IDでサンプルを取得
- `POST /api/v1/samples` - 新しいサンプルを作成
- `PUT /api/v1/samples/:id` - サンプルを更新
- `DELETE /api/v1/samples/:id` - サンプルを削除

## 使用例

### サンプルの作成
```bash
curl -X POST http://localhost:8080/api/v1/samples \
  -H "Content-Type: application/json" \
  -d '{"name":"Sample 1"}'
```

### すべてのサンプルを取得
```bash
curl http://localhost:8080/api/v1/samples
```

### IDでサンプルを取得
```bash
curl http://localhost:8080/api/v1/samples/{id}
```

### サンプルの更新
```bash
curl -X PUT http://localhost:8080/api/v1/samples/{id} \
  -H "Content-Type: application/json" \
  -d '{"name":"Updated Sample"}'
```

### サンプルの削除
```bash
curl -X DELETE http://localhost:8080/api/v1/samples/{id}
```

## ビルドと実行

### ローカルでの実行
```bash
go run cmd/api/main.go
```

### ビルド
```bash
go build -o app ./cmd/api
./app
```

### Dockerでの実行
```bash
docker-compose build go-app
docker-compose up -d go-app
```

## 環境変数

- `PORT` - サーバーのポート番号（デフォルト: 8080）

## 技術スタック

- **Webフレームワーク**: Echo v4
- **UUID生成**: google/uuid
- **データストア**: インメモリ（本番環境ではデータベースに置き換え可能）

## 今後の拡張

- GraphQL サポート (`pkg/graph/`)
- データベース統合 (PostgreSQL, MySQL など)
- 認証・認可
- テストの追加
- ロギングの強化
- メトリクスとトレーシング

# ヘルスチェック
curl http://localhost:8080/health

# サンプル作成
curl -X POST http://localhost:8080/api/v1/samples \
  -H "Content-Type: application/json" \
  -d '{"name":"Test Sample"}'

# サンプル一覧取得
curl http://localhost:8080/api/v1/samples