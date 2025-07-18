import time
from backend.services import email_service
from backend.agents import classifier, coordinator
from backend.db import crud
from backend.db.database import SessionLocal

def process_emails():
    """
    The main orchestration logic that connects all agents and services.
    """
    print("Checking for new emails...")
    unread_emails = email_service.fetch_unread_emails()

    if not unread_emails:
        print("No new emails found.")
        return

    db = SessionLocal()
    try:
        for email in unread_emails:
            print(f"Processing email from: {email.from_address} with subject: '{email.subject}'")
            
            # Create initial DB record
            db_email_record = crud.create_email_record(db, email)
            
            # 1. Classify Intent
            query = f"{email.subject}\n{email.body}"
            intent = classifier.classify_email_intent(email.subject, email.body)
            print(f"  - Classified Intent: {intent}")
            crud.update_email_record(db, email_id=db_email_record.id, intent=intent, status="CLASSIFIED")

            # 2. Coordinate Response
            reply_body = coordinator.coordinate_response(intent, query)
            print(f"  - Generated Reply.")
            crud.update_email_record(db, email_id=db_email_record.id, response=reply_body)

            # 3. Send Reply
            reply_subject = f"Re: {email.subject}"
            email_service.send_reply(email.from_address, reply_subject, reply_body)
            email_service.mark_as_read(email.uid)
            
            # Update final status in DB
            final_status = "RESPONDED" if intent not in ["OTHER"] else "OTHER_INTENT"
            crud.update_email_record(db, email_id=db_email_record.id, status=final_status)
            
            print(f"  - Reply sent and email marked as read.")
    finally:
        db.close()