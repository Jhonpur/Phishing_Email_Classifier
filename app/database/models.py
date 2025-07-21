"""definizione modelli per ORM"""

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship
from db import Base
from datetime import datetime, timezone

class User(Base): # Definizione del modello User per l'ORM
    __tablename__ = "users" # nome tabella nel database

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    cognome = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)  # Password per l'utente, da gestire in modo sicuro
    genere = Column(String(1), nullable=True)  # 'M' per maschio, 'F' per femmina
    data_nascita = Column(DateTime, nullable=True)  # Data di nascita opzionale
    #password = Column(String, nullable=False)  # Password per l'utente, da gestire in modo sicuro

    # relazioni
    
    """Questa relazione permette di accedere a tutte le email inviate da un utente
    Ad esempio, utente.sent restituisce la lista delle email dove l'utente è il mittente"""
    sent = relationship("Email", foreign_keys='Email.utente_id_sorgente', back_populates="mittente")
    
    """Questa relazione permette di accedere a tutte le email ricevute da un utente
    Ad esempio, utente.received restituisce la lista delle email dove l'utente è il destinatario"""
    received = relationship("Email", foreign_keys='Email.utente_id_destinatario', back_populates="destinatario")

    def __repr__(self):
        return f"<User(id={self.id}, nome={self.nome}, cognome={self.cognome}, email={self.email})>"


class Email(Base): # Definizione del modello Email per l'ORM
    __tablename__ = "emails"

    id = Column(Integer, primary_key=True, index=True)
    utente_id_sorgente = Column(Integer, ForeignKey("users.id"), nullable=False)
    utente_id_destinatario = Column(Integer, ForeignKey("users.id"), nullable=False)
    email_sorgente = Column(String, nullable=False)
    email_destinatario = Column(String, nullable=False)
    descrizione = Column(Text)  # body della mail, senza limite di lunghezza
    oggetto = Column(String) # oggetto della mail limite di 255 caratteri
    data = Column(DateTime, default=lambda: datetime.now(timezone.utc)) # data di invio della mail, con timezone UTC

    url = Column(Boolean, default=False) # indica se la mail contiene un URL nel body DOPO ANALISI
    stato_spam = Column(Boolean, default=False) # indica se la mail è stata classificata come spam DOPO ANALISI

    stato_read = Column(Boolean, default=False) # indica se la mail è stata letta dal destinatario
    stato_delete = Column(Boolean, default=False) # indica se la mail è stata eliminata dal destinatario

    # email_id_risposta permette di collegare una mail alla mail a cui sta rispondendo
    email_id_risposta = Column(Integer, ForeignKey("emails.id"), nullable=True)
    
    # relazioni
    """Permette di collegare una mail alla mail a cui sta rispondendo (tramite email_id_risposta).
    Ad esempio, email.risposta restituisce la mail originale a cui questa mail è una risposta."""
    risposta = relationship("Email", remote_side=[id], backref="risposte")

    """Permette di accedere all'oggetto User che ha inviato la mail.
    Ad esempio, email.mittente restituisce il mittente della mail."""
    mittente = relationship("User", foreign_keys=[utente_id_sorgente], back_populates="sent")
    
    """Permette di accedere all'oggetto User che ha ricevuto la mail.
    Ad esempio, email.destinatario restituisce il destinatario della mail."""
    destinatario = relationship("User", foreign_keys=[utente_id_destinatario], back_populates="received")

    def __repr__(self):
        return f"<Email(id={self.id}, email_sorgente={self.email_sorgente}, email_destinatario={self.email_destinatario}, oggetto={self.oggetto})>"