import React, { useState } from "react";
import { generateQuiz } from "../api";
import QuizCard from "./QuizCard";

export default function GenerateTab() {
  const [url, setUrl] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  async function onGenerate() {
    setLoading(true); setError(""); setResult(null);
    try {
      const data = await generateQuiz(url);
      setResult(data);
    } catch (e) {
      setError(e.message);
    } finally { setLoading(false); }
  }

  return (
    <div>
      <div style={{display:'flex', gap:8}}>
        <input style={{flex:1}} placeholder="Paste Wikipedia article URL" value={url} onChange={e=>setUrl(e.target.value)} />
        <button onClick={onGenerate} disabled={loading}>Generate Quiz</button>
      </div>
      {error && <div style={{color:'red'}}>{error}</div>}
      {loading && <div>Generating…</div>}
      {result && (
        <div>
          <h2>{result.title}</h2>
          <p>{result.summary}</p>
          <div style={{display:'grid', gridTemplateColumns:'repeat(auto-fit,minmax(320px,1fr))', gap:12}}>
            {result.quiz.map((q, i)=> <QuizCard key={i} question={q} index={i} />)}
          </div>
          <h4>Suggested topics</h4>
          <ul>{(result.related_topics||[]).map((t,idx)=><li key={idx}>{t}</li>)}</ul>
        </div>
      )}
    </div>
  )
}
