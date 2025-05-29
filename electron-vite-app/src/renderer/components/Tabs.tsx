// 상단탭 (내프로필 / 채팅 / 학습관리)

import React from 'react'

type Props = {
  activeTab: string
  setActiveTab: (tab: string) => void
}

export default function Tabs({ activeTab, setActiveTab }: Props) {
  return (
    <div className="flex border-b border-gray-200 mb-6">
      {['profile', 'chat', 'learning'].map((tab) => (
        <button
          key={tab}
          onClick={() => setActiveTab(tab)}
          className={`px-4 py-2 flex-1 text-center font-semibold transition-colors duration-200 ${
            activeTab === tab ? 'tab-active border-b-2 border-blue-500 text-blue-700' : 'text-gray-500 hover:text-blue-600'
          }`}
        >
          {tab === 'profile' ? '내 프로필' : tab === 'chat' ? '포켓몬 채팅' : '학습 관리'}
        </button>
      ))}
    </div>
  )
}
