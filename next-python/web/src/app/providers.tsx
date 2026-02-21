'use client'

import { Provider } from 'react-redux'
import { UrqlProvider } from '@urql/next'
import { store } from '../store/store'
import { urqlClient } from '../lib/graphql/urqlClient'

export function Providers({ children }: { children: React.ReactNode }) {
  return (
    <UrqlProvider client={urqlClient}>
      <Provider store={store}>
        {children}
      </Provider>
    </UrqlProvider>
  )
}
