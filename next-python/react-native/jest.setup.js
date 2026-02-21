import '@testing-library/jest-native/extend-expect'

// Mock expo modules
jest.mock('expo-constants', () => ({
  expoConfig: {
    extra: {}
  }
}))

jest.mock('expo-linking', () => ({
  createURL: jest.fn()
}))
