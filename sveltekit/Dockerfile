FROM node:22-alpine

WORKDIR /app

# Prismaのために必要
RUN apk add --no-cache openssl

# package.jsonとpackage-lock.jsonをコピー
COPY package*.json ./

# 依存関係のインストール
RUN npm ci

# アプリケーションコードをコピー
COPY . .

# Prismaクライアントを生成
RUN npx prisma generate

# ポート公開
EXPOSE 5173

# 開発サーバーを起動
CMD ["npm", "run", "dev", "--", "--host"]
