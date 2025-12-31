import type { LoaderFunctionArgs, MetaFunction } from "@remix-run/node";
import { json } from "@remix-run/node";
import { useLoaderData } from "@remix-run/react";
import { prisma } from "~/lib/prisma.server";

export const meta: MetaFunction = () => {
  return [
    { title: "Users - Remix Template" },
    { name: "description", content: "User list with Prisma ORM" },
  ];
};

export const loader = async ({ request }: LoaderFunctionArgs) => {
  const users = await prisma.user.findMany({
    include: {
      posts: true,
    },
    orderBy: {
      createdAt: "desc",
    },
  });

  return json({ users });
};

export default function Users() {
  const { users } = useLoaderData<typeof loader>();

  return (
    <div className="users">
      <h1>👥 ユーザー一覧</h1>
      <p className="description">
        Prisma ORMを使用してPostgreSQLからデータを取得しています (SSR)
      </p>

      {users.length === 0 ? (
        <div className="empty">
          <p>ユーザーが登録されていません。</p>
          <p className="hint">データベースにサンプルデータを追加してください。</p>
        </div>
      ) : (
        <div className="grid">
          {users.map((user) => (
            <div key={user.id} className="user-card">
              <div className="user-header">
                <div className="avatar">
                  {user.username.charAt(0).toUpperCase()}
                </div>
                <div className="user-info">
                  <h3>{user.username}</h3>
                  <p className="email">{user.email}</p>
                </div>
              </div>
              <div className="user-meta">
                <p className="date">
                  登録日: {new Date(user.createdAt).toLocaleDateString("ja-JP")}
                </p>
                {user.posts.length > 0 && (
                  <p className="posts-count">投稿: {user.posts.length}件</p>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
