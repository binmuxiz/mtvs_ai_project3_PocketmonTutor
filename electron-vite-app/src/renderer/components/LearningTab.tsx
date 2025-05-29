// 학습 관리 탭 콘텐츠 

// src/renderer/components/LearningTab.tsx
import React, { useState } from 'react'

interface Task {
  title: string
  date: string
  done: boolean
}

export default function LearningTab() {
  const [tasks, setTasks] = useState<Task[]>([
    { title: 'RAG 복습', date: '2023년 5월 20일', done: false },
    { title: 'LLM 프로젝트 발표 준비', date: '2023년 5월 25일', done: false },
    { title: '파이썬 기초 복습', date: '2023년 5월 15일 (완료)', done: true },
  ])

  return (
    <div className="space-y-6">
      <div className="bg-white rounded-lg shadow-md p-6">
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-2xl font-bold">학습 일정</h2>
          <button className="bg-blue-600 text-white px-3 py-1.5 rounded-md hover:bg-blue-700 transition text-sm flex items-center">
            새 학습 추가
          </button>
        </div>
        <div className="space-y-4">
          {tasks.map((task, idx) => (
            <div key={idx} className={`border border-gray-200 rounded-lg p-4 flex justify-between items-center ${task.done ? 'bg-gray-50' : ''}`}>
              <div>
                <h3 className={`font-medium ${task.done ? 'line-through text-gray-500' : ''}`}>{task.title}</h3>
                <p className="text-sm text-gray-500">{task.date}</p>
              </div>
              <div className="flex space-x-2">
                {!task.done && (
                  <button
                    onClick={() => {
                      const updated = [...tasks]
                      updated[idx].done = true
                      setTasks(updated)
                    }}
                    className="bg-green-100 text-green-800 px-3 py-1 rounded-md text-sm hover:bg-green-200 transition"
                  >
                    완료
                  </button>
                )}
                <button className="bg-gray-100 text-gray-800 px-3 py-1 rounded-md text-sm hover:bg-gray-200 transition">수정</button>
                <button
                  onClick={() => setTasks(tasks.filter((_, i) => i !== idx))}
                  className="bg-red-100 text-red-800 px-3 py-1 rounded-md text-sm hover:bg-red-200 transition"
                >
                  삭제
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-2xl font-bold mb-6">학습 통계</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-blue-50 rounded-lg p-4">
            <h3 className="text-lg font-medium text-blue-800 mb-2">완료한 학습</h3>
            <div className="flex items-end">
              <span className="text-3xl font-bold text-blue-600">{tasks.filter(t => t.done).length}</span>
              <span className="text-sm text-blue-600 ml-2 mb-1">개</span>
            </div>
          </div>
          <div className="bg-purple-50 rounded-lg p-4">
            <h3 className="text-lg font-medium text-purple-800 mb-2">획득한 경험치</h3>
            <div className="flex items-end">
              <span className="text-3xl font-bold text-purple-600">{tasks.filter(t => t.done).length * 10}</span>
              <span className="text-sm text-purple-600 ml-2 mb-1">포인트</span>
            </div>
          </div>
          <div className="bg-green-50 rounded-lg p-4">
            <h3 className="text-lg font-medium text-green-800 mb-2">연속 학습일</h3>
            <div className="flex items-end">
              <span className="text-3xl font-bold text-green-600">7</span>
              <span className="text-sm text-green-600 ml-2 mb-1">일</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
