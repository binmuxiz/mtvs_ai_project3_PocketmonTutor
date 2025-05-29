// 채팅탭 콘텐츠

import React, { useState } from 'react'

export default function ChatTab() {
  const [messages, setMessages] = useState([
    { role: 'pokemon', text: '안녕하세요! 오늘은 어떤 학습을 도와드릴까요?' },
    { role: 'user', text: '오늘 RAG 수업을 했는데 이거 복습할거야.' },
    { role: 'pokemon', text: '좋아요! RAG(Retrieval-Augmented Generation) 복습 일정을 추가했어요. 어떤 부분이 어려웠나요?' },
    { role: 'user', text: '벡터 데이터베이스 부분이 좀 어려웠어.' },
    { role: 'pokemon', text: '벡터 데이터베이스에 대한 간단한 문제를 내볼게요!\nQ: 벡터 데이터베이스에서 코사인 유사도를 사용하는 주된 이유는 무엇인가요?\n1. 데이터 저장 공간을 절약하기 위해\n2. 벡터의 방향 유사성을 측정하기 위해\n3. 계산 속도를 높이기 위해\n4. 데이터베이스 보안을 강화하기 위해' },
    { role: 'user', text: '2번!' },
    { role: 'pokemon', text: '정답입니다! 벡터의 방향 유사성을 측정하는 것이 코사인 유사도의 주된 목적이에요. 경험치 +10 획득했습니다! 🎉' }
  ])
  const [input, setInput] = useState('')

  const handleSend = () => {
    if (!input.trim()) return
    const newMessages = [...messages, { role: 'user', text: input }]
    setMessages(newMessages)
    setInput('')

    // 간단한 응답 시뮬레이션
    setTimeout(() => {
      const response = input.includes('학습') || input.includes('공부')
        ? '학습 일정을 추가할까요? 어떤 주제에 대해 공부하고 싶으신가요?'
        : input.includes('문제') || input.includes('퀴즈')
        ? '좋아요! 어떤 주제에 대한 문제를 풀고 싶으신가요?'
        : '더 자세히 말씀해주시겠어요? 학습 일정 관리나 문제 풀이를 도와드릴 수 있어요!'
      setMessages(prev => [...prev, { role: 'pokemon', text: response }])
    }, 500)
  }

  return (
    <div className="bg-white rounded-lg shadow-md p-6 mb-6 h-[600px] flex flex-col">
      <div className="flex-grow overflow-y-auto mb-4 p-2" id="chat-messages">
        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={`chat-bubble mb-2 ${msg.role === 'user' ? 'user-bubble text-right' : 'pokemon-bubble text-left'}`}
          >
            <p className="bg-gray-100 inline-block px-4 py-2 rounded-lg max-w-[80%]">
              {msg.text.split('\n').map((line, i) => (
                <span key={i} className="block">{line}</span>
              ))}
            </p>
          </div>
        ))}
      </div>
      <div className="border-t pt-4">
        <div className="flex items-center">
          <input
            type="text"
            placeholder="메시지를 입력하세요..."
            className="flex-grow px-4 py-2 border border-gray-300 rounded-l-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSend()}
          />
          <button
            onClick={handleSend}
            className="bg-blue-600 text-white px-4 py-2 rounded-r-md hover:bg-blue-700 transition"
          >
            전송
          </button>
        </div>
      </div>
    </div>
  )
}
