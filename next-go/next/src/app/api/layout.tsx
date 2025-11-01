import React from 'react';
import Link from 'next/link';
import "./style.css";

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <>
      <div className="flex flex-1 justify-center items-center flex-col w-screen api-layout">
        api layout
        { children }
      </div>
    </>
  );
}
