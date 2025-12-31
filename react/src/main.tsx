import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import { Provider as ReduxProvider } from 'react-redux'
import { Provider as UrqlProvider } from 'urql'
import { store } from './store/store.ts'
import { urqlClient } from './lib/graphql/urqlClient.ts'
import App from './App.tsx'
import './styles/index.css'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <ReduxProvider store={store}>
      <UrqlProvider value={urqlClient}>
        <BrowserRouter>
          <App />
        </BrowserRouter>
      </UrqlProvider>
    </ReduxProvider>
  </StrictMode>,
)
