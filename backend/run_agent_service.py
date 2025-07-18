import time
from backend.core.orchestrator import process_emails
from backend.db import models
from backend.db.database import engine

def initialize_database():
    """Creates database tables."""
    print("Initializing database...")
    models.Base.metadata.create_all(bind=engine)
    print("Database initialized.")

def main():
    """
    Runs the email processing loop continuously.
    """
    initialize_database()
    print("Starting Agentic Email Service...")
    while True:
        process_emails()
        print("Sleeping for 60 seconds...")
        time.sleep(60) # Poll every 60 seconds

if __name__ == "__main__":
    main()