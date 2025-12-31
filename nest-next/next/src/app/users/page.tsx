'use client';

import { useQuery } from '@apollo/client';
import { GET_USERS } from '@/lib/graphql/queries';
import Link from 'next/link';

interface User {
  id: string;
  email: string;
  username: string;
  createdAt: string;
  posts: Array<{
    id: string;
    title: string;
    published: boolean;
  }>;
}

export default function UsersPage() {
  const { data, loading, error } = useQuery<{ users: User[] }>(GET_USERS);

  if (loading) {
    return (
      <div className="min-h-screen p-8 flex items-center justify-center">
        <div className="text-xl">読み込み中...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen p-8 flex items-center justify-center">
        <div className="text-xl text-red-600">
          エラー: {error.message}
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen p-8">
      <div className="max-w-6xl mx-auto">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold">ユーザー一覧</h1>
          <Link
            href="/"
            className="px-4 py-2 bg-gray-500 text-white rounded hover:bg-gray-600"
          >
            ホームに戻る
          </Link>
        </div>

        {data?.users && data.users.length === 0 ? (
          <p className="text-gray-600">ユーザーが登録されていません。</p>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {data?.users.map((user) => (
              <div
                key={user.id}
                className="p-6 border rounded-lg bg-white shadow-sm hover:shadow-md transition"
              >
                <h2 className="text-xl font-bold mb-2">{user.username}</h2>
                <p className="text-sm text-gray-600 mb-2">{user.email}</p>
                <p className="text-xs text-gray-500 mb-4">
                  登録日: {new Date(user.createdAt).toLocaleDateString('ja-JP')}
                </p>
                
                {user.posts && user.posts.length > 0 && (
                  <div className="mt-4">
                    <p className="text-sm font-semibold mb-2">
                      投稿 ({user.posts.length})
                    </p>
                    <ul className="text-sm text-gray-600 space-y-1">
                      {user.posts.slice(0, 3).map((post) => (
                        <li key={post.id} className="truncate">
                          • {post.title}
                          {post.published && (
                            <span className="ml-2 text-green-600">公開中</span>
                          )}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
