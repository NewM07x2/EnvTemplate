import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import { createPinia, setActivePinia } from 'pinia'
import Counter from './Counter.vue'

describe('Counter', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
  })

  it('初期値0で表示される', () => {
    const wrapper = mount(Counter)
    expect(wrapper.text()).toContain('0')
  })

  it('ボタンが3つ存在する', () => {
    const wrapper = mount(Counter)
    const buttons = wrapper.findAll('button')
    expect(buttons).toHaveLength(3)
    expect(buttons[0].text()).toBe('-1')
    expect(buttons[1].text()).toBe('リセット')
    expect(buttons[2].text()).toBe('+1')
  })

  it('+1ボタンで値が増加する', async () => {
    const wrapper = mount(Counter)
    const incrementButton = wrapper.findAll('button')[2]
    
    await incrementButton.trigger('click')
    expect(wrapper.text()).toContain('1')
  })

  it('-1ボタンで値が減少する', async () => {
    const wrapper = mount(Counter)
    const decrementButton = wrapper.findAll('button')[0]
    
    await decrementButton.trigger('click')
    expect(wrapper.text()).toContain('-1')
  })
})
