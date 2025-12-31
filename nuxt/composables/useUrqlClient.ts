import { Client, cacheExchange, fetchExchange } from '@urql/vue'

export const useUrqlClient = () => {
  const config = useRuntimeConfig()
  
  const client = new Client({
    url: config.public.graphqlEndpoint,
    exchanges: [cacheExchange, fetchExchange],
    // リクエストヘッダーに認証トークンなどを追加する場合
    fetchOptions: () => {
      return {
        headers: {
          // 'Authorization': `Bearer ${token}`,
        },
      }
    },
  })
  
  return client
}
