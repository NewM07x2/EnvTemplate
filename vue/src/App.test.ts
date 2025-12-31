import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import { createRouter, createWebHistory } from 'vue-router'
import App from '../App.vue'

describe('App.vue', () => {
  it('アプリケーションが正しくレンダリングされる', () => {
    const router = createRouter({
      history: createWebHistory(),
      routes: [
        { path: '/', component: { template: '<div>Home</div>' } },
        { path: '/graphql', component: { template: '<div>GraphQL</div>' } },
        { path: '/prisma', component: { template: '<div>Prisma</div>' } }
      ]
    })

    const wrapper = mount(App, {
      global: {
        plugins: [router]
      }
    })

    expect(wrapper.find('.app').exists()).toBe(true)
    expect(wrapper.find('.app-header').exists()).toBe(true)
    expect(wrapper.find('.nav-list').exists()).toBe(true)
  })

  it('ナビゲーションリンクが正しく表示される', () => {
    const router = createRouter({
      history: createWebHistory(),
      routes: [
        { path: '/', component: { template: '<div>Home</div>' } }
      ]
    })

    const wrapper = mount(App, {
      global: {
        plugins: [router]
      }
    })

    const links = wrapper.findAll('a')
    expect(links).toHaveLength(3)
    expect(links[0].text()).toBe('ホーム')
    expect(links[1].text()).toBe('GraphQL (CSR)')
    expect(links[2].text()).toBe('Prisma (SSR)')
  })
})
