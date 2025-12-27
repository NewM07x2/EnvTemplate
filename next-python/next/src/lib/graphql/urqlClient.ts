import { cacheExchange, createClient, fetchExchange, ssrExchange } from 'urql';

const isServerSide = typeof window === 'undefined';
const ssrCache = ssrExchange({ isClient: !isServerSide });

export const urqlClient = createClient({
  url: process.env.NEXT_PUBLIC_GRAPHQL_ENDPOINT || 'http://localhost:8000/graphql',
  exchanges: [cacheExchange, ssrCache, fetchExchange],
  fetchOptions: () => {
    return {
      headers: {
        // 'Authorization': `Bearer ${token}`,
      },
    };
  },
});
