import PokemonTabs from './components/PokemonTabs'

import { useState } from "react";
import RegisterPage from "./pages/RegisterPage";
import RecommendPage from "./pages/RecommendPage";
import MainLearningPage from "./pages/MainLearningPage";

function App() {
  const [step, setStep] = useState<"register" | "recommend" | "main">("register");
  const [user_id, setUserId] = useState("");

  return (
    <>
      {step === "register" && (
        <RegisterPage
          onRegister={(user_id) => { 
            setUserId(user_id);
            setStep("recommend");
          }}
        />
      )}
      {step === "recommend" && (
        <RecommendPage
          user_id={user_id}

          // onConfirm은 "추천 완료 후 다음 단계로 넘어가자!" 하는 콜백 함수
          onConfirm={() => setStep("main")}
        />
      )}

      {/* {step === "main" && <MainLearningPage userId={userId} />} */}
    </>
  );
}

export default App;

