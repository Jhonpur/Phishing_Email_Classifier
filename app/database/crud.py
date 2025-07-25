"""funzioni per interragire con il database"""

from sqlalchemy.orm import Session
from .models import User, Email, UserEmail
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

#funzione che ritorna tutti gli utenti. suggerimento quando si vuole mandare una mail
def get_all_users(db: Session):
    return db.query(User).all()

#------------------------------------------------------------------------------------------------------------------------------------------------------------#

# EMAIL CRUD

# funzione per creare un'email

#per quanto riguarda l'atttributo spam, prima si usera la funzione per determinare se è una spam
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
        email_id_risposta=email_id_risposta
    )
    db.add(email)
    db.commit()
    db.refresh(email)
    return email

#funzione per ottenere tutte le mail ricevute da un utente
def get_emails_by_user(db: Session, user_id: int):
    return db.query(Email).filter(Email.utente_id_destinatario == user_id).all()


#funzione che data un ID di email ritorna l'email
def get_email_by_id(db: Session, email_id: int):
    return db.query(Email).filter(Email.id == email_id).first()




#funzione che data una mail, ritorna la mail al quale risponde
def get_email_response(db: Session, email_id: int):
    email = db.query(Email).filter(Email.id == email_id).first()
    if email and email.email_id_risposta:
        return db.query(Email).filter(Email.id == email.email_id_risposta).first()
    return None




#funzione per ottenere tutte le mail inviate da un utente
def get_emails_by_user(db: Session, user_id: int):
    return db.query(Email).filter(Email.utente_id_sorgente == user_id).all()

#funzione per segnare una mail come letta(mail ricevuta)
"""def update_email_read_status(db: Session, email_id: int):
    email = db.query(Email).filter(Email.id == email_id).first()
    if email:
        email.stato_read = True
        db.commit()
        db.refresh(email)
    return email"""

#funzione per segnare una mail come spam. per il momento serve solo per testare pero non servira nella realta visto la mail viene scansionata
#prima di essere inserita nel database
def update_email_spam_status(db: Session, email_id: int):
    email = db.query(Email).filter(Email.id == email_id).first()
    if email:
        email.stato_spam = True
        db.commit()
        db.refresh(email)
    return email

#funzione che data un utente ritorna tutte le sue mail cancellate
"""def get_deleted_emails_by_user(db: Session, user_id: int):
    return db.query(Email).filter(Email.utente_id_destinatario == user_id,Email.utente_id_mittente == user_id, Email.stato_delete == True).all()"""


#funzione che data un utente ritorna tutte le sue mail segnate come spam(mail ricevute)
def get_spam_emails_by_user(db: Session, user_id: int):
    return db.query(Email).filter(Email.utente_id_destinatario == user_id, Email.stato_spam == True).all()


"""#funzione che data un utente ritorna tutte le sue mail segnate come non lette(mail ricevute)
def get_unread_emails_by_user(db: Session, user_id: int):
    return db.query(Email).filter(Email.utente_id_destinatario == user_id, Email.stato_read == False).all()"""

#funzione per segnare una mail come cancellata
""""def update_email_delete_status(db: Session, email_id: int):
    email = db.query(Email).filter(Email.id == email_id).first()
    if email:
        email.stato_delete = True
        db.commit()
        db.refresh(email)
    return email"""

#funzione per cancellare una mail
"""def delete_email(db: Session, email_id: int):
    email = db.query(Email).filter(Email.id == email_id).first()
    if email:
        db.delete(email)
        db.commit()
    return email"""



#-------------------------------------------------------------------------------------------------------------------------------------------------------------#
#UserEmail crud 

#funzione per creare una relazione tra un utente e una mail
def create_user_email(db: Session, user_id: int, email_id: int, stato_read: bool = False, stato_delete: bool = False):
    user_email = UserEmail(user_id=user_id, email_id=email_id, stato_read=stato_read, stato_delete=stato_delete)
    db.add(user_email)
    db.commit()
    db.refresh(user_email)
    return user_email

#funzione per modificare lo stato di lettura di una mail per un utente
def update_user_email_read_status(db: Session, user_id: int, email_id: int):
    user_email = db.query(UserEmail).filter(UserEmail.user_id == user_id, UserEmail.email_id == email_id).first()
    if user_email:
        user_email.stato_read = True
        db.commit()
        db.refresh(user_email)
    return user_email

#funzione per cancellare  una mail per un utente
def update_user_email_delete_status(db: Session, user_id: int, email_id: int):
    user_email = db.query(UserEmail).filter(UserEmail.user_id == user_id, UserEmail.email_id == email_id).first()
    if user_email:
        user_email.stato_delete = True
        db.commit()
        db.refresh(user_email)
    return user_email


#funzione per per ripristinare una mail cancellata per un utente
def restore_user_email(db: Session, user_id: int, email_id: int):
    user_email = db.query(UserEmail).filter(UserEmail.user_id == user_id, UserEmail.email_id == email_id).first()
    if user_email:
        user_email.stato_delete = False
        db.commit()
        db.refresh(user_email)
    return user_email


#funzione che ritorna lo stato di lettura di una mail per un utente
def get_user_email_read_status(db: Session, user_id: int, email_id: int):
    user_email = db.query(UserEmail).filter(UserEmail.user_id == user_id, UserEmail.email_id == email_id).first()
    if user_email:
        return user_email.stato_read
    return None


#funzione che ritorna lo stato di cancellazione di una mail per un utente
def get_user_email_delete_status(db: Session, user_id: int, email_id: int):
    user_email = db.query(UserEmail).filter(UserEmail.user_id == user_id, UserEmail.email_id == email_id).first()
    if user_email:
        return user_email.stato_delete
    return None

#funzione per ottener tutte le mail cancellate da un utente
#ritorna  una lista di oggetti Email
def get_deleted_emails_by_user(db: Session, user_id: int):
    return db.query(Email).join(UserEmail).filter(UserEmail.user_id == user_id, UserEmail.stato_delete == True).all()



#funzione per ottenere tutte le mail non lette da un utente
#ritorna una lista di oggetti Email
def get_unread_emails_by_user(db: Session, user_id: int):
    return db.query(Email).join(UserEmail).filter(UserEmail.user_id == user_id, UserEmail.stato_read == False).all()



#funzione per creare una mail e segnare la relazione con l'utente nella tabella UserEmail
def create_email_with_user_relation(
    db: Session,
    user_id_sorgente: int,
    user_id_destinatario: int,
    email_sorgente: str,
    email_destinatario: str,
    descrizione: str = None,
    oggetto: str = None,
    data: datetime = None,
    url: bool = False,
    stato_spam: bool = False,
    email_id_risposta: int = None
):
    email = create_email(
        db, 
        utente_id_sorgente=user_id_sorgente, 
        utente_id_destinatario=user_id_destinatario, 
        email_sorgente=email_sorgente, 
        email_destinatario=email_destinatario, 
        descrizione=descrizione, 
        oggetto=oggetto, 
        data=data, 
        url=url, 
        stato_spam=stato_spam, 
        email_id_risposta=email_id_risposta
    )
    
    create_user_email(db, user_id_sorgente, email.id)
    create_user_email(db, user_id_destinatario, email.id)
    return email


#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------#
# per il report pdf


#funzione che ritorna il numero totale di mail ricevute da un utente
def get_total_received_emails(db: Session, user_id: int):
    return db.query(Email).filter(Email.utente_id_destinatario == user_id).count()

#funzione che ritorna il numero totale di mail inviate da un utente
def get_total_sent_emails(db: Session, user_id: int):
    return db.query(Email).filter(Email.utente_id_sorgente == user_id).count()

#funzione che ritorna il numero totale di mail spam ricevute da un utente
def get_total_spam_emails(db: Session, user_id: int):
    return db.query(Email).filter(Email.utente_id_destinatario == user_id, Email.stato_spam == True).count()

#funzione che ritorna il numero totale di mail lette da un utente
def get_total_read_emails(db: Session, user_id: int):
    return db.query(UserEmail).filter(UserEmail.user_id == user_id, UserEmail.stato_read == True).count()

#funzione che ritorna il numero di mail non lette da un utente
def get_total_non_read_emails(db: Session, user_id:int):
    return db.query(UserEmail).filter(UserEmail.user_id == user_id, UserEmail.stato_read == False).count()

#funzione che ritorna il numero di mail cancellate da un utente
def get_total_cancelled_mails(db: Session, user_id:int):
    return db.query(Email).join(UserEmail).filter(UserEmail.user_id == user_id, UserEmail.stato_delete == True).count()