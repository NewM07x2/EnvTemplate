'use client'
import React, { useState, useEffect, PropsWithChildren } from 'react';

import Profile from './Profile'

interface ListModel {
  person: {
    name: string;
    age: number | string;
  };
}
interface InputFact {
  key: number | String;
  value: React.ReactElement;
}

const animals = ["Dog", "Cat", "Rat"];

const generateThreeDigitNumber = (): string => {
  const num = Math.floor(Math.random() * 1000);
  return num.toString().padStart(3, '0');
};

const inputFact = () => ({
  key: generateThreeDigitNumber(),
  value: <input type="text" className="border border-gray-300 rounded-md p-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"/>,
});

const persons = [
  {
    name: "Geo",
    age: 18,
    hobbies: ["sports", "music"],
  },
  {
    name: "Tom",
    age: 25,
    hobbies: ["movie", "music"],
  },
  {
    name: "Lisa",
    age: 21,
    hobbies: ["sports", "travel", "game"],
  },
];

export const Array = ({ children, ...props }: PropsWithChildren<ListModel>) => {
  const [searchText, setSearchText] = useState("");
  const [inputs, setInputs] = useState<InputFact[]>([]);

  useEffect(() => {
    setInputs([inputFact(), inputFact(), inputFact()]);
  }, []);
  
  const unshiftInput = () => {
    setInputs((prev) => [inputFact(), ...prev]);
  };
  return (
    <div className='mx-1 my-1 p-2 flex flex-col items-center space-y-4 border border-solid border-gray-300'>
      <h3 className='text-left self-start'>Array Component</h3>
      <button onClick={unshiftInput}>先頭に追加</button>
      <input type="text" value={searchText} onChange={(e) => setSearchText(e.target.value)} className="border border-gray-300 rounded-md p-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"/>
      <ul>
        {
          animals
            .filter(animal => {
              return animal.indexOf(searchText) !== -1;
            })
            .map((animal) => (
              <li key={animal}>{animal}</li>
            ))
        }
      </ul>
      <ul>
        {inputs.map((input) => (
          <li key={input.key.toString()}>
            {input.key}: {input.value}
          </li>
        ))}
      </ul>
      <ul>
        {/* mapで各要素に特定の処理を行ったものを新しい配列とする */}
        {false && persons.map((person) => (
            /* リストにはkeyを設定することを忘れないように！ */
            <li key={person.name}>
            <Profile {...person} />
          </li>
        ))}
      </ul>
    </div>
  )
}