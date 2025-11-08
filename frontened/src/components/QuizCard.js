import React, { useState } from 'react';

export default function QuizCard({ question, index }) {
  const [selected, setSelected] = useState(null);
  const [showAnswer, setShowAnswer] = useState(false);

  return (
    <div style={{border:'1px solid #ddd', padding:12, borderRadius:8}}>
      <div style={{fontSize:14, color:'#333'}}><b>Q{index+1}.</b> {question.question}</div>
      <div style={{marginTop:8}}>
        {question.options.map((opt, i)=> (
          <div key={i} style={{marginBottom:6}}>
            <label style={{display:'flex', gap:8, alignItems:'center'}}>
              <input type="radio" name={`q${index}`} onChange={()=>setSelected(opt)} />
              <span>{opt}</span>
            </label>
          </div>
        ))}
      </div>
      <div style={{marginTop:6, display:'flex', justifyContent:'space-between', alignItems:'center'}}>
        <small>{question.difficulty}</small>
        <div>
          <button onClick={()=>setShowAnswer(s=>!s)} style={{marginRight:8}}>Show Answer</button>
        </div>
      </div>
      {showAnswer && (
        <div style={{marginTop:8, background:'#fafafa', padding:8, borderRadius:6}}>
          <div><b>Answer:</b> {question.answer}</div>
          <div><b>Explanation:</b> {question.explanation}</div>
        </div>
      )}
    </div>
  );
}
