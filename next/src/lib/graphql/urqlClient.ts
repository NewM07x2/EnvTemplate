import { cacheExchange, createClient, fetchExchange, ssrExchange } from 'urql';

const isServerSide = typeof window === 'undefined';
const ssrCache = ssrExchange({ isClient: !isServerSide });

export const urqlClient = createClient({
  url: process.env.NEXT_PUBLIC_GRAPHQL_ENDPOINT || 'http://localhost:4000/graphql',
  exchanges: [cacheExchange, ssrCache, fetchExchange],
  // リクエストヘッダーに認証トークンなどを追加する場合
  fetchOptions: () => {
    return {
      headers: {
        // 'Authorization': `Bearer ${token}`,
      },
    };
  },
});
