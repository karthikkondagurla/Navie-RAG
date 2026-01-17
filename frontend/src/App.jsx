import { useState } from 'react'
import axios from 'axios'
import './App.css'

function App() {
  const [messages, setMessages] = useState([
    { role: 'assistant', content: 'Hello! I am your Insurance Policy Assistant. How can I help you today?' }
  ])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [isOpen, setIsOpen] = useState(false)

  const handleSend = async (e) => {
    e.preventDefault()
    if (!input.trim()) return

    const userMessage = { role: 'user', content: input }
    setMessages(prev => [...prev, userMessage])
    setInput('')
    setLoading(true)

    try {
      const response = await axios.post('http://localhost:8000/chat', { message: input })
      const botMessage = { role: 'assistant', content: response.data.response }
      setMessages(prev => [...prev, botMessage])
    } catch (error) {
      console.error('Error:', error)
      setMessages(prev => [...prev, { role: 'assistant', content: 'Sorry, I encountered an error. Ensure the backend is running.' }])
    } finally {
      setLoading(false)
    }
  }

  // Floating Button
  if (!isOpen) {
    return (
      <button className="floating-btn" onClick={() => setIsOpen(true)}>
        💬
      </button>
    )
  }

  // Chat Window
  return (
    <div className="chat-modal">
      <header className="chat-header">
        <h1>🔍 Insurance &nbsp; <span onClick={() => setIsOpen(false)} style={{ cursor: 'pointer', float: 'right' }}>✖</span></h1>
      </header>

      <div className="messages-container">
        {messages.map((msg, index) => (
          <div key={index} className={`message ${msg.role}`}>
            <div className="message-content">
              {msg.content}
            </div>
          </div>
        ))}
        {loading && <div className="message assistant"><div className="message-content">Thinking...</div></div>}
      </div>

      <form className="input-area" onSubmit={handleSend}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask a question..."
          disabled={loading}
          autoFocus
        />
        <button type="submit" disabled={loading}>Send</button>
      </form>
    </div>
  )
}

export default App
