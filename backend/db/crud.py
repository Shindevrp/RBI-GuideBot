from sqlalchemy.orm import Session
from . import models
from backend.services.email_service import Email as EmailData

def create_email_record(db: Session, email: EmailData) -> models.ProcessedEmail:
    db_email = models.ProcessedEmail(
        from_address=email.from_address,
        subject=email.subject,
        body=email.body
    )
    db.add(db_email)
    db.commit()
    db.refresh(db_email)
    return db_email

def update_email_record(db: Session, email_id: int, intent: str = None, response: str = None, status: str = None):
    db_email = db.query(models.ProcessedEmail).filter(models.ProcessedEmail.id == email_id).first()
    if db_email:
        if intent:
            db_email.classified_intent = intent
        if response:
            db_email.response_body = response
        if status:
            db_email.status = status
        db.commit()
        db.refresh(db_email)
    return db_email