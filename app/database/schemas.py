"""(schemi Pydantic)"""

from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
from datetime import datetime, timezone

class UserCreate(BaseModel): # Definizione dello schema per la creazione di un utente
    nome: str = Field(min_length=1, max_length=50, description="Nome dell'utente")
    cognome: str = Field(min_length=1, max_length=50, description="Cognome dell'utente")
    email: EmailStr
    genere : str = Field( default=None,pattern="^(m|f)$", description="m per maschio, f per femmina") # 'M' per maschio, 'F' per femmina
    data_nascita :Optional[datetime] = None  # Data di nascita opzionale
    password: str = Field(min_length=8, description="Password dell'utente, deve essere sicura e complessa")

    



class UserOut(BaseModel):  # Definizione dello schema per l'output di un utente
    nome: str
    cognome: str
    email: EmailStr

    class Config:
        from_attributes = True


class EmailCreate(BaseModel): # Definizione dello schema per la creazione di un'email
    email_sorgente: EmailStr
    email_destinatario: EmailStr
    descrizione: Optional[str] = Field(default=None,min_length=0,description="Contenuto della mail (testo)")
    oggetto: Optional[str] = Field(default=None,min_length=0, description= "oggetto della mail")
    email_id_risposta: Optional[int] = None # ID della mail a cui si sta rispondendo, se presente
    data: datetime # è la data usando datetime.now(timezone.utc) , momento in cui viene creata l'email
    #stato_spam: bool

    

class EmailOut(EmailCreate): # Definizione dello schema per l'output di un'email
    id: int
    email_sorgente: EmailStr
    email_destinatario: EmailStr
    descrizione: Optional[str] = None
    oggetto: Optional[str] = None
    data: datetime
    stato_spam: Optional[bool] = False #da modificare dopo.
    spam_probability: Optional[float] = 0.0 # probabilità che la mail sia spam, da 0 a 100

    #deve essere una lista di motivi per cui la mail è stata classificata come spam, se presente
    spam_reason: Optional[list[str]] = None # motivo per cui la mail è stata classificata come spam, se presente
    email_id_risposta: Optional[int] = None

    class Config:
        from_attributes= True