// src/renderer/App.tsx
import React, { useState } from 'react'
import Tabs from './components/Tabs'
import ProfileTab from './components/ProfileTab'
import ChatTab from './components/ChatTab'
import LearningTab from './components/LearningTab'
import Footer from './components/Footer'

export default function App() {
  const [activeTab, setActiveTab] = useState<'profile' | 'chat' | 'learning'>('profile')

  return (
    <div className="flex flex-col min-h-screen bg-gray-100">
      <main className="flex-grow container mx-auto p-4">
        <Tabs activeTab={activeTab} setActiveTab={setActiveTab} />
        {activeTab === 'profile' && <ProfileTab />}
        {activeTab === 'chat' && <ChatTab />}
        {activeTab === 'learning' && <LearningTab />}
      </main>
      <Footer />
    </div>
  )
}
