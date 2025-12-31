import '@testing-library/jest-dom'
import { cleanup } from '@testing-library/react'
import { afterEach } from 'vitest'

// テスト後のクリーンアップ
afterEach(() => {
  cleanup()
})

// グローバルモック設定
global.matchMedia = global.matchMedia || function () {
  return {
    matches: false,
    addListener: function () {},
    removeListener: function () {},
  }
}
