import { describe, it, expect } from 'vitest';

describe('基本的なテスト', () => {
  it('足し算が正しく動作する', () => {
    expect(1 + 1).toBe(2);
  });

  it('配列に要素が含まれる', () => {
    const arr = [1, 2, 3];
    expect(arr).toContain(2);
  });

  it('オブジェクトのプロパティが一致する', () => {
    const obj = { name: 'test', value: 42 };
    expect(obj).toHaveProperty('name', 'test');
  });
});
