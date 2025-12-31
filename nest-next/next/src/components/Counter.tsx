'use client';

import { useAppDispatch, useAppSelector } from '@/hooks';
import { increment, decrement, reset } from '@/store/slices/counterSlice';

export default function Counter() {
  const count = useAppSelector((state) => state.counter.value);
  const dispatch = useAppDispatch();

  return (
    <div className="flex flex-col items-center gap-4 p-6 border rounded-lg bg-white shadow-sm">
      <h2 className="text-2xl font-bold">Redux Counter</h2>
      <div className="text-4xl font-bold text-blue-600">{count}</div>
      <div className="flex gap-2">
        <button
          onClick={() => dispatch(decrement())}
          className="px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600 transition"
        >
          -1
        </button>
        <button
          onClick={() => dispatch(reset())}
          className="px-4 py-2 bg-gray-500 text-white rounded hover:bg-gray-600 transition"
        >
          Reset
        </button>
        <button
          onClick={() => dispatch(increment())}
          className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition"
        >
          +1
        </button>
      </div>
    </div>
  );
}
