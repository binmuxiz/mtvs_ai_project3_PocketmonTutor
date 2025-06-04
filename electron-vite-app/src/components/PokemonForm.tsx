import { useState } from 'react';

const BASE_URL = import.meta.env.VITE_SERVER_API_URL;

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

function PokemonForm({ user_id, onRecommend }) {
  const [personality, setPersonality] = useState('');
  const [hobby, setHobby] = useState('');
  const [color, setColor] = useState('');
  const [mood, setMood] = useState('');
  const [selectedTypes, setSelectedTypes] = useState<string[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const toggleType = (type: string) => {
    setSelectedTypes(prev =>
      prev.includes(type) ? prev.filter(t => t !== type) : [...prev, type]
    );
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!user_id) {
      alert("사용자 정보가 없습니다. 먼저 등록해주세요.");
      return;
    }
    setIsLoading(true);
    try {
      const response = await fetch(`${BASE_URL}/pokemon/recommend/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          user_id,
          personality,
          hobby,
          color,
          mood,
          type: selectedTypes.join(", ")
        })
      });
      const recResult = await response.json();
      if (!response.ok) {
        alert("❌ 추천 요청이 실패하였습니다.");
        throw new Error(recResult.detail || "❌ 추천 실패");
      }
      onRecommend(recResult.recommendations);
    } catch (err) {
      console.error("❌ 에러 발생:", err);
      alert("서버 통신 중 문제가 발생했어요.");
    } finally {
      setIsLoading(false);
    }
  };

return (
  <div className="relative rounded-3xl shadow-xl bg-white overflow-hidden p-6 sm:p-8 transition-transform duration-300 hover:-translate-y-1 hover:shadow-2xl">
    <div className="relative z-10">
      <div className="text-center mb-6">
        <h1 className="text-2xl sm:text-3xl font-bold text-gray-800 mb-1">나에게 맞는 포켓몬 찾기</h1>
        <p className="text-sm text-gray-600">당신의 성격과 취향을 바탕으로 최적의 포켓몬 파트너를 찾아드립니다!</p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-5">
        {[
          { label: "성격유형", value: personality, set: setPersonality, placeholder: "예: ENFP, 활발한, 차분한..." },
          { label: "취미나 관심사", value: hobby, set: setHobby, placeholder: "예: 독서, 게임, 요리..." },
          { label: "선호하는 색상", value: color, set: setColor, placeholder: "예: 파란색, 보라색..." },
          { label: "선호하는 분위기", value: mood, set: setMood, placeholder: "예: 귀여운, 활기찬..." }
        ].map(({ label, value, set, placeholder }) => (
          <div key={label}>
            <label className="block text-base font-medium text-gray-700 mb-1">{label}</label>
            <input
              value={value}
              onChange={(e) => set(e.target.value)}
              placeholder={placeholder}
              className="input-field w-full px-4 py-2 rounded-xl bg-gray-50 text-gray-800 outline-none text-sm"
            />
          </div>
        ))}

        <div>
          <label className="block text-base font-medium text-gray-700 mb-2">선호하는 타입 (여러 개 선택 가능)</label>
          <div className="grid grid-cols-3 sm:grid-cols-6 gap-2">
            {types.map((t) => (
              
              <button
                key={t.name}
                type="button"
                onClick={() => toggleType(t.name)}
                className={`type-btn py-1.5 px-2 rounded-lg font-medium flex flex-col items-center justify-center text-xs transition-all
                  ${
                    selectedTypes.includes(t.name)
                      ? "bg-indigo-100 ring-2 ring-indigo-400 text-indigo-700 shadow-md scale-95"
                      : "bg-gray-100 text-gray-800"
                  }`}
              >
                <img src={t.img} alt={t.name} className="w-4 h-4 mb-0.5" />
                <span>{t.name}</span>
              </button>
            ))}
          </div>
        </div>

        <div className="text-center pt-3">
          <button
            type="submit"
            disabled={isLoading}
            className="bg-gradient-to-r from-[#ff6b6b] to-[#ff8e8e] text-white font-bold text-base px-6 py-3 rounded-full shadow-md hover:shadow-lg hover:-translate-y-0.5 transition-all duration-300 disabled:opacity-60"
          >
            {isLoading ? "추천 중..." : "나의 포켓몬 찾기"}
          </button>
        </div>

        
      </form>
    </div>
  </div>
);

}

export default PokemonForm;