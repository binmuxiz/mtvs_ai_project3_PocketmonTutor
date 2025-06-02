// 왼쪽 입력폼 (성격, 취미, 색상, 분위기, 타입)


import { useState } from 'react'

const BASE_URL = import.meta.env.VITE_SERVER_API_URL

const types = [
  { name: "노말", img: "/types/normal.png" },
  { name: "불꽃", img: "/types/fire.png" },
  { name: "물", img: "/types/water.png" },
  { name: "풀", img: "/types/grass.png" },
  { name: "전기", img: "/types/electricity.png" },
  { name: "얼음", img: "/types/ice.png" },
  { name: "격투", img: "/types/fight.png" },
  { name: "독", img: "/types/poison.png" },
  { name: "땅", img: "/types/ground.png" },
  { name: "비행", img: "/types/flight.png" },
  { name: "에스퍼", img: "/types/esper.png" },
  { name: "벌레", img: "/types/worm.png" },
  { name: "바위", img: "/types/rock.png" },
  { name: "고스트", img: "/types/ghost.png" },
  { name: "드래곤", img: "/types/dragon.png" },
  { name: "악", img: "/types/evil.png" },
  { name: "강철", img: "/types/steel.png" },
  { name: "페어리", img: "/types/fairy.png" }
];


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
    
    const recommendationData = {
      user_id: userId,
      personality,
      hobby,
      color,
      mood,
      type,
    };


// 서버로 전송 
    try {
      // 사용자 등록 
      const userRes = await fetch(`${BASE_URL}/users/`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(userData),
      })

      const result = await userRes.json()

// 이건 not found아닌가 ?
      if (userRes.status === 400) {
        console.warn("⚠️ 이미 등록된 사용자입니다.")
        alert("이미 등록된 사용자입니다.");
        return;

      } else if (!userRes.ok) {
        throw new Error(result.detail || "❌ 사용자 등록 실패")
      }




// 사용자 등록 성공 시 추천 정보 요청
      const recRes = await fetch(`${BASE_URL}/recommend/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(recommendationData),
      });

      const recResult = await recRes.json();

      if (!recRes.ok) {
        throw new Error(recResult.detail || "❌ 추천 저장 실패");
      }

      console.log("✅ 추천 완료:", recResult.message);
      alert("🎉 포켓몬 추천이 완료되었습니다!");

    } catch (err) {
      console.error("❌ 에러 발생:", err);
      alert("서버 통신 중 문제가 발생했어요.");
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


      {/* 성격 */}
      <div className="mb-4">
        <label className="block text-sm font-medium text-gray-700 mb-1">성격 유형</label>
        <input
          type="text"
          value={personality}
          onChange={(e) => setPersonality(e.target.value)}
          placeholder="예: 창의적, 논리적, 활발함 등"
          className="w-full px-4 py-2 rounded-lg border border-gray-300 focus:outline-none"
        />
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

      {/* 선호 색상 */}
      <div className="mb-4">
        <label className="block text-sm font-medium text-gray-700 mb-1">선호하는 색상</label>
        <input
          type="text"
          value={color}
          onChange={(e) => setColor(e.target.value)}
          placeholder="예: 파란색, 노란색 등"
          className="w-full px-4 py-2 rounded-lg border border-gray-300 focus:outline-none"
        />
      </div>


      {/* 분위기 */}
      <div className="mb-4">
        <label className="block text-sm font-medium text-gray-700 mb-1">선호하는 분위기</label>
        <input
          type="text"
          value={mood}
          onChange={(e) => setMood(e.target.value)}
          placeholder="예: 귀여운, 강렬한, 차분한 등"
          className="w-full px-4 py-2 rounded-lg border border-gray-300 focus:outline-none"
        />
      </div>

      <div className="mb-6">
        <label className="block text-sm font-medium text-gray-700 mb-2">선호하는 타입(속성)</label>
        <div className="grid grid-cols-6 gap-2">
          {types.map((t) => (
            <button
              key={t.name}
              onClick={() => setType(t.name)}
              className={`flex flex-col items-center p-2 rounded border 
                ${type === t.name ? 'bg-indigo-100 border-indigo-500' : 'bg-white border-gray-300'} 
                hover:shadow`}
            >
              <img src={t.img} alt={t.name} className="w-6 h-6 mb-1" />
              <span className="text-xs">{t.name}</span>
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


