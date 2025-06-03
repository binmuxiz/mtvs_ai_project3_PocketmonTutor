import PokemonTabs from './components/PokemonTabs';
import { useState } from "react";
import RegisterPage from "./pages/RegisterPage";
import MainLearningPage from "./pages/MainLearningPage";
import PokemonForm from "./components/PokemonForm";
import PokemonCard from "./components/PokemonCard";

function App() {
  const [step, setStep] = useState<"register" | "form" | "recommend" | "main">("register");
  const [user_id, setUserId] = useState("");
  const [recommendation, setRecommendation] = useState(null);

  return (
    <>
      {step === "register" && (
        <RegisterPage
          onRegister={(user_id) => {
            setUserId(user_id);
            setStep("form");
          }}
        />
      )}

      {step === "form" && (
          <div className="p-6 max-w-4xl mx-auto">

            <PokemonForm
              user_id={user_id}
              onRecommend={(result) => {
                setRecommendation(result);
                setStep("recommend");
              }}
            />
          </div>
      )}

      {step === "recommend" && recommendation && (
        // <div className="p-6 max-w-4xl mx-auto">
        <div className="min-h-screen flex items-center justify-center bg-gradient-to-b from-orange-400 to-orange-500">

          <PokemonCard
            data={recommendation}
            onConfirm={() => setStep("main")}
            onClose={() => setStep("form")}   // ← X 버튼 누르면 입력화면으로
          />
        </div>
      )}

      {step === "main" && <MainLearningPage userId={user_id} />}
    </>
  );
}

export default App;