import { Routes, Route, Link } from 'react-router-dom'
import HomePage from './pages/HomePage'
import GraphQLPage from './pages/GraphQLPage'
import PrismaPage from './pages/PrismaPage'

function App() {
  return (
    <div className="app">
      <header className="app-header">
        <nav>
          <ul className="nav-list">
            <li><Link to="/">ホーム</Link></li>
            <li><Link to="/graphql">GraphQL (CSR)</Link></li>
            <li><Link to="/prisma">Prisma (SSR)</Link></li>
          </ul>
        </nav>
      </header>
      <main className="app-main">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/graphql" element={<GraphQLPage />} />
          <Route path="/prisma" element={<PrismaPage />} />
        </Routes>
      </main>
    </div>
  )
}

export default App
