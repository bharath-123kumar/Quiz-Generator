import React from 'react';
import QuizCard from './QuizCard';

export default function DetailsModal({ data, onClose }){
  return (
    <div style={{position:'fixed', left:0, top:0, right:0, bottom:0, background:'rgba(0,0,0,0.3)', padding:40}}>
      <div style={{background:'#fff', padding:20, borderRadius:8, maxWidth:1000, margin:'0 auto', maxHeight:'90vh', overflowY:'auto'}}>
        <button onClick={onClose} style={{float:'right'}}>Close</button>
        <h2>{data.title}</h2>
        <p>{data.summary}</p>
        <div style={{display:'grid', gridTemplateColumns:'repeat(auto-fit,minmax(320px,1fr))', gap:12}}>
          {data.quiz.map((q,i)=><QuizCard key={i} question={q} index={i} />)}
        </div>
        <h4>Related Topics</h4>
        <ul>{(data.related_topics||[]).map((t,i)=><li key={i}>{t}</li>)}</ul>
      </div>
    </div>
  )
}
