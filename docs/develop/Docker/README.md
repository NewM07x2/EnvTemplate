# Docker 入門ガイド

> **対象者**: Docker を初めて使う開発者・このリポジトリのテンプレートを動かしたい方  
> **所要時間**: 約 60 分

---

## 📚 目次

1. [Docker とは](#1-docker-とは)
2. [インストール](#2-インストール)
3. [基本概念](#3-基本概念)
4. [Dockerfile の書き方](#4-dockerfile-の書き方)
5. [docker-compose の使い方](#5-docker-compose-の使い方)
6. [よく使うコマンド一覧](#6-よく使うコマンド一覧)
7. [このリポジトリでの使い方](#7-このリポジトリでの使い方)
8. [トラブルシューティング](#8-トラブルシューティング)

---

## 1. Docker とは

**Docker** は、アプリケーションとその実行環境を **コンテナ** という単位でまとめて管理するツールです。

```
従来の開発環境:
  開発者 A の PC: Node.js 18, PostgreSQL 15 → 動く
  開発者 B の PC: Node.js 20, PostgreSQL 16 → 動かない 😢
  本番サーバー:   Node.js 16              → 挙動が違う 😱

Docker を使った開発環境:
  全員が同じコンテナを使う → どこでも同じように動く ✅
```

### Docker のメリット

| メリット | 説明 |
|---------|------|
| **環境の統一** | チーム全員・本番環境で同じ環境を再現できる |
| **簡単なセットアップ** | コマンド 1 行でアプリ + DB を起動できる |
| **依存関係の隔離** | Node.js のバージョンが違うプロジェクトを同時に動かせる |
| **クリーンな削除** | コンテナを削除すれば PC に痕跡が残らない |

---

## 2. インストール

### Docker Desktop（Windows / Mac）

1. [Docker Desktop](https://www.docker.com/products/docker-desktop/) からインストーラーをダウンロード
2. インストール後、Docker Desktop を起動
3. ターミナルで確認：

```bash
docker --version
# Docker version 27.x.x, build xxxx

docker compose version
# Docker Compose version v2.x.x
```

> ⚠️ **Windows の場合**: WSL 2（Windows Subsystem for Linux）の有効化が必要です。  
> Docker Desktop のインストール時に案内が表示されます。

---

## 3. 基本概念

### イメージ（Image）

アプリを動かすための **設計図・テンプレート** です。

```
例: node:18-alpine  → Node.js 18 が入った軽量 Linux 環境
例: postgres:16     → PostgreSQL 16 が入った環境
例: nginx:latest    → Nginx（Web サーバー）が入った環境
```

### コンテナ（Container）

イメージから作られる **実際に動いているプロセス** です。

```
イメージ  ──（docker run）──→  コンテナ（実行中）
（設計図）                      （実際の建物）
```

### ボリューム（Volume）

コンテナを削除してもデータを**永続化**するための仕組みです。

```yaml
volumes:
  - postgres_data:/var/lib/postgresql/data  # DB データを永続化
  - .:/app                                  # ホスト PC のコードをコンテナにマウント
```

### ポートマッピング

ホスト PC とコンテナのポートを接続します。

```yaml
ports:
  - "3000:3000"  # ホスト:コンテナ
  # ブラウザで localhost:3000 → コンテナの 3000 番ポートへ転送
```

---

## 4. Dockerfile の書き方

`Dockerfile` はイメージの作り方を定義するファイルです。

### このリポジトリの Next.js 用 Dockerfile

```dockerfile
# ベースイメージを指定（Node.js 18 + 軽量 Alpine Linux）
FROM node:18-alpine

# コンテナ内の作業ディレクトリを設定
WORKDIR /app

# Alpine に必要な追加パッケージをインストール
RUN apk add --no-cache openssl

# 先に package.json だけコピー（依存関係のキャッシュを活かすため）
COPY package*.json ./

# npm パッケージをインストール
RUN npm install

# Prisma スキーマをコピーしてクライアントを生成
COPY prisma ./prisma/
RUN npx prisma generate

# アプリのソースコードをすべてコピー
COPY . .

# ポート 3000 を外部に公開
EXPOSE 3000

# コンテナ起動時に実行するコマンド
CMD ["npm", "run", "dev"]
```

### Dockerfile の主要な命令

| 命令 | 説明 | 例 |
|------|------|-----|
| `FROM` | ベースイメージを指定 | `FROM node:18-alpine` |
| `WORKDIR` | 作業ディレクトリを設定 | `WORKDIR /app` |
| `COPY` | ファイルをコンテナにコピー | `COPY . .` |
| `RUN` | ビルド時にコマンドを実行 | `RUN npm install` |
| `CMD` | コンテナ起動時のコマンド | `CMD ["npm", "start"]` |
| `EXPOSE` | 使用するポートを宣言 | `EXPOSE 3000` |
| `ENV` | 環境変数を設定 | `ENV NODE_ENV=production` |
| `ARG` | ビルド引数を定義 | `ARG APP_VERSION=1.0` |

### マルチステージビルド（本番用）

```dockerfile
# === ビルドステージ ===
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build

# === 実行ステージ（軽量） ===
FROM node:18-alpine AS runner
WORKDIR /app

# ビルド成果物だけをコピー（node_modules は含めない）
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static
COPY --from=builder /app/public ./public

EXPOSE 3000
CMD ["node", "server.js"]
```

> ✅ **マルチステージビルド**を使うと、本番イメージのサイズを大幅に削減できます（1GB → 200MB 以下）。

---

## 5. docker-compose の使い方

`docker-compose.yml` は、複数のコンテナをまとめて管理する設定ファイルです。

### このリポジトリの docker-compose.yml（Next.js + PostgreSQL）

```yaml
version: "3.8"

services:
  # Next.js アプリ
  app:
    build:
      context: .               # Dockerfile があるディレクトリ
      dockerfile: ./docker/Dockerfile
    ports:
      - "3000:3000"            # ホストPC:コンテナ
    volumes:
      - .:/app                 # ソースコードをリアルタイム同期（ホットリロード用）
      - /app/node_modules      # node_modules はコンテナ側を使う
    environment:
      - NODE_ENV=development
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/nextapp?schema=public
    depends_on:
      - db                     # db サービスが起動してから app を起動

  # PostgreSQL データベース
  db:
    image: postgres:16-alpine  # Dockerfile なしで公式イメージを直接使う
    restart: always
    ports:
      - "5432:5432"
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_DB=nextapp
    volumes:
      - postgres_data:/var/lib/postgresql/data  # データを永続化

# 名前付きボリューム（docker volume として管理）
volumes:
  postgres_data:
```

### 起動・停止コマンド

```bash
# コンテナをバックグラウンドで起動
docker compose up -d

# ログをリアルタイム確認（Ctrl+C で終了）
docker compose logs -f

# 特定サービスのログだけ確認
docker compose logs -f app

# コンテナを停止（データは残る）
docker compose down

# コンテナ + ボリューム（DB データ）をすべて削除
docker compose down -v
```

---

## 6. よく使うコマンド一覧

### コンテナ操作

```bash
# 起動中のコンテナ一覧
docker ps

# 全コンテナ一覧（停止中も含む）
docker ps -a

# コンテナの中に入る（シェルを起動）
docker compose exec app sh        # Alpine 系は sh
docker compose exec app bash      # Ubuntu 系は bash

# コンテナ内でコマンドを実行
docker compose exec app npm run migrate
docker compose exec db psql -U postgres -d nextapp
```

### イメージ操作

```bash
# ローカルのイメージ一覧
docker images

# イメージを削除
docker rmi イメージID

# 使っていないイメージ・コンテナをまとめて削除
docker system prune
```

### ビルド

```bash
# イメージを再ビルドして起動
docker compose up -d --build

# キャッシュを使わずにビルド
docker compose build --no-cache
```

---

## 7. このリポジトリでの使い方

### テンプレート別の起動方法

#### Next.js（`next/`）

```bash
cd next

# 環境変数ファイルを作成
cp .env.example .env

# コンテナを起動
docker compose up -d

# DB マイグレーションを実行
docker compose exec app npx prisma migrate dev

# ブラウザで確認
# → http://localhost:3000
```

#### Next.js + Go（`next-go/`）

```bash
cd next-go
docker compose up -d
# Next.js → http://localhost:3000
# Go API  → http://localhost:8080
```

#### Next.js + FastAPI（`next-python/`）

```bash
cd next-python
docker compose up -d
# Next.js → http://localhost:3000
# FastAPI → http://localhost:8000/docs
```

### 環境変数の管理

```bash
# .env.example をコピーして .env を作成（Git 管理外）
cp .env.example .env

# .env ファイルを編集
# DATABASE_URL=postgresql://...
# NEXT_PUBLIC_SUPABASE_URL=https://...
```

> ⚠️ `.env` ファイルは **絶対に Git にコミットしない**こと。`.gitignore` に含まれていることを確認してください。

---

## 8. トラブルシューティング

### ポートが使用中

```
Error: bind: address already in use
```

```bash
# 使用中のポートを確認（Windows PowerShell）
netstat -ano | findstr :3000

# プロセスを終了
taskkill /PID <PID番号> /F

# または docker-compose.yml のポートを変更
ports:
  - "3001:3000"  # ホスト側を 3001 に変更
```

### コンテナが起動しない

```bash
# エラーログを確認
docker compose logs app

# コンテナを再ビルド
docker compose up -d --build
```

### DB に接続できない

```bash
# DB コンテナが起動しているか確認
docker compose ps

# DB に直接接続して確認
docker compose exec db psql -U postgres -d nextapp -c "\dt"

# 環境変数の確認
docker compose exec app env | grep DATABASE_URL
```

### ボリュームのリセット（DB を初期化したい）

```bash
# コンテナとボリュームを削除
docker compose down -v

# 再起動（DB は空の状態から）
docker compose up -d
```

---

## 📌 まとめ

| 概念 | 一言説明 |
|------|---------|
| **Image** | アプリの設計図 |
| **Container** | イメージから動いているプロセス |
| **Dockerfile** | イメージの作り方を定義するファイル |
| **docker-compose** | 複数コンテナをまとめて管理する設定ファイル |
| **Volume** | データを永続化する仕組み |

```bash
# 基本の流れ
docker compose up -d    # 起動
docker compose logs -f  # ログ確認
docker compose exec app sh  # コンテナに入る
docker compose down     # 停止
```
