from fastapi import FastAPI, HTTPException, Depends
from .schemas import GenerateIn, QuizRecordOut
from . import scraper, llm_client, crud
from .db import SessionLocal
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse

app = FastAPI(title="WikiQuiz Generator")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/api/generate", response_model=QuizRecordOut)
async def generate_quiz(payload: GenerateIn, db: Session = Depends(get_db)):
    url = payload.url
    # simple validation: must be wikipedia.org
    from urllib.parse import urlparse
    parsed = urlparse(url)
    if "wikipedia.org" not in parsed.netloc:
        raise HTTPException(status_code=400, detail="Only wikipedia.org URLs are supported.")

    try:
        raw_html = scraper.fetch_html(url)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Error fetching URL: {str(e)}")

    parsed_data = scraper.parse_wikipedia(raw_html)
    entities = scraper.extract_entities(parsed_data.get("scraped_text",""))

    # LLM calls (generate quiz and related topics)
    try:
        quiz_out = llm_client.generate_quiz(parsed_data["scraped_text"], parsed_data["title"])
    except Exception as e:
        # proceed but record error
        quiz_out = {"quiz": [], "error": str(e)}

    try:
        related = llm_client.generate_related(parsed_data["scraped_text"], parsed_data["title"])
    except Exception:
        related = []

    payload_db = {
        "title": parsed_data.get("title"),
        "summary": parsed_data.get("summary"),
        "raw_html": raw_html,
        "scraped_text": parsed_data.get("scraped_text"),
        "sections": parsed_data.get("sections"),
        "key_entities": entities,
        "quiz": quiz_out.get("quiz", []),
        "related_topics": related
    }

    rec, created = crud.create_or_get_by_url(db, url, payload_db)
    # return existing or created record
    return rec

@app.get("/api/history")
def history(db: Session = Depends(get_db)):
    items = crud.list_history(db)
    return [{"id": r.id, "url": r.url, "title": r.title, "created_at": r.created_at} for r in items]

@app.get("/api/quizzes/{qid}", response_model=QuizRecordOut)
def quiz_detail(qid: int, db: Session = Depends(get_db)):
    rec = crud.get_quiz(db, qid)
    if not rec:
        raise HTTPException(status_code=404, detail="Not found")
    return rec
