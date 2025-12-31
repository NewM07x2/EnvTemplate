import { useQuery } from 'urql'

const USERS_QUERY = `
  query {
    users {
      id
      username
      email
    }
  }
`

function GraphQLPage() {
  const [result] = useQuery({ query: USERS_QUERY })

  if (result.fetching) {
    return <div className="loading">読み込み中...</div>
  }

  if (result.error) {
    return (
      <div>
        <h1>GraphQL (CSR) - urql</h1>
        <div className="error">
          エラー: {result.error.message}
          <p style={{ marginTop: '1rem', fontSize: '0.9rem' }}>
            GraphQL APIサーバーが起動していることを確認してください。
          </p>
        </div>
      </div>
    )
  }

  return (
    <div>
      <h1>GraphQL (CSR) - urql</h1>
      
      <div className="card">
        <h2>📡 urqlを使用したデータ取得</h2>
        <p>
          このページでは、<code>urql</code>を使用してGraphQL APIからデータを取得します。
          クライアントサイドレンダリング (CSR) で動作します。
        </p>
      </div>

      <div className="card">
        <h2>👥 ユーザー一覧</h2>
        {result.data?.users?.length > 0 ? (
          <ul style={{ listStyle: 'none' }}>
            {result.data.users.map((user: any) => (
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
        <pre>{`import { useQuery } from 'urql'

const USERS_QUERY = \`
  query {
    users {
      id
      username
      email
    }
  }
\`

function GraphQLPage() {
  const [result] = useQuery({ query: USERS_QUERY })
  // ...
}`}</pre>
      </div>
    </div>
  )
}

export default GraphQLPage
