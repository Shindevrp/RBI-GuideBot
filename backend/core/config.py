from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Load .env file if it exists
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

    # OpenAI and Pinecone
    OPENAI_API_KEY: "YOUR_OPENAI_API_KEY"
    PINECONE_API_KEY: "YOUR_PINECONE_API_KEY"
    PINECONE_ENV: "PINECONE_ENV" = "us-east-1"

    # Vector DB Index Names
    RBI_PINECONE_INDEX: str = "rbi-regulations-index"
    LENDING_PINECONE_INDEX: str = "nbfc-lending-index"

    # Email Ingestion (IMAP)
    IMAP_SERVER: "YOUR_IMAP_SERVER"
    IMAP_USER: "YOUR_IMAP_USER"
    IMAP_PASSWORD: "YOUR_IMAP_PASSWORD"

    # Email Reply (SMTP)
    SMTP_SERVER: "YOUR_SMTP_SERVER"
    SMTP_PORT: "YOUR_SMTP_PORT" = 587
    SMTP_USER: "YOUR_SMTP_USER"
    SMTP_PASSWORD: "YOUR_SMTP_PASSWORD"

     # Database
    DATABASE_URL: str = "sqlite:///./rbi_guidebot_agent.db"


settings = Settings()