'use client';

import { useState, useEffect } from 'react';
import { postsApi } from '@/lib/api';

interface Post {
  id: string;
  title: string;
  content: string;
  published: boolean;
  author_id: string;
  created_at: string;
}

export default function PostsPage() {
  const [posts, setPosts] = useState<Post[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [filter, setFilter] = useState<'all' | 'published' | 'draft'>('all');

  useEffect(() => {
    fetchPosts();
  }, [filter]);

  const fetchPosts = async () => {
    try {
      setLoading(true);
      const published =
        filter === 'all' ? undefined : filter === 'published' ? true : false;
      const data = await postsApi.getPosts(published);
      setPosts(data);
    } catch (err: any) {
      setError(err.message || 'Failed to fetch posts');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="text-center py-12">
        <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-supabase-green"></div>
        <p className="mt-4 text-gray-600">Loading posts...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 rounded-lg p-6 text-center">
        <p className="text-red-800">Error: {error}</p>
        <button
          onClick={fetchPosts}
          className="mt-4 px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700"
        >
          Retry
        </button>
      </div>
    );
  }

  return (
    <div>
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold text-gray-900">📝 投稿一覧</h1>
        <div className="flex space-x-4">
          <select
            value={filter}
            onChange={(e) =>
              setFilter(e.target.value as 'all' | 'published' | 'draft')
            }
            className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-supabase-green focus:border-transparent"
          >
            <option value="all">すべて</option>
            <option value="published">公開済み</option>
            <option value="draft">下書き</option>
          </select>
        </div>
      </div>

      {posts.length === 0 ? (
        <div className="bg-gray-50 rounded-lg p-12 text-center">
          <p className="text-gray-600 text-lg">投稿がありません</p>
        </div>
      ) : (
        <div className="space-y-4">
          {posts.map((post) => (
            <div
              key={post.id}
              className="bg-white rounded-lg shadow-md p-6 hover:shadow-xl transition-shadow"
            >
              <div className="flex justify-between items-start mb-3">
                <h3 className="text-xl font-semibold text-gray-900">
                  {post.title}
                </h3>
                <span
                  className={`px-3 py-1 rounded-full text-sm font-medium ${
                    post.published
                      ? 'bg-green-100 text-green-800'
                      : 'bg-gray-100 text-gray-800'
                  }`}
                >
                  {post.published ? '公開' : '下書き'}
                </span>
              </div>
              {post.content && (
                <p className="text-gray-600 mb-4 line-clamp-3">
                  {post.content}
                </p>
              )}
              <div className="flex justify-between items-center text-sm text-gray-500">
                <span>
                  {new Date(post.created_at).toLocaleDateString('ja-JP')}
                </span>
                <span>作成者ID: {post.author_id.substring(0, 8)}...</span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
