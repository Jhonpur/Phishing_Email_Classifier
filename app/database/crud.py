"""funzioni per interragire con il database"""

from sqlalchemy.orm import Session
from models import User, Email
from datetime import datetime, timezone
#from datetime import datetime

# USER CRUD

# funzione per creare un utente
def create_user(db: Session, nome: str, cognome: str, email: str, password: str  ,genere: str = None, data_nascita: str = None):
    user = User(nome=nome, cognome=cognome, email=email, password =password, genere=genere, data_nascita=data_nascita)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

# funzione per ottenere un utente per ID
def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


#funzione per ritornare l'utente per email
def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

#funzione per cancellare un utente dal database
def delete_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
    return user

#------------------------------------------------------------------------------------------------------------------------------------------------------------#

# EMAIL CRUD

# funzione per creare un'email

#perquanto riguarda l'atttributo spam, prima si usera la funzione per determinare se è una spam
#e poi si usera il risultato come parametro della funzione 
def create_email(
    db: Session,
    utente_id_sorgente: int,
    utente_id_destinatario: int,
    email_sorgente: str,
    email_destinatario: str,
    descrizione: str = None,
    oggetto: str = None,
    data: datetime = None,
    url: bool = False,
    stato_spam: bool = False,
    stato_read: bool = False,
    stato_delete: bool = False,
    email_id_risposta: int = None
):
    email = Email(
        utente_id_sorgente=utente_id_sorgente,
        utente_id_destinatario=utente_id_destinatario,
        email_sorgente=email_sorgente,
        email_destinatario=email_destinatario,
        descrizione=descrizione,
        oggetto=oggetto,
        data=data,
        url=url,
        stato_spam=stato_spam,
        stato_read=stato_read,
        stato_delete=stato_delete,
        email_id_risposta=email_id_risposta
    )
    db.add(email)
    db.commit()
    db.refresh(email)
    return email

#funzione per ottenere tutte le mail ricevute da un utente
def get_emails_by_user(db: Session, user_id: int):
    return db.query(Email).filter(Email.utente_id_destinatario == user_id).all()


#funzione per ottenere tutte le mail inviate da un utente
def get_emails_by_user(db: Session, user_id: int):
    return db.query(Email).filter(Email.utente_id_sorgente == user_id).all()

#funzione per segnare una mail come letta
def update_email_read_status(db: Session, email_id: int):
    email = db.query(Email).filter(Email.id == email_id).first()
    if email:
        email.stato_read = True
        db.commit()
        db.refresh(email)
    return email

#funzione per segnare una mail come spam. per il momento serve solo per testare
def update_email_spam_status(db: Session, email_id: int):
    email = db.query(Email).filter(Email.id == email_id).first()
    if email:
        email.stato_spam = True
        db.commit()
        db.refresh(email)
    return email

#funzione che data un utente ritorna tutte le sue mail cancellate
def get_deleted_emails_by_user(db: Session, user_id: int):
    return db.query(Email).filter(Email.utente_id_destinatario == user_id, Email.stato_delete == True).all()


##funzione che data un utente ritorna tutte le sue mail segnate come spam
def get_spam_emails_by_user(db: Session, user_id: int):
    return db.query(Email).filter(Email.utente_id_destinatario == user_id, Email.stato_spam == True).all()


##funzione che data un utente ritorna tutte le sue mail segnate come non lette
def get_unread_emails_by_user(db: Session, user_id: int):
    return db.query(Email).filter(Email.utente_id_destinatario == user_id, Email.stato_read == False).all()

#funzione per segnare una mail come cancellata
def update_email_delete_status(db: Session, email_id: int):
    email = db.query(Email).filter(Email.id == email_id).first()
    if email:
        email.stato_delete = True
        db.commit()
        db.refresh(email)
    return email

#funzione per cncellare una mail
def delete_email(db: Session, email_id: int):
    email = db.query(Email).filter(Email.id == email_id).first()
    if email:
        db.delete(email)
        db.commit()
    return email