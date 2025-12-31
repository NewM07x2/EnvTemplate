import { Hono } from 'hono';

const posts = new Hono();

// インメモリストレージ
const mockPosts = [
  {
    id: '1',
    title: 'Introduction to Hono',
    content: 'Hono is a fast and lightweight web framework.',
    authorId: '1',
    published: true,
    createdAt: new Date().toISOString(),
  },
  {
    id: '2',
    title: 'Cloudflare Workers Guide',
    content: 'Deploy your apps to the edge with Cloudflare Workers.',
    authorId: '2',
    published: true,
    createdAt: new Date().toISOString(),
  },
];

// GET /api/posts - 全投稿取得
posts.get('/', (c) => {
  const published = c.req.query('published');
  
  let filteredPosts = mockPosts;
  if (published !== undefined) {
    const isPublished = published === 'true';
    filteredPosts = mockPosts.filter((p) => p.published === isPublished);
  }

  return c.json({
    posts: filteredPosts,
    count: filteredPosts.length,
  });
});

// GET /api/posts/:id - 特定投稿取得
posts.get('/:id', (c) => {
  const id = c.req.param('id');
  const post = mockPosts.find((p) => p.id === id);

  if (!post) {
    return c.json({ error: 'Post not found' }, 404);
  }

  return c.json({ post });
});

// POST /api/posts - 投稿作成
posts.post('/', async (c) => {
  try {
    const body = await c.req.json();
    
    if (!body.title || !body.authorId) {
      return c.json({ error: 'Title and authorId are required' }, 400);
    }

    const newPost = {
      id: String(mockPosts.length + 1),
      title: body.title,
      content: body.content || '',
      authorId: body.authorId,
      published: body.published || false,
      createdAt: new Date().toISOString(),
    };

    mockPosts.push(newPost);

    return c.json({ post: newPost }, 201);
  } catch (error) {
    return c.json({ error: 'Invalid JSON' }, 400);
  }
});

export default posts;
