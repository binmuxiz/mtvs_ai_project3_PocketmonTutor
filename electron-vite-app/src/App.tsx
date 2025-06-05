import { useState } from "react";
import RegisterPage from "./pages/RegisterPage";
import MainLearningPage from "./pages/MainLearningPage";
import PokemonForm from "./components/PokemonForm";
import PokemonCard from "./components/PokemonCard";

function App() {
  const [step, setStep] = useState<"register" | "form" | "recommend" | "main">("register");
  const [user_id, setUserId] = useState("");
  const [pokemonData, setPokemonData] = useState(null);
  const [model_url, setModelUrl] = useState("");

  return (
    <>
      {step === "register" && (
        <RegisterPage
          onRegister={(user_id) => {
            setUserId(user_id);
            setStep("form");
          }}

          onLogin={(pokemon) => {
            setUserId(pokemon.user_id);
            setPokemonData(pokemon);
            setModelUrl(pokemon.model_file_path); // model_url도 세팅
            setStep("main");
          }}
        />
      )}

      {step === "form" && (
          <div className="p-6 max-w-4xl mx-auto">

            <PokemonForm
              user_id={user_id}
              onRecommend={(pokemonData) => {
                setPokemonData(pokemonData);
                setStep("recommend");
              }}
            />
          </div>
      )}

{/* 포켓몬 추천 결과 카드 */}
      {step === "recommend" && pokemonData && (
        // <div className="p-6 max-w-4xl mx-auto">
        <div className="min-h-screen flex items-center justify-center bg-gradient-to-b from-orange-400 to-orange-500">

          <PokemonCard
            user_id={user_id}
            pokemonData={pokemonData}

            onConfirm={(model_url, ) => {
              setModelUrl(model_url); 
              setStep("main");
            }}
            
            onClose={() => setStep("form")}   // ← X 버튼 누르면 입력화면으로
          />
        </div>
      )}

      {step === "main" && 
          <MainLearningPage 
            user_id={user_id} 
            model_url={model_url} 
            pokemonData={pokemonData}
      />}
    </>
  );
}

export default App;