import React, { useState, useEffect } from "react";
import QuizCard from "./components/QuizCard";
import HistoryTable from "./components/HistoryTable";

function App() {
  const [activeTab, setActiveTab] = useState("generate");
  const [url, setUrl] = useState("");
  const [quiz, setQuiz] = useState(null);
  const [history, setHistory] = useState([]);

  const generateQuiz = async () => {
    const res = await fetch("http://127.0.0.1:8000/generate_quiz", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url }),
    });
    const data = await res.json();
    setQuiz(data);
  };

  const loadHistory = async () => {
    const res = await fetch("http://127.0.0.1:8000/history");
    const data = await res.json();
    setHistory(data);
  };

  useEffect(() => {
    loadHistory();
  }, []);

  return (
    <div style={{ padding: "2rem", fontFamily: "sans-serif" }}>
      <div>
        <button onClick={() => setActiveTab("generate")}>Generate Quiz</button>
        <button onClick={() => setActiveTab("history")}>Past Quizzes</button>
      </div>

      {activeTab === "generate" && (
        <div>
          <h3>Generate from Wikipedia</h3>
          <input
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            placeholder="Enter Wikipedia URL"
            style={{ width: "60%", marginRight: "1rem" }}
          />
          <button onClick={generateQuiz}>Generate</button>

          {quiz && (
            <div style={{ marginTop: "1rem" }}>
              <h2>{quiz.title}</h2>
              <p>{quiz.summary}</p>
              {quiz.quiz.map((q, i) => (
                <QuizCard key={i} q={q} i={i} />
              ))}
              <p>
                <b>Related Topics:</b> {quiz.related_topics.join(", ")}
              </p>
            </div>
          )}
        </div>
      )}

      {activeTab === "history" && <HistoryTable history={history} />}
    </div>
  );
}

export default App;
