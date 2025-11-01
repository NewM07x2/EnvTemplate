"use client"
import React, { useState, useEffect, useReducer } from 'react';
import { createPortal } from "react-dom";


type State = {
  a: number;
  b: number;
  result: number;
};
type CalcType = typeof CALC_OPTIONS[number];

type Action = {
  type: String;
  payload?: { name: string, value: number }
}
const CALC_OPTIONS = ["+", "-", "×", "÷"];

const reducer = (state: State, action: Action): State => {
  switch (action.type) {
    case "change":
      if (action.payload) {
        return {...state, [action.payload.name]: action.payload.value};
      }
    case "+":
      return {...state, result: state.a + state.b};
    case "-":
      return {...state, result: state.a - state.b};
    case "×":
      return {...state, result: state.a * state.b};
    case "÷":
      return {...state, result: state.b !== 0 ? Number((state.a / state.b).toFixed(2)) : state.result};
    default:
      throw new Error('不明なactionです。')
  }
};

export default function Reducer() {
  const initState = {
    a: 1,
    b: 2,
    result: 3,
  };

  const [calcType, setCalcTypeType] = useState(CALC_OPTIONS[0]);
  const [state, dispatch] = useReducer(reducer, initState);

  const calcExec = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const selectedType = e.target.value as CalcType;
    setCalcTypeType(selectedType);
    dispatch({type: selectedType, payload: { name: 'result', value: 0 }});
  };

  const inputChangeHandler = (e: React.ChangeEvent<HTMLInputElement>) => {
    const val = Number(e.target.value);
    dispatch({ type: "change", payload: { name: e.target.name, value: val } });
    dispatch({ type: calcType });
  };

  return (
    <>
      <p className="text-4xl">Reducer Page</p>
      <div className='flex flex-col justify-center items-center'>
        <select name="type" onChange={(e) => calcExec(e)}>
          {CALC_OPTIONS.map((type) => (
            <option key={type} value={type}>
              {type}
            </option>
          ))}
        </select>
        <div className='flex justify-center items-center gap-4 col-1'>
          <input type="number" name="a" value={state.a} onChange={(e) => inputChangeHandler(e)} className="border border-gray-300 rounded-md p-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 my-0.5"/>
          <label className='font-bold text-xl'> { calcType }</label>
          <input type="number" name="b" value={state.b} onChange={(e) => inputChangeHandler(e)} className="border border-gray-300 rounded-md p-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 my-0.5"/>
          <label className='font-bold text-xl'> = {state.result}</label>
        </div>
      </div>
    </>
  );
}