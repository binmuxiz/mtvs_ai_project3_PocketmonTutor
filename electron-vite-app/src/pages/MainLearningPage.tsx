import { useState, useRef, useEffect } from "react";
import { Canvas, useThree, useLoader, useFrame } from "@react-three/fiber";
import { OrbitControls } from "@react-three/drei";
import { GLTFLoader } from "three/examples/jsm/loaders/GLTFLoader";
import { AnimationMixer } from "three";

import axios from 'axios';


const BASE_URL = import.meta.env.VITE_SERVER_API_URL


// function CameraLights() {
//   const { camera } = useThree();

//   return (
//     <group position={camera.position}>
//       {/* <pointLight intensity={1.2} /> */}
//       <ambientLight intensity={3.5} />
//               <directionalLight position={[1, 1, 1]} intensity={4.0} castShadow/>
//               <spotLight position={[0, 8, 10]} angle={0.4} penumbra={0.7} intensity={5.0} castShadow />
//               <ambientLight />
//               <directionalLight position={[5, 5, 5]} />

//     </group>
//   );
// }

function FixedLight() {
  return (
    <>
      <ambientLight intensity={3} />
      {/* <directionalLight
        intensity={4}
        position={[0, 5, 10]}
        target-position={[0, 0, 0]}
        castShadow
      /> */}
      {/* <spotLight
        intensity={5}
        position={[0, 8, 20]}
        angle={0.4}
        penumbra={0.7}
        castShadow
      /> */}
      <directionalLight
        intensity={4}
        position={[0, 0, -20]}
        target-position={[0, 0, 0]}
        castShadow
      />
    </>
  );
}

// 포켓몬 모델
function PokemonModel() {
  const gltf = useLoader(GLTFLoader, "/pokemon-models/Untitled.glb");
  const modelRef = useRef<any>(null);
  const mixerRef = useRef<AnimationMixer | null>(null);

// 자동 회전
  // useFrame((state, delta) => {
  //   if (modelRef.current) {
  //     modelRef.current.rotation.y += delta * 0.5; // 자동 회전 (Y축)
  //   }
  // });
  // return <primitive object={gltf.scene} scale={2.5} position={[0, -1.5, 0]} />;

  useEffect(() => {
    if (gltf.animations && gltf.animations.length > 0 && modelRef.current) {
      mixerRef.current = new AnimationMixer(modelRef.current);
      gltf.animations.forEach((clip) => {
        mixerRef.current?.clipAction(clip).play();
      });
    }
  }, [gltf]);

  useFrame((state, delta) => {
    mixerRef.current?.update(delta);
  });


  return (
    <primitive
      object={gltf.scene}
      ref={modelRef}
      scale={2.5}
      position={[0, 0, 0]}
    />
  );

}

export default function MainLearningPage({ user_id }) {
  const [exp, setExp] = useState(45);
  const [level, setLevel] = useState(5);
  const maxExp = 100;
  const expPercent = (exp / maxExp) * 100;

  const [userInput, setUserInput] = useState("");
  const inputRef = useRef<HTMLInputElement>(null);

  type ChatMessage = {
    sender: "user" | "ai";
    message: string;
  }
  const [chatHistory, setChatHistory] = useState<ChatMessage[]>([]);


  const sendMessage = async () => {
    if (!userInput.trim()) return;

    const userText = userInput;
    setUserInput("");

    // chathistory에 user message 저장
    const newUserMessage: ChatMessage = {
      sender: "user", 
      message: userInput,
    };
    setChatHistory((prev) => [...prev, newUserMessage]);


    try {

    // api 요청 
      const response = await axios.post(`${BASE_URL}/chatbot/`, { 
        user_id: user_id,
        text: userText,
      });

      console.log("response.data = ", response.data)

    // chathistory에 ai message 저장
      const newAiMessage: ChatMessage = {
        sender: "ai",
        message: response.data,
      };
      setChatHistory((prev) => [...prev, newAiMessage]);

      inputRef.current?.focus();

    } catch(error) {
      setChatHistory((prev) => [
        ...prev,
        { sender: "ai", message: "⚠️ 오류가 발생했습니다." },
      ]);
      console.error("Error sending message: ", error);
      }
  }

  return (
    <div className="min-h-screen flex flex-col overflow-hidden bg-gradient-to-b from-[#f0f8ff] to-white font-[\'Noto Sans KR\']">
      {/* 상단 경험치바 */}
      <header className="bg-white shadow-md px-8 py-4">
        <div className="max-w-5xl mx-auto flex items-center space-x-4">
          <div className="bg-yellow-400 text-white rounded-full w-10 h-10 flex items-center justify-center font-bold text-lg">
            P
          </div>
          <div className="font-bold text-base whitespace-nowrap">Lv. {level}</div>
          <div className="flex-1">
            <div className="relative">
              <div className="h-2 bg-gray-300 rounded-full overflow-hidden">
                <div
                  className="h-full bg-green-400 transition-all"
                  style={{ width: `${expPercent}%` }}
                ></div>
              </div>
              <div className="absolute right-0 -top-5 text-xs text-gray-500">경험치: {exp}/{maxExp}</div>
            </div>
          </div>
          <div>
            <div className="w-8 h-8 bg-blue-500 text-white flex items-center justify-center rounded-full">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5.121 17.804A13.937 13.937 0 0112 15c2.485 0 4.779.635 6.879 1.804M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
            </div>
          </div>
        </div>
      </header>

  
      {/* 메인 영역 */}
      {/* <main className="flex-1 flex p-6 overflow-hidden w-full"> */}
      {/* <main className="flex-1 flex p-6 overflow-hidden h-[calc(100vh-8rem)]"> */}
      <main className="flex w-full overflow-hidden">

        {/* 왼쪽 - 3D 모델 영역 */}
        <div className="w-3/5 flex flex-col items-center justify-center">
        {/* <div className="w-3/5 h-[calc(100vh-200px)] flex flex-col items-center justify-center"> */}
        {/* <div className="w-3/5 h-[calc(/100vh-200px)] bg-white rounded-2xl shadow flex flex-col items-center justify-center mt-8"> */}
          <div className="text-xl font-bold mb-2">피카츄</div>
          <div className="w-full h-[calc(100vh-200px)]">
            <Canvas camera={{ position: [0, 1.5, 10], fov: 45 }}>


              {/* <CameraLights /> */}

              <FixedLight />
              <ambientLight intensity={3.5} />
              <directionalLight position={[1, 1, 1]} intensity={4.0} castShadow/>
              <spotLight position={[0, 8, 10]} angle={0.4} penumbra={0.7} intensity={5.0} castShadow />
              <ambientLight />
              <directionalLight position={[5, 5, 5]} />

              <PokemonModel/>

              <OrbitControls enableZoom={false} />

            </Canvas>
          </div>
        </div>

        {/* 오른쪽 - 말풍선 영역 */}
        <div className="w-2/5 p-4">
          <div className="flex flex-col gap-4 overflow-y-auto max-h-[calc(100vh-250px)] pr-2 scroll-smooth">
            {chatHistory.map((chat, index) => (
              <div key={index} className={`flex ${chat.sender === "user" ? "justify-end" : "justify-start"}`}>
                <div
                  className={`
                    relative px-4 py-3 rounded-2xl max-w-[70%] break-words text-sm leading-relaxed shadow-md
                    ${chat.sender === "user" ? "bg-blue-500 text-white" : "bg-white border border-gray-300 text-gray-800"}
                  `}
                >
                  <div
                    className={`
                      absolute w-4 h-4 rotate-45
                      ${chat.sender === "user"
                        ? "bg-blue-500 -bottom-2 right-4"
                        : "bg-white border-l border-t border-gray-300 -top-2 left-4"}
                    `}
                  ></div>
                  {chat.sender === "user" ? "🙋 " : "🤖 "} {chat.message}
                </div>
              </div>
            ))}
          </div>
        </div>



      </main>

      {/* 하단 입력 영역 */}
      <footer className="input-area p-4">
        <div className="max-w-5xl mx-auto w-full">
          <div className="flex items-center bg-gray-100 rounded-full p-1">
            {/* 이미지 업로드 버튼 */}
            <button className="p-2 rounded-full hover:bg-gray-200">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
            </button>
            
            {/* 파일 업로드 버튼 */}
            <button className="p-2 rounded-full hover:bg-gray-200">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15.172 7l-6.586 6.586a2 2 0 102.828 2.828l6.414-6.586a4 4 0 00-5.656-5.656l-6.415 6.585a6 6 0 108.486 8.486L20.5 13" />
              </svg>
            </button>

            {/* 입력창*/}
            <input 
              id="message-input" 
              ref={inputRef} 
              type="text" 
              value={userInput} 
              onChange={(e) => setUserInput(e.target.value)} 
              placeholder="메시지를 입력하세요..." 
              onKeyDown={(e) => e.key === "Enter" && sendMessage()}  
              className="flex-1 bg-transparent border-none focus:outline-none px-4 py-2" />
            
            {/* 음성 버튼 */}
            <button className="p-2 rounded-full hover:bg-gray-200">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" />
              </svg>
            </button>
            
            {/* 전송 버튼 */}
            <button id="send-button" onClick={sendMessage} className="bg-blue-500 text-white rounded-full p-2 ml-1 hover:bg-blue-600">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
              </svg>
            </button>
          </div>
        </div>
      </footer>
    </div>
  );
}
