from . import models, schemas
from .db import SessionLocal, engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
import json

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_or_get_by_url(db: Session, url, payload):
    # Try to create record; if unique constraint violation, return existing
    rec = models.QuizRecord(
        url=url,
        title=payload.get("title"),
        summary=payload.get("summary"),
        raw_html=payload.get("raw_html"),
        scraped_text=payload.get("scraped_text"),
        sections=payload.get("sections"),
        key_entities=payload.get("key_entities"),
        quiz=payload.get("quiz"),
        related_topics=payload.get("related_topics")
    )
    db.add(rec)
    try:
        db.commit()
        db.refresh(rec)
        return rec, True
    except IntegrityError:
        db.rollback()
        existing = db.query(models.QuizRecord).filter(models.QuizRecord.url == url).first()
        return existing, False

def list_history(db: Session, limit=100):
    return db.query(models.QuizRecord).order_by(models.QuizRecord.created_at.desc()).limit(limit).all()

def get_quiz(db: Session, qid: int):
    return db.query(models.QuizRecord).filter(models.QuizRecord.id == qid).first()
