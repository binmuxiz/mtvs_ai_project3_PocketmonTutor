import { useState } from 'react'
import { PokemonData } from '../types/PokemonData'; // 혹은 경로에 맞게

interface Props {
  data: PokemonData;
  onConfirm: () => void;
}

const typeColors: Record<string, string> = {
  노말: "bg-gray-300 text-gray-900",
  불꽃: "bg-orange-400 text-white",
  물: "bg-blue-400 text-white",
  풀: "bg-green-400 text-white",
  전기: "bg-yellow-300 text-black",
  얼음: "bg-cyan-300 text-black",
  격투: "bg-red-600 text-white",
  독: "bg-purple-400 text-white",
  땅: "bg-yellow-700 text-white",
  비행: "bg-indigo-300 text-white",
  에스퍼: "bg-pink-400 text-white",
  벌레: "bg-lime-500 text-black",
  바위: "bg-yellow-800 text-white",
  고스트: "bg-purple-700 text-white",
  드래곤: "bg-indigo-600 text-white",
  악: "bg-gray-800 text-white",
  강철: "bg-slate-400 text-white",
  페어리: "bg-pink-200 text-black",
};


function PokemonCard({ data, onConfirm }: Props) {
  return (
    <div className="card-container">
      <div className="card max-w-xl mx-auto rounded-xl overflow-hidden shadow-lg bg-white transition-transform duration-500">

        {/* 카드 헤더: 이름 + 번호 */}
        <div className="flex justify-between items-center px-4 py-2 bg-gradient-to-r from-orange-500 to-red-600 text-white font-bold text-lg rounded-t-xl">
          <span>{data.name}</span>
          <span>#{data.no}</span>
        </div>
        {/* 이미지와 타입 배지 */}
        <div className="relative h-64 bg-gradient-to-b from-orange-200 to-amber-100">
          <img
            src={data.image}
            alt={data.name}
            className="absolute inset-0 w-full h-full object-contain p-4"
          />
          <div className="absolute bottom-2 right-2 flex gap-2">
            {data.pokemon_type.map((type, index) => (
            <span
              key={index}
              className={`px-3 py-1 rounded-full text-sm font-bold ${typeColors[type] || "bg-gray-200 text-gray-800"}`}
            >
              {type}
            </span>
            ))}
          </div>
        </div>

        {/* 설명 */}
        <div className="p-5">
          <div className="mb-4 bg-amber-50 p-3 rounded-lg shadow-inner">
            <p className="text-gray-700 leading-relaxed">{data.description}</p>
          </div>

          {/* 매칭 정보 */}
          <div className="bg-amber-50 rounded-lg shadow-inner p-3">
            <h2 className="text-lg font-bold text-orange-800 mb-2">매칭 정보</h2>
            <div className="space-y-2">
              {Object.entries(data.match).map(([key, value]) => (
                <div key={key} className="flex items-center">
                  <span className="w-24 text-orange-700 font-medium">
                    {key === "personality"
                      ? "성격"
                      : key === "hobby"
                      ? "취미"
                      : key === "color"
                      ? "색상"
                      : key === "mood"
                      ? "분위기"
                      : key === "type"
                      ? "타입"
                      : key}
                    :
                  </span>
                  <span
                    className={`px-2 py-1 rounded text-sm ${
                      value.includes("강렬")
                        ? "bg-red-100 text-red-800"
                        : value.includes("안됨")
                        ? "bg-gray-100 text-gray-800"
                        : "bg-green-100 text-green-800"
                    }`}
                  >
                    {value}
                  </span>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* 버튼 */}
        <div className="bg-gradient-to-r from-orange-600 to-red-600 p-3 text-center">
          <button
            onClick={onConfirm}
            className="text-white font-bold py-2 px-4 rounded hover:opacity-90"
          >
            이 포켓몬으로 할래요!
          </button>
        </div>
      </div>
    </div>
  );
}

export default PokemonCard;
