# WikiQuiz — Generate quizzes from Wikipedia articles

## Overview
FastAPI backend scrapes a Wikipedia article and generates a quiz using LangChain + LLM. React frontend provides two tabs: Generate Quiz and History.

## Requirements
- Python 3.10+
- Node 16+
- PostgreSQL
- (Optional) OpenAI API Key or configured LangChain provider

## Backend setup
1. Create `.env` in backend/:
   DATABASE_URL=postgresql://user:pass@localhost:5432/wqdb
   LLM_PROVIDER=openai
   OPENAI_API_KEY=sk-...
   MAX_QUESTIONS=7

2. Install:
   cd backend
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt

3. Start app:
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

## Frontend setup
1. cd frontend
2. npm install
3. Create `.env` with REACT_APP_API_BASE=http://localhost:8000/api
4. npm start

## Endpoints
POST /api/generate
  Body: { "url": "https://en.wikipedia.org/wiki/Alan_Turing" }
GET /api/history
GET /api/quizzes/{id}

## Sample data
See sample_data/ folder for tested URLs and output JSON.

## Prompt templates
Stored in backend/app/prompts/quiz_prompt.txt and related_prompt.txt.

## Notes
- Caching: the database uses a unique constraint on url; repeated requests return stored quiz.
- To change the LLM provider (e.g., Gemini) wire in the LangChain adapter in llm_client.get_llm().
