# Vercel Analytics・Monitoring・Logging 統合

> **対象者**: 本番環境の可視化・監視・デバッグが必要な開発者  
> **主要トピック**: Vercel Analytics / Web Vitals / APM / ログ集約 / エラートラッキング / ダッシュボード

---

## 📚 目次

1. [Vercel Analytics](#1-vercel-analytics)
2. [Web Vitals 監視](#2-web-vitals-監視)
3. [Application Performance Monitoring (APM)](#3-application-performance-monitoring-apm)
4. [構造化ログ](#4-構造化ログ)
5. [エラートラッキング](#5-エラートラッキング)
6. [カスタムメトリクス](#6-カスタムメトリクス)
7. [ダッシュボード・アラート](#7-ダッシュボードアラート)
8. [本番環境デバッグ](#8-本番環境デバッグ)

---

## 1. Vercel Analytics

### 1.1 基本セットアップ

```bash
npm install @vercel/analytics @vercel/web-vitals
```

```typescript
// app/layout.tsx (Next.js 13+)
import { Analytics } from '@vercel/analytics/react';
import { SpeedInsights } from '@vercel/speed-insights/react';

export default function RootLayout({ children }) {
  return (
    <html>
      <body>
        {children}
        <Analytics />
        <SpeedInsights />
      </body>
    </html>
  );
}
```

### 1.2 カスタムイベント追跡

```typescript
// lib/analytics.ts
import { track } from '@vercel/analytics';

// ページビュー
export function trackPageView(path: string) {
  track('pageView', { path });
}

// ユーザーアクション
export function trackUserAction(action: string, properties?: any) {
  track(action, properties || {});
}

// コンバージョン
export function trackConversion(type: string, value: number) {
  track('conversion', { type, value });
}

// エラー
export function trackError(error: Error, context?: any) {
  track('error', {
    message: error.message,
    stack: error.stack,
    context: JSON.stringify(context),
  });
}

// 使用例
export function trackButtonClick(buttonName: string) {
  track('button_click', {
    button: buttonName,
    timestamp: new Date().toISOString(),
  });
}
```

### 1.3 ユーザー識別

```typescript
// lib/user-tracking.ts
import { setUser, identify } from '@vercel/analytics';

export function identifyUser(userId: string, properties?: any) {
  // ユーザー ID を設定
  setUser(userId);

  // 追加属性を記録
  identify(userId, {
    email: properties?.email,
    plan: properties?.plan,
    createdAt: properties?.createdAt,
  });
}

export function unidentifyUser() {
  setUser('');
}
```

---

## 2. Web Vitals 監視

### 2.1 Core Web Vitals 測定

```typescript
// lib/web-vitals.ts
import { getCLS, getFCP, getFID, getLCP, getTTFB } from 'web-vitals';

export function observeWebVitals() {
  // Cumulative Layout Shift
  getCLS((metric) => {
    console.log('CLS:', metric.value);
    sendMetricToAnalytics('CLS', metric.value);
  });

  // First Contentful Paint
  getFCP((metric) => {
    console.log('FCP:', metric.value);
    sendMetricToAnalytics('FCP', metric.value);
  });

  // First Input Delay
  getFID((metric) => {
    console.log('FID:', metric.value);
    sendMetricToAnalytics('FID', metric.value);
  });

  // Largest Contentful Paint
  getLCP((metric) => {
    console.log('LCP:', metric.value);
    sendMetricToAnalytics('LCP', metric.value);
  });

  // Time to First Byte
  getTTFB((metric) => {
    console.log('TTFB:', metric.value);
    sendMetricToAnalytics('TTFB', metric.value);
  });
}

function sendMetricToAnalytics(name: string, value: number) {
  const threshold = {
    CLS: 0.1,
    FCP: 1800,
    FID: 100,
    LCP: 2500,
    TTFB: 600,
  };

  const isGood = value <= threshold[name as keyof typeof threshold];

  // ログ送信
  fetch('/api/metrics', {
    method: 'POST',
    body: JSON.stringify({
      metric: name,
      value,
      status: isGood ? 'good' : 'poor',
      timestamp: new Date().toISOString(),
    }),
  }).catch(() => {
    // ネットワークエラーでも無視
  });
}
```

### 2.2 カスタムパフォーマンス計測

```typescript
// lib/performance.ts
export class PerformanceMonitor {
  private marks: Map<string, number> = new Map();

  start(label: string) {
    this.marks.set(label, performance.now());
  }

  end(label: string) {
    const start = this.marks.get(label);
    if (!start) {
      console.warn(`No start mark for ${label}`);
      return 0;
    }

    const duration = performance.now() - start;
    this.marks.delete(label);

    console.log(`${label}: ${duration.toFixed(2)}ms`);

    return duration;
  }

  async measure<T>(
    label: string,
    fn: () => Promise<T>
  ): Promise<T> {
    this.start(label);
    const result = await fn();
    this.end(label);
    return result;
  }
}

// 使用例
const monitor = new PerformanceMonitor();

export async function fetchDataWithMetrics() {
  return monitor.measure('fetch-data', async () => {
    return await fetch('/api/data').then((r) => r.json());
  });
}
```

---

## 3. Application Performance Monitoring (APM)

### 3.1 Datadog 統合

```bash
npm install @datadog/browser-rum @datadog/browser-logs
```

```typescript
// lib/datadog.ts
import { datadogRum } from '@datadog/browser-rum';
import { datadogLogs } from '@datadog/browser-logs';

export function initializeDatadog() {
  datadogRum.init({
    applicationId: process.env.NEXT_PUBLIC_DATADOG_APP_ID!,
    clientToken: process.env.NEXT_PUBLIC_DATADOG_CLIENT_TOKEN!,
    site: 'datadoghq.com',
    service: 'my-app',
    env: process.env.NODE_ENV,
    version: process.env.NEXT_PUBLIC_APP_VERSION,
    sessionSampleRate: 100,
    sessionReplaySampleRate: 20,
    trackUserInteractions: true,
    trackResources: true,
    trackLongTasks: true,
    defaultPrivacyLevel: 'mask-user-input',
  });

  datadogRum.startSessionReplayRecording();

  datadogLogs.init({
    applicationId: process.env.NEXT_PUBLIC_DATADOG_APP_ID!,
    clientToken: process.env.NEXT_PUBLIC_DATADOG_CLIENT_TOKEN!,
    site: 'datadoghq.com',
    service: 'my-app',
    env: process.env.NODE_ENV,
    sessionSampleRate: 100,
    forwardErrorsToLogs: true,
  });

  datadogLogs.logger.info('Datadog initialized');
}

// ユーザー情報設定
export function setDatadogUser(userId: string, userData?: any) {
  datadogRum.setUser({
    id: userId,
    name: userData?.name,
    email: userData?.email,
  });
}
```

### 3.2 New Relic 統合

```bash
npm install @newrelic/browser-agent
```

```typescript
// lib/new-relic.ts
import * as newrelic from '@newrelic/browser-agent';

export function initializeNewRelic() {
  newrelic.init({
    accountID: process.env.NEXT_PUBLIC_NEW_RELIC_ACCOUNT_ID,
    trustKey: process.env.NEXT_PUBLIC_NEW_RELIC_TRUST_KEY,
    agentID: process.env.NEXT_PUBLIC_NEW_RELIC_AGENT_ID,
    licenseKey: process.env.NEXT_PUBLIC_NEW_RELIC_LICENSE_KEY,
    applicationID: process.env.NEXT_PUBLIC_NEW_RELIC_APP_ID,
    beacon: 'bam.nr-data.net',
    errorBeacon: 'bam.nr-data.net',
  });

  newrelic.noticeError(new Error('Test error'));
}

// カスタムメトリクス
export function recordCustomMetric(name: string, value: number) {
  newrelic.addPageAction(name, { value });
}
```

### 3.3 Sentry 統合

```bash
npm install @sentry/nextjs
```

```typescript
// lib/sentry.ts
import * as Sentry from '@sentry/nextjs';

export function initializeSentry() {
  Sentry.init({
    dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,
    environment: process.env.NODE_ENV,
    release: process.env.NEXT_PUBLIC_APP_VERSION,
    tracesSampleRate: 1.0,
    replaysSessionSampleRate: 0.1,
    replaysOnErrorSampleRate: 1.0,
    integrations: [
      new Sentry.Replay({
        maskAllText: false,
        blockAllMedia: false,
      }),
    ],
  });
}

// ユーザー設定
export function setSentryUser(userId: string, email?: string) {
  Sentry.setUser({
    id: userId,
    email,
  });
}

// エラー報告
export function captureException(error: Error, context?: any) {
  Sentry.captureException(error, {
    contexts: { custom: context },
  });
}
```

---

## 4. 構造化ログ

### 4.1 ログユーティリティ

```typescript
// lib/logger.ts
type LogLevel = 'debug' | 'info' | 'warn' | 'error';

interface LogEntry {
  timestamp: string;
  level: LogLevel;
  message: string;
  context?: any;
  userId?: string;
  requestId?: string;
}

class Logger {
  private isDev = process.env.NODE_ENV === 'development';

  private log(level: LogLevel, message: string, context?: any) {
    const entry: LogEntry = {
      timestamp: new Date().toISOString(),
      level,
      message,
      context,
    };

    const logString = JSON.stringify(entry);

    switch (level) {
      case 'debug':
        console.debug(logString);
        break;
      case 'info':
        console.info(logString);
        break;
      case 'warn':
        console.warn(logString);
        break;
      case 'error':
        console.error(logString);
        break;
    }

    // 本番環境ではリモートログサービスに送信
    if (!this.isDev && level !== 'debug') {
      this.sendToRemote(entry);
    }
  }

  debug(message: string, context?: any) {
    this.log('debug', message, context);
  }

  info(message: string, context?: any) {
    this.log('info', message, context);
  }

  warn(message: string, context?: any) {
    this.log('warn', message, context);
  }

  error(message: string, context?: any) {
    this.log('error', message, context);
  }

  private async sendToRemote(entry: LogEntry) {
    try {
      await fetch('/api/logs', {
        method: 'POST',
        body: JSON.stringify(entry),
      });
    } catch (error) {
      // ログ送信失敗時は無視
    }
  }
}

export const logger = new Logger();
```

### 4.2 API ルートでのログ

```typescript
// app/api/logs/route.ts
import { logger } from '@/lib/logger';
import { NextRequest, NextResponse } from 'next/server';

export async function POST(req: NextRequest) {
  const logEntry = await req.json();

  logger.info('Remote log received', {
    level: logEntry.level,
    message: logEntry.message,
  });

  // ログをサービスに送信
  try {
    await fetch('https://logs.example.com/api/logs', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${process.env.LOGGING_API_KEY}`,
      },
      body: JSON.stringify(logEntry),
    });
  } catch (error) {
    console.error('Failed to send logs to service', error);
  }

  return NextResponse.json({ success: true });
}
```

### 4.3 コンテキスト付きロギング

```typescript
// lib/context-logger.ts
import { logger } from './logger';

export class ContextLogger {
  constructor(private context: Record<string, any>) {}

  debug(message: string, extra?: any) {
    logger.debug(message, { ...this.context, ...extra });
  }

  info(message: string, extra?: any) {
    logger.info(message, { ...this.context, ...extra });
  }

  warn(message: string, extra?: any) {
    logger.warn(message, { ...this.context, ...extra });
  }

  error(message: string, extra?: any) {
    logger.error(message, { ...this.context, ...extra });
  }
}

// API ルートで使用
export async function handleRequest(req: NextRequest) {
  const requestId = crypto.randomUUID();
  const log = new ContextLogger({ requestId, method: req.method });

  log.info('Request started', { path: req.nextUrl.pathname });

  try {
    // ビジネスロジック
    log.info('Request completed');
  } catch (error) {
    log.error('Request failed', { error });
    throw error;
  }
}
```

---

## 5. エラートラッキング

### 5.1 グローバルエラーハンドラー

```typescript
// lib/error-handler.ts
import { logger } from './logger';

export function captureError(error: Error, context?: any) {
  logger.error(error.message, {
    stack: error.stack,
    name: error.name,
    ...context,
  });

  // 外部サービスに送信（Sentry/Datadog等）
  if (typeof window !== 'undefined') {
    // クライアント側
    sendToErrorTrackingService(error, context);
  }
}

async function sendToErrorTrackingService(error: Error, context?: any) {
  try {
    await fetch('/api/errors', {
      method: 'POST',
      body: JSON.stringify({
        message: error.message,
        stack: error.stack,
        url: window.location.href,
        userAgent: navigator.userAgent,
        context,
        timestamp: new Date().toISOString(),
      }),
    });
  } catch (e) {
    // 送信失敗時は無視
  }
}

// グローバル例外ハンドラー
if (typeof window !== 'undefined') {
  window.addEventListener('error', (event) => {
    captureError(event.error, {
      type: 'uncaughtException',
      filename: event.filename,
      lineno: event.lineno,
      colno: event.colno,
    });
  });

  window.addEventListener('unhandledrejection', (event) => {
    captureError(
      event.reason instanceof Error
        ? event.reason
        : new Error(String(event.reason)),
      {
        type: 'unhandledRejection',
      }
    );
  });
}
```

### 5.2 API エラー追跡

```typescript
// middleware.ts
import { logger } from '@/lib/logger';
import { NextRequest, NextResponse } from 'next/server';

export function middleware(request: NextRequest) {
  const requestId = request.headers.get('x-request-id') || crypto.randomUUID();

  const response = NextResponse.next();
  response.headers.set('x-request-id', requestId);

  return response;
}

// app/api/[...route]/route.ts
export async function GET(req: NextRequest) {
  const requestId = req.headers.get('x-request-id');

  try {
    // 処理
    return NextResponse.json({ success: true });
  } catch (error) {
    logger.error('API Error', {
      requestId,
      path: req.nextUrl.pathname,
      error: error instanceof Error ? error.message : String(error),
    });

    return NextResponse.json(
      { error: 'Internal Server Error' },
      { status: 500 }
    );
  }
}
```

---

## 6. カスタムメトリクス

### 6.1 ビジネスメトリクス

```typescript
// lib/business-metrics.ts
import { track } from '@vercel/analytics';
import { logger } from './logger';

export class BusinessMetrics {
  static recordSale(amount: number, productId: string, userId: string) {
    track('sale', {
      amount,
      productId,
      userId,
      timestamp: new Date().toISOString(),
    });

    logger.info('Sale recorded', {
      amount,
      productId,
      userId,
    });
  }

  static recordSignup(userId: string, plan: string) {
    track('signup', {
      userId,
      plan,
      timestamp: new Date().toISOString(),
    });

    logger.info('User signup', { userId, plan });
  }

  static recordActiveUser(userId: string) {
    track('active_user', {
      userId,
      timestamp: new Date().toISOString(),
    });
  }

  static recordChurn(userId: string, reason?: string) {
    track('churn', {
      userId,
      reason,
      timestamp: new Date().toISOString(),
    });

    logger.warn('User churn', { userId, reason });
  }
}

// 使用例
export function trackPurchase(amount: number, productId: string) {
  BusinessMetrics.recordSale(amount, productId, userId);
}
```

### 6.2 技術メトリクス

```typescript
// lib/technical-metrics.ts
import { logger } from './logger';

export class TechnicalMetrics {
  static recordDatabaseQuery(query: string, duration: number) {
    logger.debug('DB Query', {
      query: query.substring(0, 100),
      duration: `${duration.toFixed(2)}ms`,
    });

    if (duration > 1000) {
      logger.warn('Slow database query', {
        query: query.substring(0, 100),
        duration: `${duration.toFixed(2)}ms`,
      });
    }
  }

  static recordCacheHit(key: string) {
    logger.debug('Cache hit', { key });
  }

  static recordCacheMiss(key: string) {
    logger.debug('Cache miss', { key });
  }

  static recordExternalAPICall(service: string, duration: number, status: number) {
    logger.debug('External API call', {
      service,
      duration: `${duration.toFixed(2)}ms`,
      status,
    });

    if (duration > 5000 || status >= 400) {
      logger.warn('Slow/failed external API call', {
        service,
        duration: `${duration.toFixed(2)}ms`,
        status,
      });
    }
  }
}
```

---

## 7. ダッシュボード・アラート

### 7.1 メトリクス API

```typescript
// app/api/metrics/dashboard/route.ts
import { sql } from '@vercel/postgres';
import { NextResponse } from 'next/server';

export async function GET() {
  try {
    // アクセス数（過去24時間）
    const pageviews = await sql`
      SELECT COUNT(*) as count FROM analytics
      WHERE created_at > NOW() - INTERVAL '24 hours'
      AND event_type = 'pageview';
    `;

    // ユーザー数
    const users = await sql`
      SELECT COUNT(DISTINCT user_id) as count FROM analytics
      WHERE created_at > NOW() - INTERVAL '24 hours';
    `;

    // エラー数
    const errors = await sql`
      SELECT COUNT(*) as count FROM error_logs
      WHERE created_at > NOW() - INTERVAL '24 hours';
    `;

    // 平均応答時間
    const avgResponseTime = await sql`
      SELECT AVG(duration) as avg_ms FROM api_metrics
      WHERE created_at > NOW() - INTERVAL '24 hours';
    `;

    return NextResponse.json({
      pageviews: pageviews.rows[0].count,
      users: users.rows[0].count,
      errors: errors.rows[0].count,
      avgResponseTime: avgResponseTime.rows[0].avg_ms,
      timestamp: new Date().toISOString(),
    });
  } catch (error) {
    return NextResponse.json(
      { error: 'Failed to fetch metrics' },
      { status: 500 }
    );
  }
}
```

### 7.2 アラート設定

```typescript
// lib/alerts.ts
export interface Alert {
  id: string;
  name: string;
  metric: string;
  threshold: number;
  operator: '>' | '<' | '==' | '!=' | '>=' | '<=';
  duration: number; // 秒
  notificationChannels: string[];
}

export const ALERTS: Alert[] = [
  {
    id: 'error-rate-high',
    name: 'High Error Rate',
    metric: 'error_count',
    threshold: 10,
    operator: '>',
    duration: 300, // 5分以上
    notificationChannels: ['slack', 'email'],
  },
  {
    id: 'response-time-slow',
    name: 'Slow Response Time',
    metric: 'avg_response_time',
    threshold: 5000,
    operator: '>',
    duration: 600, // 10分以上
    notificationChannels: ['slack', 'pagerduty'],
  },
  {
    id: 'db-connection-pool-exhausted',
    name: 'DB Connection Pool Exhausted',
    metric: 'db_connections_in_use',
    threshold: 95,
    operator: '>=',
    duration: 60,
    notificationChannels: ['slack', 'email', 'pagerduty'],
  },
];

// アラート発火関数
export async function checkAlerts() {
  for (const alert of ALERTS) {
    const currentValue = await getMetricValue(alert.metric);

    if (shouldTriggerAlert(currentValue, alert)) {
      await notifyChannels(alert);
    }
  }
}

async function notifyChannels(alert: Alert) {
  for (const channel of alert.notificationChannels) {
    switch (channel) {
      case 'slack':
        await notifySlack(alert);
        break;
      case 'email':
        await notifyEmail(alert);
        break;
      case 'pagerduty':
        await notifyPagerDuty(alert);
        break;
    }
  }
}
```

---

## 8. 本番環境デバッグ

### 8.1 リモートロギング

```typescript
// lib/remote-debugger.ts
export class RemoteDebugger {
  static async captureState(context: string) {
    const state = {
      context,
      timestamp: new Date().toISOString(),
      url: typeof window !== 'undefined' ? window.location.href : null,
      memory: performance.memory ? {
        usedJSHeapSize: performance.memory.usedJSHeapSize,
        totalJSHeapSize: performance.memory.totalJSHeapSize,
      } : null,
    };

    await fetch('/api/debug/capture', {
      method: 'POST',
      body: JSON.stringify(state),
    });
  }

  static async captureScreenshot() {
    if (typeof window === 'undefined') return;

    const canvas = await html2canvas(document.body);
    const blob = await new Promise<Blob>((resolve) => {
      canvas.toBlob((b) => resolve(b!));
    });

    const formData = new FormData();
    formData.append('screenshot', blob, 'screenshot.png');

    await fetch('/api/debug/screenshot', {
      method: 'POST',
      body: formData,
    });
  }
}

// 使用例
export function debugMode() {
  if (process.env.DEBUG === 'true') {
    RemoteDebugger.captureState('User interaction detected');
  }
}
```

### 8.2 セッションリプレイ

```typescript
// lib/session-replay.ts
export function enableSessionReplay() {
  if (process.env.NEXT_PUBLIC_SESSION_REPLAY === 'true') {
    // Sentry の Session Replay が自動的に有効
    // または別サービス（Logrocket, FullStory等）を初期化
  }
}

// ユーザーが明示的にオプトイン
export async function optInSessionReplay(userId: string) {
  await fetch('/api/session-replay/opt-in', {
    method: 'POST',
    body: JSON.stringify({ userId }),
  });
}
```

---

## 📖 関連ドキュメント

- [06_パフォーマンス最適化.md](./06_パフォーマンス最適化.md) — Core Web Vitals 基礎
- [08_運用方法.md](./08_運用方法.md) — 監視・セットアップ
