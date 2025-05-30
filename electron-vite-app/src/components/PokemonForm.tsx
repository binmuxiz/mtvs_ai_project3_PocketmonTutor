// 왼쪽 입력폼 (성격, 취미, 색상, 분위기, 타입)


import { useState } from 'react'

const BASE_URL = import.meta.env.VITE_SERVER_API_URL


// React에서는 하나의 컴포넌트 함수 안에서 모든 상태 관리(useState)와 로직(handleSubmit) 을 작성해야 하기 때문이야.
function PokemonForm() {

  console.log(BASE_URL)
  
  const [userId, setUserId] = useState("")
  const [name, setName] = useState("")
  const [personality, setPersonality] = useState('')
  const [hobby, setHobby] = useState('')
  const [color, setColor] = useState('')
  const [mood, setMood] = useState('')
  const [type, setType] = useState('')


  const handleSubmit = async () => {

    console.log({ personality, hobby, color, mood, type })

    const userData = {
      user_id: userId,
      name,
      personality,
      hobby,
      color,
      mood,
      type,
    }

// 서버로 전송 
    try {
      // 사용자 등록 
      const userRes = await fetch(`${BASE_URL}/users/`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(userData),
      })

      const result = await userRes.json()

      console.log("✅ ", result.message)
      alert("🎉 사용자 정보가 등록록되었습니다!")

      if (userRes.status === 400) {
        console.warn("⚠️ 이미 등록된 사용자입니다.")
      } else if (!userRes.ok) {
        throw new Error("❌ 사용자 등록 실패")
      }




    } catch (err) {
    console.error("❌ 서버 통신 에러:", err)
    alert("서버와 연결 중 문제가 발생했어요.")
    }
  } 





  // return JSX
  return (
    <div className="bg-white rounded-xl p-6 w-full">
      <h2 className="text-xl font-bold text-gray-800 mb-4">나에게 맞는 포켓몬 찾기</h2>

      {/* 사용자 ID */}
      <div className="mb-4">
        <label className="block text-sm font-medium text-gray-700 mb-1">사용자 ID</label>
        <input
          type="text"
          value={userId}
          onChange={(e) => setUserId(e.target.value)}
          placeholder="예: u001"
          className="w-full px-4 py-2 rounded-lg border border-gray-300 focus:outline-none"
        />
      </div>

      {/* 사용자 이름 */}
      <div className="mb-4">
        <label className="block text-sm font-medium text-gray-700 mb-1">이름</label>
        <input
          type="text"
          value={name}
          onChange={(e) => setName(e.target.value)}
          placeholder="예: 홍길동"
          className="w-full px-4 py-2 rounded-lg border border-gray-300 focus:outline-none"
        />
      </div>


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

      {/* 나의 포켓몬 찾기 */}
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


