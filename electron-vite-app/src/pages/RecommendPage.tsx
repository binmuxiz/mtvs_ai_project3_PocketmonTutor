import { useState } from 'react'


import PokemonForm from "../components/PokemonForm";
import PokemonCard from "../components/PokemonCard";


// RecommendPage는 포켓몬 추천을 위한 중간 단계로,

// ✅ 왼쪽에는 입력 폼
// ✅ 오른쪽에는 추천 결과 카드

// 를 보여주고, 추천 완료되면 사용자 확인 후 다음 단계로 넘어가게 하는 UI야.

function RecommendPage({ user_id, onConfirm }) {
  
  const [recommendations, setRecommendations] = useState(null);

  return (
    <div className="flex p-6 gap-6">
      <div className="w-1/2">
        <PokemonForm
          user_id={user_id}
          // 폼 내부에서 추천이 완료되면 onRecommend 콜백을 통해 result를 받아서 상태에 저장
          onRecommend={(result) => setRecommendations(result)}
        />
      </div>


{/* PokemonCard에서 “확인” 버튼을 누르면 onConfirm()이 실행되고, */}
      <div className="w-1/2">
        {recommendations && (
          <PokemonCard data={recommendations} onConfirm={onConfirm} />
        )}
      </div>
    </div>
  );
}

export default RecommendPage
