// counterSlice.ts
// reduxjs/toolkitで使用する場合の「reducer」の役割
import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import { getJsonData } from '../../app/api/getJsonData';

interface CounterState {
  data: any;
  status: 'idle' | 'loading' | 'succeeded' | 'failed';
  error: string | null;
}
const initialState: CounterState = {
  data: {},
  status: 'idle',
  error: null,
};

export const addAsyncThunk = createAsyncThunk(
  'addAsync',
  async () => {
    const response = await getJsonData();
    console.log(response.data);
    return response.data;
}
);

export const counterAPISlice = createSlice({
  name: 'counter',
  initialState,
  reducers: {
    clearApiData: (state) => {
      state.data = {};
      state.status = 'idle';
      state.error = null;
    }
  },
  extraReducers: (builder) => {
    builder
      .addCase(addAsyncThunk.pending, (state) => {
        state.status = 'loading';
      })
      .addCase(addAsyncThunk.fulfilled, (state, action: PayloadAction<number>) => {
        state.status = 'succeeded';
        state.data = action.payload;
      })
      .addCase(addAsyncThunk.rejected, (state, action) => {
        state.status = 'failed';
        state.error = action.error.message || null;
      });
  },
});

export const { clearApiData } = counterAPISlice.actions;
export default counterAPISlice.reducer;