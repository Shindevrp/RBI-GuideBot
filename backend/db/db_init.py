# db_init.py
# Utility to initialize the search history database for RBI GuideBot

from backend.models.search_history import Base, engine

if __name__ == "__main__":
    print("Creating all tables in the database...")
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully.")
