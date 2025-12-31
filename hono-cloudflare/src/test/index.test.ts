import { describe, it, expect } from 'vitest';
import app from '../index';

describe('Hono API Tests', () => {
  it('should return welcome message', async () => {
    const res = await app.request('/');
    expect(res.status).toBe(200);
    
    const data = await res.json();
    expect(data.message).toContain('Hono + Cloudflare Workers');
  });

  it('should return health status', async () => {
    const res = await app.request('/health');
    expect(res.status).toBe(200);
    
    const data = await res.json();
    expect(data.status).toBe('ok');
    expect(data.timestamp).toBeDefined();
  });

  it('should return 404 for unknown route', async () => {
    const res = await app.request('/unknown');
    expect(res.status).toBe(404);
  });
});

describe('Users API Tests', () => {
  it('should get all users', async () => {
    const res = await app.request('/api/users');
    expect(res.status).toBe(200);
    
    const data = await res.json();
    expect(data.users).toBeInstanceOf(Array);
    expect(data.count).toBeGreaterThan(0);
  });

  it('should get user by id', async () => {
    const res = await app.request('/api/users/1');
    expect(res.status).toBe(200);
    
    const data = await res.json();
    expect(data.user.id).toBe('1');
    expect(data.user.name).toBeDefined();
  });

  it('should return 404 for non-existent user', async () => {
    const res = await app.request('/api/users/999');
    expect(res.status).toBe(404);
  });

  it('should create new user', async () => {
    const res = await app.request('/api/users', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        name: 'Test User',
        email: 'test@example.com',
      }),
    });
    
    expect(res.status).toBe(201);
    const data = await res.json();
    expect(data.user.name).toBe('Test User');
    expect(data.user.email).toBe('test@example.com');
  });
});

describe('Posts API Tests', () => {
  it('should get all posts', async () => {
    const res = await app.request('/api/posts');
    expect(res.status).toBe(200);
    
    const data = await res.json();
    expect(data.posts).toBeInstanceOf(Array);
  });

  it('should filter published posts', async () => {
    const res = await app.request('/api/posts?published=true');
    expect(res.status).toBe(200);
    
    const data = await res.json();
    expect(data.posts.every((p: any) => p.published === true)).toBe(true);
  });

  it('should get post by id', async () => {
    const res = await app.request('/api/posts/1');
    expect(res.status).toBe(200);
    
    const data = await res.json();
    expect(data.post.id).toBe('1');
  });
});
