import { Hono } from 'hono';
import usersRoutes from './users';
import postsRoutes from './posts';

const api = new Hono();

// サブルート
api.route('/users', usersRoutes);
api.route('/posts', postsRoutes);

// APIルートのルート
api.get('/', (c) => {
  return c.json({
    message: 'API Routes',
    version: 'v1',
    routes: {
      users: '/api/users',
      posts: '/api/posts',
    },
  });
});

export default api;
