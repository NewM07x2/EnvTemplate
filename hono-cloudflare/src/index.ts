import { Hono } from 'hono';
import { cors } from 'hono/cors';
import { logger } from 'hono/logger';
import { prettyJSON } from 'hono/pretty-json';
import apiRoutes from './routes/api';
import { errorHandler } from './middleware/errorHandler';

type Bindings = {
  ENVIRONMENT: string;
  // KV, D1, R2などのバインディングをここに追加
  // MY_KV: KVNamespace;
  // DB: D1Database;
  // MY_BUCKET: R2Bucket;
};

const app = new Hono<{ Bindings: Bindings }>();

// ミドルウェア
app.use('*', logger());
app.use('*', prettyJSON());
app.use('*', cors());

// エラーハンドリング
app.onError(errorHandler);

// ルート
app.get('/', (c) => {
  return c.json({
    message: '🚀 Hono + Cloudflare Workers API',
    version: '0.1.0',
    environment: c.env.ENVIRONMENT,
    endpoints: {
      api: '/api',
      health: '/health',
      users: '/api/users',
    },
  });
});

app.get('/health', (c) => {
  return c.json({
    status: 'ok',
    timestamp: new Date().toISOString(),
    uptime: performance.now(),
  });
});

// APIルート
app.route('/api', apiRoutes);

export default app;
