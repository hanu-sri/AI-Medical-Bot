import { useState } from "react";
import "./App.css";

function App() {

  const [message, setMessage] = useState("");
  const [response, setResponse] = useState("");

  const sendMessage = async () => {

    const res = await fetch("http://127.0.0.1:8001/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        message: message,
      }),
    });

    const data = await res.json();

    setResponse(data.response);
  };

  return (
    <div className="container">

      <div className="card">

        <h1>🩺 AI Medical Assistant</h1>

        <p className="subtitle">
          Ask health-related questions safely
        </p>

        <div className="chatbox">

          <div className="user">
            <strong>You:</strong> {message}
          </div>

          {response && (
            <div
              className="bot"
              style={{
                marginTop: "20px",
                background: "#1e293b",
                padding: "20px",
                borderRadius: "10px",
                width: "600px",
                color: "white",
                textAlign: "left",
              }}
            >
              <h2>🩺 AI Doctor</h2>
              <p>{response}</p>
            </div>
          )}

        </div>

        <div className="input-area">

          <input
            type="text"
            placeholder="Describe your symptoms..."
            value={message}
            onChange={(e) => setMessage(e.target.value)}
          />

          <button onClick={sendMessage}>
            Send
          </button>

        </div>

        <p className="disclaimer">
          ⚠️ This AI provides educational information only and is not a substitute for professional medical advice.
        </p>

      </div>

    </div>
  );
}

export default App;