'use client'
import Link from 'next/link';
import { useSelector, useDispatch } from 'react-redux';

export default function GetApiPage() {
  return (
    <>
      <p className="text-4xl api-title">Get API Page</p>
      <Link href="/api" className="text-gray-300 hover:bg-gray-700 px-3 py-2 rounded">API</Link>
    </>
  );
}
