'use client'
import React, { useState, useEffect, PropsWithChildren } from 'react';

interface ListModel {
  person: {
    name: string;
    age: number | string;
  };
}

export const List = ({ children, ...props }: PropsWithChildren<ListModel>) => {
  const person = props.person;
  return (
    <div className='mx-1 my-1 p-2 flex flex-col items-center space-y-4 border border-solid border-gray-300'>
      <h3 className='text-left self-start'>List Component</h3>
      {children}
      <ul>
        {
          Object.entries(person).map(([key, value]) => (
            <li key={key}>{key}: {value}</li>
          ))
        }
      </ul>
    </div>
  )
}