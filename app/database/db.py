"""connessione DB e Base ORM"""

from sqlalchemy import create_engine # SQLAlchemy
from sqlalchemy.orm import declarative_base, sessionmaker # ORM

DATABASE_URL = "sqlite:///./phising_email_detection_database.db" # SQLite database URL

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False}) # SQLite specific argument
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False) # Session factory
Base = declarative_base() # Base class for ORM models 

# Crea tutte le tabelle
Base.metadata.create_all(bind=engine)