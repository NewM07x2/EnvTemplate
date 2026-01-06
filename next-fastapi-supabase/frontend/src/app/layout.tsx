import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'Next.js + FastAPI + Supabase',
  description: 'Full-stack application with Supabase authentication',
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="ja">
      <body className="antialiased bg-gray-50">
        <nav className="bg-supabase-green text-white shadow-lg">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between h-16 items-center">
              <div className="flex space-x-8">
                <a href="/" className="font-bold text-xl hover:text-gray-200">
                  Next + FastAPI + Supabase
                </a>
                <a href="/users" className="hover:text-gray-200">
                  Users
                </a>
                <a href="/posts" className="hover:text-gray-200">
                  Posts
                </a>
                <a href="/about" className="hover:text-gray-200">
                  About
                </a>
              </div>
              <div className="flex space-x-4">
                <a
                  href="/login"
                  className="px-4 py-2 rounded hover:bg-green-600"
                >
                  Login
                </a>
                <a
                  href="/register"
                  className="px-4 py-2 bg-white text-supabase-green rounded hover:bg-gray-100"
                >
                  Register
                </a>
              </div>
            </div>
          </div>
        </nav>
        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {children}
        </main>
        <footer className="bg-gray-800 text-white mt-12">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 text-center">
            <p>&copy; 2026 Next.js + FastAPI + Supabase Template</p>
          </div>
        </footer>
      </body>
    </html>
  );
}
