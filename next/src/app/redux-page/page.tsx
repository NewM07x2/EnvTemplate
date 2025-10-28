'use client'
import React from 'react'
import { useAppSelector, useAppDispatch } from '../../hooks';
import { RootState } from '../../store/store';
import { increment, decrement } from '../../store/slices/counterSlice';
import { addAsyncThunk, clearApiData } from '../../store/slices/counterApiSlice';

export default function Reducer() {

  const count = useAppSelector((state: RootState) => state.counter.value);
  const dispatch = useAppDispatch();

  const apiData = useAppSelector((state: RootState) => state.counterAPI.data);
  const status = useAppSelector((state: RootState) => state.counterAPI.status);

  const addAsync = () => {
    // JSON初期化
    dispatch(clearApiData());
    // JSON取得
    dispatch(addAsyncThunk());
  };

  return (
    <>
      <p className="text-4xl">Redux Page</p>
      <div>
        <h1>Counter: {count}</h1>
        <button onClick={() => dispatch(increment(2))}> + </button>
        <button onClick={() => dispatch(decrement(0))}> - </button>
      </div>
      {/* 非同期処理をRedux Thunkを用いて記載する。 */}
      <div>
        {apiData && Object.keys(apiData).length > 0 && (
          <h1>API Data: {JSON.stringify(apiData)}</h1>
        )}
        <button onClick={addAsync}>Add Async</button>
        {status === 'loading' && <p>Loading...</p>}
        {status === 'failed' && <p>Error occurred</p>}
      </div>
    </>
  );
}
// インストール情報
// npm install @reduxjs/toolkit
// npm install react-redux