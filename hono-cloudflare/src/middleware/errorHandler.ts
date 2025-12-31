import { ErrorHandler } from 'hono';

export const errorHandler: ErrorHandler = (err, c) => {
  console.error('Error:', err);

  // エラーの種類に応じてレスポンスを返す
  if (err.message.includes('Not Found')) {
    return c.json({ error: 'Not Found' }, 404);
  }

  if (err.message.includes('Unauthorized')) {
    return c.json({ error: 'Unauthorized' }, 401);
  }

  if (err.message.includes('Forbidden')) {
    return c.json({ error: 'Forbidden' }, 403);
  }

  // デフォルトは500エラー
  return c.json(
    {
      error: 'Internal Server Error',
      message: err.message,
    },
    500
  );
};
