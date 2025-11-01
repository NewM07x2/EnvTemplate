import Link from 'next/link';
import { Suspense } from 'react';
import { getPosts, BlogPost } from '@/lib/api';

const PostsList = ({ posts }: { posts: BlogPost[] }) => {
  return (
    <ul className="overflow-y-auto max-h-[calc(100vh-200px)] space-y-2 pr-2">
      {posts.map((post) => (
        <li key={post.id} className="hover:bg-gray-100">
          {post.id} : {post.title}
        </li>
      ))}
    </ul>
  );
};

export default async function BlogPage() {
  const posts = await getPosts();

  return (
    <div className="flex flex-col h-full max-h-[calc(100vh-100px)]">
      <h1 className="text-4xl my-4 flex-shrink-0">Blog Page</h1>
      <div className="flex-1 overflow-hidden">
        <Suspense fallback={<p>Loading posts...</p>}>
          <PostsList posts={posts} />
        </Suspense>
      </div>
      <Link href="/" className="text-blue-500 hover:underline mx-4 my-2 text-center inline-block flex-shrink-0">Home</Link>
    </div>
  );
}