// 프로필 탭 콘텐츠

import React from 'react'

export default function ProfileTab() {
  return (
    <div className="bg-white rounded-lg shadow-md p-6 mb-6">
      <div className="flex flex-col md:flex-row gap-6">
        <div className="md:w-1/3">
          <div className="bg-gray-100 rounded-lg p-4 h-full flex flex-col items-center justify-center">
            <div className="w-40 h-40 relative">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" className="w-full h-full">
                <path d="M256 0C114.6 0 0 114.6 0 256s114.6 256 256 256 256-114.6 256-256S397.4 0 256 0zm0 448c-105.9 0-192-86.1-192-192S150.1 64 256 64s192 86.1 192 192-86.1 192-192 192z" fill="#FFD700"/>
                <path d="M256 128c-70.7 0-128 57.3-128 128s57.3 128 128 128 128-57.3 128-128-57.3-128-128-128zm0 208c-44.2 0-80-35.8-80-80s35.8-80 80-80 80 35.8 80 80-35.8 80-80 80z" fill="#FF6B6B"/>
                <circle cx="256" cy="256" r="32" fill="#4FC3F7"/>
              </svg>
              <div className="absolute bottom-0 right-0 bg-blue-500 text-white rounded-full w-10 h-10 flex items-center justify-center text-lg font-bold">5</div>
            </div>
            <h3 className="text-xl font-bold mt-4">피카츄</h3>
            <p className="text-gray-500 text-sm">전기 타입</p>
            <div className="w-full mt-4">
              <div className="flex justify-between text-sm mb-1">
                <span>경험치</span>
                <span>340/500</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-3">
                <div className="bg-yellow-400 h-3 rounded-full" style={{ width: '68%' }}></div>
              </div>
            </div>
          </div>
        </div>
        <div className="md:w-2/3">
          <h2 className="text-2xl font-bold mb-4">내 정보</h2>
          <form className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">이름</label>
              <input type="text" className="w-full px-3 py-2 border border-gray-300 rounded-md" defaultValue="김코딩" />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">선호하는 활동 스타일</label>
              <select className="w-full px-3 py-2 border border-gray-300 rounded-md" defaultValue="활동적인">
                <option>활동적인</option>
                <option>차분한</option>
                <option>모험적인</option>
                <option>분석적인</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">좋아하는 취미</label>
              <input type="text" className="w-full px-3 py-2 border border-gray-300 rounded-md" defaultValue="코딩, 게임" />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">가장 좋아하는 장소</label>
              <input type="text" className="w-full px-3 py-2 border border-gray-300 rounded-md" defaultValue="카페" />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">가장 좋아하는 색깔</label>
              <input type="text" className="w-full px-3 py-2 border border-gray-300 rounded-md" defaultValue="파란색" />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">구체적으로 좋아하는 것들</label>
              <input type="text" className="w-full px-3 py-2 border border-gray-300 rounded-md" defaultValue="새로운 기술 배우기, 문제 해결하기" />
            </div>
            <div className="md:col-span-2">
              <label className="block text-sm font-medium text-gray-700 mb-1">구체적으로 싫어하는 것들</label>
              <input type="text" className="w-full px-3 py-2 border border-gray-300 rounded-md" defaultValue="지루한 반복 작업, 긴 회의" />
            </div>
          </form>
          <div className="mt-6 flex justify-end">
            <button type="button" className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 transition">나에게 맞는 포켓몬 찾기</button>
          </div>
          <div className="mt-8">
            <h3 className="text-xl font-bold mb-4">추천 이유</h3>
            <div className="bg-yellow-50 border-l-4 border-yellow-400 p-4 rounded">
              <p className="text-sm text-gray-700">
                <span className="font-bold">피카츄</span>는 당신의 활동적이고 모험적인 성향과 잘 어울립니다.<br/>
                새로운 기술을 배우는 것을 좋아하는 당신처럼 피카츄도 다양한 전기 기술을 습득하는 것을 좋아합니다.<br/>
                또한 문제 해결 능력이 뛰어난 당신의 특성은 피카츄의 영리함과 일치합니다.<br/>
                파란색을 좋아하는 당신의 취향은 피카츄의 밝고 긍정적인 에너지와 조화를 이룹니다.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
