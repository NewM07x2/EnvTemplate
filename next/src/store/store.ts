// store.ts
import { configureStore } from '@reduxjs/toolkit';
import counterSliceReducer from './slices/counterSlice';
import counterAPIReducer from './slices/counterApiSlice';

export const store = configureStore({
  reducer: {
    counter: counterSliceReducer,
    counterAPI: counterAPIReducer
  },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
