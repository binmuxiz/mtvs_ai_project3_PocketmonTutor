// 학습 추가 모달 

import React from 'react'

type Props = {
  isOpen: boolean
  onClose: () => void
  onConfirm: () => void
}

export default function Modal({ isOpen, onClose, onConfirm }: Props) {
  if (!isOpen) return null

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-lg shadow-xl p-6 w-full max-w-md">
        <div className="flex justify-between items-center mb-4">
          <h3 className="text-xl font-bold">새 학습 추가</h3>
          <button onClick={onClose} className="text-gray-500 hover:text-gray-700 text-xl">×</button>
        </div>
        <form>
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-1">학습 제목</label>
            <input type="text" className="w-full px-3 py-2 border border-gray-300 rounded-md" placeholder="예: RAG 복습" />
          </div>
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-1">날짜</label>
            <input type="date" className="w-full px-3 py-2 border border-gray-300 rounded-md" />
          </div>
          <div className="mb-4">
            <label className="block text-sm font-medium text-gray-700 mb-1">메모 (선택사항)</label>
            <textarea className="w-full px-3 py-2 border border-gray-300 rounded-md" rows={3}></textarea>
          </div>
          <div className="flex justify-end">
            <button type="button" onClick={onClose} className="bg-gray-200 text-gray-800 px-4 py-2 rounded-md mr-2 hover:bg-gray-300 transition">취소</button>
            <button type="button" onClick={onConfirm} className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 transition">추가</button>
          </div>
        </form>
      </div>
    </div>
  )
}
