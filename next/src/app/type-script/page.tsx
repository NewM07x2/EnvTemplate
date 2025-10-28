'use strict'
import Link from 'next/link';
import Image from 'next/image';

import weatherConditions from './weather_conditions.json';

export default function TypeScriptPage() {
  console.log(`-------`)
  // 文字列の型定義
  /*
  const str1: string = '1'
  const str2: string = '2'
  const str3: string = str1 + str2;
  console.log(str3)

  const OKFlg: boolean = true
  const NGFlg: boolean = false
  console.log(OKFlg) 
  console.log(NGFlg) 
  
  // 数値のリストを定義
  const numberList: Array<number> = [1, 2, 3, 4, 5];
  // 文字列のリストを定義
  const namesList: Array<string> = ['Alice', 'Bob', 'Charlie'];
  // 数値と文字列のリストを結合
  const combinedList: Array<number | string> = [...numberList, ...namesList];
  // 結合されたリストをコンソールに出力
  console.log(combinedList);

  */

  const cityInfo = [
    {
      id: 'osaka',
      englishName: 'Osaka',
      japaneseName: '大阪',
      latitude: 34.6937,
      longitude: 135.5023
    },
    {
      id: 'tokyo',
      englishName: 'Tokyo',
      japaneseName: '東京',
      latitude: 35.6895,
      longitude: 139.6917
    }
  ];
  const apiKey = '5d08679cc82c4250b5a145708242310';
  const city = 'Tokyo';
  const url = `http://api.weatherapi.com/v1/current.json?key=${apiKey}&q=${city}&aqi=no`;
  
  fetch(url)
    .then(response => response.json())
    .then(data => {
      // console.log(data)
      const cityObj = cityInfo.find(item => item.englishName === data.location.name);
      // console.log(cityObj)
      
      if (cityObj) {
        console.log(data.current.condition.code)
        const condition = weatherConditions.find(item => item.code === data.current.condition.code);
        const japaneseCondition = condition ? condition.languages.find(lang => lang.lang_iso === 'ja') : null;
        console.log(japaneseCondition)

        console.log(`${cityObj.japaneseName}の現在の気温: ${data.current.temp_c}°C`);
        console.log(`天気: ${japaneseCondition ? japaneseCondition.day_text : data.current.condition.text}`);
        console.log(`湿度: ${data.current.humidity}%`);
        console.log(`湿度: ${data.current.humidity}%`);
      } else {
        console.log(`${city}の情報が見つかりませんでした`);
      }
    })
    .catch(error => console.error('Error:', error));



  console.log(`-------`)
  return (
    <>
      <div className="p-8 flex flex-col h-full w-full">
        <div className="p-8 border-gray-100 rounded-xl w-full bg-gray-200 h-full">
          <h1 className="text-4xl my-4 flex-shrink-0">TypeScript Page</h1>
          <div className="flex-1 overflow-hidden">
            <p className="font-bold">天気予報取得</p>
          </div>
        </div>
      </div>
    </>
  );
}
