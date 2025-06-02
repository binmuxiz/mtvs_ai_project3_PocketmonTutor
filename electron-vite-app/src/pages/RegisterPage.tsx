import { useState } from 'react'

const BASE_URL = import.meta.env.VITE_SERVER_API_URL


function RegisterPage({ onRegister }) {

  const [user_id, setUserId] = useState("");
  const [name, setName] = useState("");

  const handleRegister = async () => {
    if (!user_id || !name) return alert("ID와 이름을 모두 입력해주세요.");

    console.log({ user_id, name })

    const userData = {
      user_id,
      name
    }


    try {
      // 사용자 등록 요청
      const response = await fetch(`${BASE_URL}/users/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(userData),
      })

      if (response.status === 400) {
        console.warn("⚠️ 이미 등록된 사용자입니다.")
        alert("이미 등록된 사용자입니다.");
        return;

      } else if (!response.ok) {
        throw new Error("❌ 사용자 등록 실패")
      }

      onRegister(user_id);  // 상태 전달
      
    } catch(err) {
      console.error("❌ 에러 발생:", err);
      alert("서버 통신 중 문제가 발생했어요.");
    }
  };

  return (
    <div className="p-8 max-w-sm mx-auto">
      <h1 className="text-xl font-bold mb-4">사용자 등록</h1>
      <input placeholder="사용자 ID" value={user_id} onChange={(e) => setUserId(e.target.value)} className="mb-2 w-full border p-2" />
      <input placeholder="이름" value={name} onChange={(e) => setName(e.target.value)} className="mb-4 w-full border p-2" />

      <button onClick={handleRegister} className="bg-blue-600 text-white px-4 py-2 rounded">가입하기</button>
    </div>
  );
}

export default RegisterPage 