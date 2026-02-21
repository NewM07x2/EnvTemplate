import React from 'react';
import { render } from '@testing-library/react-native';
import { Provider } from 'react-redux';
import { store } from '@/store/store';

describe('Counter Slice', () => {
  it('should have initial value of 0', () => {
    const state = store.getState();
    expect(state.counter.value).toBe(0);
  });
});

describe('User Slice', () => {
  it('should have null initial user', () => {
    const state = store.getState();
    expect(state.user.currentUser).toBeNull();
    expect(state.user.isLoading).toBe(false);
    expect(state.user.error).toBeNull();
  });
});
