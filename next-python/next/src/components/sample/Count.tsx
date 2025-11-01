"use client"
import React, { useState, useEffect, PropsWithChildren } from 'react';

interface CountModel {
  title?: any;
  count?: any;
  setCount?: any;
}

export const Count = ({ children, title, count, setCount }: PropsWithChildren<CountModel>) => {
  
  const plusCount = () => {
    setCount(count + 1)
  }
  const minusCount = () => {
    setCount(count - 1);
  }

  return (
    <div className='text-center'>
      <p className="text-4xl">Welcome to Home!</p>
      <p className="text-4xl">
        {title}: {count}
      </p>
      <div className='flex justify-center items-center gap-4 col-1'>
        <button className='bg-blue-500 hover:bg-blue-700 text-white py-2 px-4 rounded' onClick={plusCount}>+</button>
        <button className='bg-blue-500 hover:bg-blue-700 text-white py-2 px-4 rounded' onClick={minusCount}>-</button>
      </div>
    </div>
  )
}