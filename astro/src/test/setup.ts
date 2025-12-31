import { afterEach } from 'vitest'
import { cleanup } from '@testing-library/react'

// テスト後のクリーンアップ
afterEach(() => {
  cleanup()
})
