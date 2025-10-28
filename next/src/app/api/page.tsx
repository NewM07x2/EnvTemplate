'use client'
import { useEffect, useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { RootState } from '../../store/store';
import Link from 'next/link';


// APIレスポンスの型を定義
interface ApiResponse {
  message: string;
}

const getSampleApi = async (): Promise<ApiResponse> => {
  try {
    const res = await fetch(
      'http://localhost:3000/api/sample', 
      { 
        method: 'GET', 
        cache: 'no-store'
      }
    );
    return await res.json();
  } catch (error) {
    console.error('Error fetching API:', error);
    throw error; // エラーを再スローする
  }
}

const ApiPage = () => {
  const count = useSelector((state: RootState) => state.counter.value);
  const [apiData, setApiData] = useState<ApiResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const response = await getSampleApi();
        setApiData(response);
      } catch (error) {
        console.error('Error fetching API:', error);
        setApiData(null);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);
  
  return (
    <>
      <p className="text-4xl api-title">API Page</p>
      <Link href="/api/get-api" className="text-gray-300 hover:bg-gray-700 px-3 py-2 rounded">GetAPI</Link>
      <div>
        {loading ? (
          "処理中..."
        ) : apiData ? (
          apiData.message
        ) : (
          "データの取得に失敗しました。"
        )}
      </div>
    </>
  );
}
export default ApiPage