import { useEffect, useState } from 'react'
import axios from 'axios'

interface User {
  id: number
  username: string
  email: string
}

function PrismaPage() {
  const [users, setUsers] = useState<User[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    // SSRの代わりにAPIエンドポイント経由でPrismaデータを取得
    const fetchUsers = async () => {
      try {
        const response = await axios.get('/api/users')
        setUsers(response.data)
      } catch (err) {
        setError('データの取得に失敗しました')
        console.error(err)
      } finally {
        setLoading(false)
      }
    }

    fetchUsers()
  }, [])

  if (loading) {
    return <div className="loading">読み込み中...</div>
  }

  if (error) {
    return (
      <div>
        <h1>Prisma (SSR相当) - API経由</h1>
        <div className="error">
          {error}
          <p style={{ marginTop: '1rem', fontSize: '0.9rem' }}>
            Prisma APIエンドポイントを実装する必要があります。
          </p>
        </div>
      </div>
    )
  }

  return (
    <div>
      <h1>Prisma (SSR相当) - API経由</h1>
      
      <div className="card">
        <h2>🗄️ Prismaを使用したデータ取得</h2>
        <p>
          このページでは、バックエンドAPI経由で<code>Prisma</code>を使用してPostgreSQLから
          データを取得します。Reactのみの環境では完全なSSRはできませんが、
          APIエンドポイント経由でサーバーサイドのデータアクセスを実現できます。
        </p>
      </div>

      <div className="card">
        <h2>👥 ユーザー一覧</h2>
        {users.length > 0 ? (
          <ul style={{ listStyle: 'none' }}>
            {users.map((user) => (
              <li key={user.id} style={{ marginBottom: '0.5rem' }}>
                <strong>{user.username}</strong> - {user.email}
              </li>
            ))}
          </ul>
        ) : (
          <p>データがありません</p>
        )}
      </div>

      <div className="card">
        <h2>💻 コード例</h2>
        <pre>{`// フロントエンド (React)
const response = await axios.get('/api/users')
setUsers(response.data)

// バックエンド (Express + Prisma)
app.get('/api/users', async (req, res) => {
  const users = await prisma.user.findMany()
  res.json(users)
})`}</pre>
      </div>

      <div className="card">
        <h2>📝 注意</h2>
        <p>
          完全なSSR (サーバーサイドレンダリング) を実現するには、Next.jsなどのフレームワークが必要です。
          このReactテンプレートでは、APIエンドポイント経由でのデータ取得を実装することで、
          Prismaの使用例を示しています。
        </p>
      </div>
    </div>
  )
}

export default PrismaPage
