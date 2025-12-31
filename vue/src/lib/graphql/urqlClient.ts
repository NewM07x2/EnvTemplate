import { createClient, fetchExchange } from '@urql/core'

const GRAPHQL_ENDPOINT = import.meta.env.VITE_GRAPHQL_ENDPOINT || 'http://localhost:8080/graphql'

export const urqlClient = createClient({
  url: GRAPHQL_ENDPOINT,
  exchanges: [fetchExchange]
})
