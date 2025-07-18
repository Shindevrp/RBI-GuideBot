from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from .database import Base

class ProcessedEmail(Base):
    __tablename__ = "processed_emails"

    id = Column(Integer, primary_key=True, index=True)
    received_at = Column(DateTime(timezone=True), server_default=func.now())
    from_address = Column(String, index=True)
    subject = Column(String)
    body = Column(Text)
    classified_intent = Column(String, nullable=True)
    response_body = Column(Text, nullable=True)
    status = Column(String, default="RECEIVED") # e.g., RECEIVED, CLASSIFIED, RESPONDED, FAILED, OTHER_INTENT
    processed_at = Column(DateTime(timezone=True), onupdate=func.now())