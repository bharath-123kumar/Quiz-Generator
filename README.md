
https://sdmntprkoreacentral.oaiusercontent.com/files/00000000-d7c4-7206-8490-0dd2f51278c4/raw?se=2025-11-08T19%3A41%3A48Z&sp=r&sv=2024-08-04&sr=b&scid=abbc76a5-f329-41e3-8bb0-b9a01b2443ba&skoid=9063adf3-a524-4acf-b70a-8731b33f2f50&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2025-11-08T00%3A34%3A47Z&ske=2025-11-09T00%3A34%3A47Z&sks=b&skv=2024-08-04&sig=NMriIU%2BdZu%2BAipyFJvkfKrQ3k9BMn9123xs%2Bh2oVlH0%3D


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
