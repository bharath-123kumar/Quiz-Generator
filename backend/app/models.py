from sqlalchemy import Column, Integer, String, Text, DateTime, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from .db import Base

class QuizRecord(Base):
    __tablename__ = "quiz_records"
    id = Column(Integer, primary_key=True, index=True)
    url = Column(String(1000), nullable=False)
    title = Column(String(500))
    summary = Column(Text)
    raw_html = Column(Text)
    scraped_text = Column(Text)
    sections = Column(JSONB)  # list of sections
    key_entities = Column(JSONB)  # dict for people/orgs/locations
    quiz = Column(JSONB)  # list of question dicts
    related_topics = Column(JSONB)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (UniqueConstraint('url', name='uq_url'),)
