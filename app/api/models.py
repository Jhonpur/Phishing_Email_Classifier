from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

DATABASE_URL = "app/database/database.db"  # Sostituisci 'database.db' con il nome del tuo file .db

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    cognome = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    genere = Column(String(1))
    data_nascita = Column(DateTime)

class Email(Base):
    __tablename__ = "emails"
    
    id = Column(Integer, primary_key=True, index=True)
    utente_id_sorgente = Column(Integer, ForeignKey("users.id"), nullable=False)
    utente_id_destinatario = Column(Integer, ForeignKey("users.id"), nullable=False)
    email_sorgente = Column(String, nullable=False)
    email_destinatario = Column(String, nullable=False)
    descrizione = Column(Text)
    oggetto = Column(String)
    data = Column(DateTime)
    url = Column(Boolean)
    stato_spam = Column(Boolean)
    email_id_risposta = Column(Integer, ForeignKey("emails.id"))
    
    # Relationships
    sorgente = relationship("User", foreign_keys=[utente_id_sorgente])
    destinatario = relationship("User", foreign_keys=[utente_id_destinatario])

class UserEmail(Base):
    __tablename__ = "user_emails"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    email_id = Column(Integer, ForeignKey("emails.id"), nullable=False)
    stato_read = Column(Boolean)
    stato_delete = Column(Boolean)
    
    # Relationships
    user = relationship("User")
    email = relationship("Email")

# Dependency per ottenere il DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()