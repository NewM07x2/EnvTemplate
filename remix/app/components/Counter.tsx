import { useState } from "react";

export default function Counter() {
  const [count, setCount] = useState(0);

  const doubled = count * 2;
  const isEven = count % 2 === 0;

  return (
    <div className="counter">
      <h2>React Counter</h2>

      <div className="display">
        <div className="count-value">{count}</div>
        <div className="derived-info">
          <span>2倍: {doubled}</span>
          <span className={`badge ${isEven ? "even" : "odd"}`}>
            {isEven ? "偶数" : "奇数"}
          </span>
        </div>
      </div>

      <div className="buttons">
        <button
          onClick={() => setCount(count - 1)}
          className="btn btn-danger"
        >
          -1
        </button>
        <button onClick={() => setCount(0)} className="btn btn-secondary">
          Reset
        </button>
        <button
          onClick={() => setCount(count + 1)}
          className="btn btn-primary"
        >
          +1
        </button>
      </div>

      <p className="info">
        Reactの<code>useState</code>フックを使用しています
      </p>
    </div>
  );
}
