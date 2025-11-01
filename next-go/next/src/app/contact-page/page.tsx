import Link from 'next/link';
import Image from 'next/image';

export default function ContactPage() {
  return (
    <>
      <div className="bg-white text-center shadow-xl p-8 w-80 rounded">
        <div className="mt-4">
          <p className="font-bold">contact Info</p>
        </div>
        <div className="flex justify-center mt-2">
          <Image src="/sanuna.svg" alt="Vercel Logo" width={50} height={50} className="ml-1"/>
        </div>
        <div className="mt-4">
          <p className='font-bold'>Address</p>
          <p className='text-xs mt-1 text-gray-600'>東京都品川区</p>
          <p className='font-bold mt-2'>E-mail</p>
          <p className='text-xs mt-1 text-gray-600'>test@gmail.com</p>
          <p className='font-bold mt-2'>Phone</p>
          <p className='text-xs mt-1 text-gray-600'>090-0000-0000</p>
        </div>
        <Link href="/" className="block w-full"><label className="mt-4 text-gray-300 inline-block w-full rounded py-2 px-4 hover:bg-gray-700 hover:text-white transition-colors duration-200 ease-in-out">Home</label></Link>
      </div>

      {/* <div className="flex flex-1 justify-center items-center flex-col w-screen">
      </div> */}
    </>
  );
}
