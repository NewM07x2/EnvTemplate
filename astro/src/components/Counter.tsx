import { useState } from 'react';

export default function Counter() {
  const [count, setCount] = useState(0);

  return (
    <div className="space-y-4">
      <div className="text-center">
        <p className="text-4xl font-bold text-blue-600 mb-4">{count}</p>
        <div className="flex gap-4 justify-center">
          <button
            onClick={() => setCount(count - 1)}
            className="bg-red-500 text-white px-6 py-2 rounded-lg hover:bg-red-600 transition"
          >
            -1
          </button>
          <button
            onClick={() => setCount(0)}
            className="bg-gray-500 text-white px-6 py-2 rounded-lg hover:bg-gray-600 transition"
          >
            リセット
          </button>
          <button
            onClick={() => setCount(count + 1)}
            className="bg-blue-500 text-white px-6 py-2 rounded-lg hover:bg-blue-600 transition"
          >
            +1
          </button>
        </div>
      </div>
      <p className="text-sm text-gray-500 text-center">
        このカウンターはReactコンポーネントです（client:load）
      </p>
    </div>
  );
}
