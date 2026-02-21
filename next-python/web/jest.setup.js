// jest.setup.js
import '@testing-library/jest-dom'

// Mock next/router
jest.mock('next/router', () => ({
  useRouter() {
    return {
      route: '/',
      pathname: '/',
      query: {},
      asPath: '/',
      push: jest.fn(),
      replace: jest.fn(),
      reload: jest.fn(),
      back: jest.fn(),
      prefetch: jest.fn(),
      beforePopState: jest.fn(),
      events: {
        on: jest.fn(),
        off: jest.fn(),
        emit: jest.fn()
      },
      isFallback: false
    }
  }
}))

// Mock next/image
jest.mock('next/image', () => ({
  __esModule: true,
  default: (props) => {
    // eslint-disable-next-line jsx-a11y/alt-text
    return <img {...props} />
  }
}))

// Mock next/link
jest.mock('next/link', () => {
  return ({ children, href }) => {
    return children
  }
})

// Environment setup
process.env.NEXT_PUBLIC_GRAPHQL_ENDPOINT = 'http://localhost:8000/graphql'
process.env.NEXT_PUBLIC_API_URL = 'http://localhost:8000'
