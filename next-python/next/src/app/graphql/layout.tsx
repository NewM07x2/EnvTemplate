import type { Metadata } from "next";
import Link from 'next/link';
import Image from 'next/image';
import "@/styles/globals.css";

import React from 'react';

export default function RootLayout({ children }: { children: React.ReactNode }) {
  
  return (
    <div>
        <div className="flex flex-1 justify-center items-center flex-col w-screen">
          {children}
        </div>
    </div>
  );
}