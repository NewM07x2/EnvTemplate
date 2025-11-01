/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  logging: {
    fetches: {
      level: 'verbose',
      fullUrl: true,
    },
  },
};

export default nextConfig;
