// 왼쪽 입력폼 (성격, 취미, 색상, 분위기, 타입)

import { useState } from 'react'

function PokemonForm() {
  const [personality, setPersonality] = useState('')
  const [hobby, setHobby] = useState('')
  const [color, setColor] = useState('')
  const [mood, setMood] = useState('')
  const [type, setType] = useState('')

  const handleSubmit = () => {
    // TODO: 추천 API 연결
    console.log({ personality, hobby, color, mood, type })
  }

  return (
    <div className="bg-white rounded-xl p-6 w-full">
      <h2 className="text-xl font-bold text-gray-800 mb-4">나에게 맞는 포켓몬 찾기</h2>

      {/* 성격 유형 */}
      <div className="mb-4">
        <label className="block text-sm font-medium text-gray-700 mb-1">성격 유형</label>
        <select
          className="w-full px-4 py-2 rounded-lg border border-gray-300 focus:outline-none"
          value={personality}
          onChange={(e) => setPersonality(e.target.value)}
        >
          <option value="">선택해주세요</option>
          <option value="extrovert">외향적</option>
          <option value="introvert">내향적</option>
          <option value="creative">창의적</option>
          <option value="practical">실용적</option>
          <option value="analytical">분석적</option>
        </select>
      </div>

      {/* 취미 */}
      <div className="mb-4">
        <label className="block text-sm font-medium text-gray-700 mb-1">취미나 관심사</label>
        <input
          type="text"
          value={hobby}
          onChange={(e) => setHobby(e.target.value)}
          placeholder="예: 스포츠, 음악 감상, 독서, 여행 등"
          className="w-full px-4 py-2 rounded-lg border border-gray-300 focus:outline-none"
        />
      </div>

      {/* 색상 선택 */}
      <div className="mb-4">
        <label className="block text-sm font-medium text-gray-700 mb-1">선호하는 색상</label>
        <div className="flex gap-2">
          {["red", "blue", "green", "yellow", "purple"].map((c) => (
            <button
              key={c}
              onClick={() => setColor(c)}
              className={`w-8 h-8 rounded-full border-2 ${color === c ? 'border-gray-800' : 'border-transparent'} bg-${c}-500`}
            />
          ))}
        </div>
      </div>

      {/* 분위기 */}
      <div className="mb-4">
        <label className="block text-sm font-medium text-gray-700 mb-1">선호하는 분위기</label>
        <div className="grid grid-cols-2 gap-2">
          {["귀여운", "카리스마 있는", "강렬한", "신비로운"].map((m) => (
            <button
              key={m}
              onClick={() => setMood(m)}
              className={`py-2 px-3 rounded-lg ${mood === m ? 'bg-indigo-100 text-indigo-700' : 'bg-gray-100'}`}
            >
              {m}
            </button>
          ))}
        </div>
      </div>

      {/* 타입 */}
      <div className="mb-6">
        <label className="block text-sm font-medium text-gray-700 mb-1">선호하는 타입(속성)</label>
        <div className="grid grid-cols-3 gap-2">
          {["불", "물", "풀", "전기", "에스퍼", "노말"].map((t) => (
            <button
              key={t}
              onClick={() => setType(t)}
              className={`py-2 px-2 rounded-lg text-sm font-medium ${type === t ? 'bg-indigo-100 text-indigo-700' : 'bg-gray-100'}`}
            >
              {t}
            </button>
          ))}
        </div>
      </div>

      <button
        onClick={handleSubmit}
        className="w-full py-3 px-6 bg-indigo-600 text-white font-medium rounded-lg hover:bg-indigo-700"
      >
        나의 포켓몬 찾기
      </button>
    </div>
  )
}

export default PokemonForm
