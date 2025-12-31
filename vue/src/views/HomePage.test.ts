import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import HomePage from './HomePage.vue'

describe('HomePage.vue', () => {
  it('ホームページが正しくレンダリングされる', () => {
    const wrapper = mount(HomePage)
    expect(wrapper.text()).toContain('Vue + GraphQL + Prisma テンプレート')
  })

  it('主な技術スタックセクションが表示される', () => {
    const wrapper = mount(HomePage)
    expect(wrapper.text()).toContain('📦 主な技術スタック')
    expect(wrapper.text()).toContain('Vue 3')
    expect(wrapper.text()).toContain('TypeScript')
    expect(wrapper.text()).toContain('Vite')
  })

  it('使い方セクションが表示される', () => {
    const wrapper = mount(HomePage)
    expect(wrapper.text()).toContain('🚀 使い方')
    expect(wrapper.text()).toContain('GraphQL (CSR)')
    expect(wrapper.text()).toContain('Prisma (SSR)')
  })

  it('cardクラスが適用されている', () => {
    const wrapper = mount(HomePage)
    const cards = wrapper.findAll('.card')
    expect(cards.length).toBeGreaterThan(0)
  })
})
