const API_BASE = process.env.REACT_APP_API_BASE || "http://localhost:8000/api";

export async function generateQuiz(url) {
  const res = await fetch(`${API_BASE}/generate`, {
    method: "POST",
    headers: {'Content-Type':'application/json'},
    body: JSON.stringify({ url })
  });
  if (!res.ok) throw new Error((await res.json()).detail || 'Error');
  return res.json();
}

export async function getHistory() {
  const res = await fetch(`${API_BASE}/history`);
  if (!res.ok) throw new Error('History fetch failed');
  return res.json();
}

export async function getQuiz(id) {
  const res = await fetch(`${API_BASE}/quizzes/${id}`);
  if (!res.ok) throw new Error('Quiz fetch failed');
  return res.json();
}
