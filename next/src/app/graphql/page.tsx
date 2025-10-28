'use client'
import { useSelector, useDispatch } from 'react-redux';
import { RootState } from '../../store/store';
import Link from 'next/link';
import { Button } from '@/';
import { PrismaClient } from "@prisma/client";

export default function GraphqlPage() {
  const prisma = new PrismaClient();

  const addData = async () => {
    try {
      const response = await fetch('/api/addData', {
        method: 'POST',
      });
      const newData = await response.json();
      console.log('Data added:', newData);
    } catch (error) {
      console.error('Error adding data:', error);
    }
  };


  const count = useSelector((state: RootState) => state.counter.value);
  return (
    <>
      <p className="text-4xl api-title">Graphql Page</p>
      <Link href="/api/get-api" className="text-gray-300 hover:bg-gray-700 px-3 py-2 rounded">GetAPI</Link>
      <button onClick={addData} className='bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded'>Get Data</button>
    </>
  );
}
