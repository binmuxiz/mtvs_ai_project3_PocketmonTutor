// 탭 UI 컴포넌트 ( 포켓본 매칭, 학습 파트너 )


import { useState } from 'react'
import PokemonForm from './PokemonForm'

export default function PokemonTabs() {
  const [activeTab, setActiveTab] = useState<'match' | 'learn'>('match')

  const switchTab = (tab: 'match' | 'learn') => setActiveTab(tab)

  return (
    <div className="mb-6">
      {/* 탭 버튼 */}
      <div className="flex rounded-lg overflow-hidden mb-4">
        <button
          className={`py-3 px-6 flex-1 text-center transition-all duration-200 ${activeTab === 'match' ? 'bg-indigo-600 text-white' : 'bg-gray-100 text-gray-700'}`}
          onClick={() => switchTab('match')}
        >
          포켓몬 매칭
        </button>
        <button
          className={`py-3 px-6 flex-1 text-center transition-all duration-200 ${activeTab === 'learn' ? 'bg-indigo-600 text-white' : 'bg-gray-100 text-gray-700'}`}
          onClick={() => switchTab('learn')}
        >
          학습 파트너
        </button>
      </div>

      {/* 탭 내용 */}
      <div className="bg-white rounded-xl shadow-lg p-6">
        {activeTab === 'match' && (
          <div className="grid md:grid-cols-2 gap-8">
            <PokemonForm />
            {/* 추후: <PokemonCard /> */}
            <div className="flex items-center justify-center text-gray-400">
              포켓몬 추천 결과 영역 (추후 구현)
            </div>
          </div>
        )}

        {activeTab === 'learn' && (
          <div className="grid md:grid-cols-2 gap-8">
            {/* 추후: <PokemonStatus /> + <ChatPanel /> */}
            <div className="h-64 bg-indigo-50 flex items-center justify-center rounded-xl">
              포켓몬 3D 모델 + 경험치 바 자리
            </div>
            <div className="h-64 bg-gray-50 flex items-center justify-center rounded-xl">
              챗봇 패널 자리
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
