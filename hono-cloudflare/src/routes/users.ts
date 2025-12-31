import { Hono } from 'hono';
import { z } from 'hono/validator';

const users = new Hono();

// インメモリストレージ (本番ではKV/D1を使用)
const mockUsers = [
  { id: '1', name: 'Alice', email: 'alice@example.com', createdAt: new Date().toISOString() },
  { id: '2', name: 'Bob', email: 'bob@example.com', createdAt: new Date().toISOString() },
  { id: '3', name: 'Charlie', email: 'charlie@example.com', createdAt: new Date().toISOString() },
];

// GET /api/users - 全ユーザー取得
users.get('/', (c) => {
  return c.json({
    users: mockUsers,
    count: mockUsers.length,
  });
});

// GET /api/users/:id - 特定ユーザー取得
users.get('/:id', (c) => {
  const id = c.req.param('id');
  const user = mockUsers.find((u) => u.id === id);

  if (!user) {
    return c.json({ error: 'User not found' }, 404);
  }

  return c.json({ user });
});

// POST /api/users - ユーザー作成
users.post('/', async (c) => {
  try {
    const body = await c.req.json();
    
    // 簡易バリデーション
    if (!body.name || !body.email) {
      return c.json({ error: 'Name and email are required' }, 400);
    }

    const newUser = {
      id: String(mockUsers.length + 1),
      name: body.name,
      email: body.email,
      createdAt: new Date().toISOString(),
    };

    mockUsers.push(newUser);

    return c.json({ user: newUser }, 201);
  } catch (error) {
    return c.json({ error: 'Invalid JSON' }, 400);
  }
});

// PUT /api/users/:id - ユーザー更新
users.put('/:id', async (c) => {
  const id = c.req.param('id');
  const userIndex = mockUsers.findIndex((u) => u.id === id);

  if (userIndex === -1) {
    return c.json({ error: 'User not found' }, 404);
  }

  try {
    const body = await c.req.json();
    
    mockUsers[userIndex] = {
      ...mockUsers[userIndex],
      ...body,
      id, // IDは変更不可
    };

    return c.json({ user: mockUsers[userIndex] });
  } catch (error) {
    return c.json({ error: 'Invalid JSON' }, 400);
  }
});

// DELETE /api/users/:id - ユーザー削除
users.delete('/:id', (c) => {
  const id = c.req.param('id');
  const userIndex = mockUsers.findIndex((u) => u.id === id);

  if (userIndex === -1) {
    return c.json({ error: 'User not found' }, 404);
  }

  const deletedUser = mockUsers.splice(userIndex, 1)[0];

  return c.json({ message: 'User deleted', user: deletedUser });
});

export default users;
