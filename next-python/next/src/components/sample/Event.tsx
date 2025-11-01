"use client"
import React, { useState,  PropsWithChildren } from 'react';

interface EventModel {
  person: {
    name: string;
    age: number | string;
  };
  updatePerson: (person: { name: string; age: number | string }) => void;
  resetPerson: () => void;
}

export const Event = ({ person, updatePerson, resetPerson }: EventModel) => {
  
  // オブジェクトを書き換える場合、1項目だけ変えると、他が初期化されてしまうので、
  // 全体をコピーした上で、変えたい項目のみ更新すること！
  const changeName = (event: React.ChangeEvent<HTMLInputElement>) => {
    person.name = '';
    updatePerson({ ...person, name: event.target.value })
  }
  const changeAge = (event: React.ChangeEvent<HTMLInputElement>) => {
    updatePerson({ ...person, age: event.target.value })
  }
  const reset = () => {
    resetPerson()
  }

  return (
    <div className='mx-1 my-1 p-2 flex flex-col items-center space-y-4 border border-solid border-gray-300'>
      <h3 className='text-left self-start'>Event Component</h3>
      <div className='flex flex-col items-center'>
        <div>↓↓↓名前を入力↓↓↓</div>
        <input type="text" value={person.name} onChange={changeName} className="border border-gray-300 rounded-md p-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"/>
      </div>
      
      <div className='flex flex-col items-center'>
        <div>↓↓↓年齢を入力↓↓↓</div>
        <input type="number" value={person.age} onChange={changeAge} className="border border-gray-300 rounded-md p-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"/>
      </div>
      
      <div>
        <button onClick={reset} className='bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded'>
          リセット
        </button>
      </div>
    </div>
  );
}