import { useState, useEffect, useRef } from "react"
import axios from "axios"
import "./App.css"
import { motion } from "framer-motion"
import CharacterSelection from "./CharacterSelection" // Import CharacterSelection component
import ChatArea from "./ChatArea" // Import ChatArea component
import InputBar from "./InputBar" // Import InputBar component

const API_URL = "http://127.0.0.1:8000"


function App() {
  const [sessionId, setSessionId] = useState("")
  const [character, setCharacter] = useState("Iron Man")
  const [userMessage, setUserMessage] = useState("")
  const [chat, setChat] = useState([])
  const [loading, setLoading] = useState(false)
  const chatEndRef = useRef(null)

  useEffect(() => {
    const fetchSession = async () => {
      const response = await axios.get(`${API_URL}/new_session`)
      setSessionId(response.data.session_id)
    }
    fetchSession()
  }, [])

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }, [chatEndRef]) // Fixed dependency

  const sendMessage = async () => {
    if (!userMessage.trim()) return
    setLoading(true)

    const newChat = [...chat, { sender: "User", text: userMessage }]
    setChat(newChat)
    setUserMessage("")

    try {
      const response = await axios.post(`${API_URL}/chat`, {
        session_id: sessionId,
        character,
        user_message: userMessage,
      })

      newChat.push({ sender: character, text: response.data.response })
      setChat(newChat)
    } catch (error) {
      newChat.push({ sender: "System", text: "Error fetching response." })
      setChat(newChat)
    }
    setLoading(false)
  }

  return (
    <div className="min-h-screen min-w-screen w-full bg-gradient-to-b from-gray-900 to-gray-800 text-white p-5 flex flex-col items-center justify-center">
      <motion.h1
        initial={{ opacity: 0, y: -50 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="text-4xl font-bold mb-8 text-yellow-400 drop-shadow-glow"
      >
        🎭 AI Movie Character Chat
      </motion.h1>

      <motion.div
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.5 }}
        className="w-full max-w-2xl bg-gray-800 rounded-xl shadow-2xl overflow-hidden"
      >
        <CharacterSelection character={character} setCharacter={setCharacter} />
        <ChatArea chat={chat} character={character} chatEndRef={chatEndRef} />
        <InputBar
          userMessage={userMessage}
          setUserMessage={setUserMessage}
          sendMessage={sendMessage}
          loading={loading}
        />
      </motion.div>
    </div>
  )
}

export default App

