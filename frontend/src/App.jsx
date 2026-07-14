import { useState } from 'react'
import axios from 'axios'
import './App.css'

function App() {
  const [file, setFile] = useState(null)
  const [uploadStatus, setUploadStatus] = useState('idle')
  const [chatHistory, setChatHistory] = useState([])
  const [query, setQuery] = useState('')
  const [isTyping, setIsTyping] = useState(false)


  const API_URL = "http://127.0.0.1:8000"


  const handleFileChange = (e) => {
    if (e.target.files[0]) {
      setFile(e.target.files[0])
      setUploadStatus('idle')
    }
  }


  const handleUpload = async () => {
    if (!file) return;

    setUploadStatus('uploading')
    const formData = new FormData()
    formData.append('file', file)

      try {
        const response = await axios.post(`${API_URL}/upload`, formData, {
          headers: { 'Content-Type': 'multipart/form-data' }
        })
        console.log(response.data)
        setUploadStatus('success')
      } catch (error) {
        console.error("Upload failed", error)
        setUploadStatus('error')
      }
  }


  const handleChat = async (e) => {
    e.preventDefault()
    if (!query.trim()) return


      const userMessage = { role: 'user', text: query }
      setChatHistory((prev) => [...prev, userMessage])
      setQuery('')
      setIsTyping(true)

      try {
        const response = await axios.post(`${API_URL}/chat`, { query: userMessage.text })


        setChatHistory((prev) => [...prev, { role: 'ai', text: response.data.answer }])
      } catch (error) {
        console.error("Chat failed", error)
        setChatHistory((prev) => [...prev, { role: 'error', text: "Failed to reach the server. Make sure FastAPI is running." }])
      } finally {
        setIsTyping(false)
      }
  }

  return (
    <div className="app-container">
    <header>
    <h1>📄 RAG Document Analyzer</h1>
    <p>Upload a PDF and ask questions about its contents.</p>
    </header>


    <section className="upload-section">
    <div className="file-input-wrapper">
    <input
    type="file"
    accept=".pdf"
    onChange={handleFileChange}
    disabled={uploadStatus === 'uploading'}
    />
    <button
    onClick={handleUpload}
    disabled={!file || uploadStatus === 'uploading'}
    className="upload-btn"
    >
    {uploadStatus === 'uploading' ? 'Processing...' : 'Upload & Process'}
    </button>
    </div>

    {uploadStatus === 'success' && (
      <div className="status success">✅ Document embedded into ChromaDB! You can now chat.</div>
    )}
    {uploadStatus === 'error' && (
      <div className="status error">❌ Upload failed. Check the FastAPI console.</div>
    )}
    </section>


    {uploadStatus === 'success' && (
      <section className="chat-section">
      <div className="chat-window">
      {chatHistory.length === 0 ? (
        <p className="placeholder">Ask a question to get started...</p>
      ) : (
        chatHistory.map((msg, index) => (
          <div key={index} className={`message ${msg.role}`}>
          <strong>{msg.role === 'user' ? 'You:' : 'AI:'}</strong> {msg.text}
          </div>
        ))
      )}
      {isTyping && <div className="message ai"><strong>AI:</strong> <em>Thinking...</em></div>}
      </div>

      <form onSubmit={handleChat} className="chat-input-form">
      <input
      type="text"
      value={query}
      onChange={(e) => setQuery(e.target.value)}
      placeholder="e.g., What is the main conclusion of the report?"
      disabled={isTyping}
      />
      <button type="submit" disabled={isTyping || !query.trim()}>Send</button>
      </form>
      </section>
    )}
    </div>
  )
}

export default App
