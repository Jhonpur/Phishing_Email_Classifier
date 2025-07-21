"""(serve solo per testare localmente)"""

#from sqlalchemy.orm import Session
from db import engine, Base, SessionLocal
from models import *
from crud import *
from schemas import *

# Crea le tabelle nel database
Base.metadata.create_all(bind=engine)
from sqlalchemy.orm import sessionmaker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



    

def main():
    db = SessionLocal()

    # SOLO PER TEST: elimina tutti gli utenti e le email
    db.query(Email).delete()
    db.query(User).delete()
    db.commit()

    # Crea due utenti
    user1_schema = UserCreate( nome="Mario", cognome="Rossi", email="mario.rossi@email.com",password="password123",genere = "m")
    user2_schema = UserCreate(nome="Anna", cognome="Bianchi", email="anna.bianchi@email.com",password="password456")

    user1 = create_user(db, **user1_schema.model_dump())
    user2 = create_user(db, **user2_schema.model_dump())
    print("Utenti creati:", user1, user2)

    # Crea una email da Mario ad Anna
    email_schema = EmailCreate(
        email_sorgente=user1.email,
        email_destinatario=user2.email,
        descrizione="Ciao Anna, come stai?",
        oggetto="Saluti",
        data=datetime.now(timezone.utc)
    )

    email = create_email(db, utente_id_sorgente = get_user_by_email(db,email_schema.email_sorgente).id,utente_id_destinatario = get_user_by_email(db,email_schema.email_destinatario).id,**email_schema.model_dump())

    print("Email inviata:", email)

    # Recupera Mario e stampa le sue email inviate
    

    mario = get_user_by_id(db, user1.id)
    print("Email inviate da Mario:", mario.sent)

    for email in mario.sent:
        email_out = EmailOut.model_validate(email) #si converte la mail in uno schema Pydantic per l'output
        print("Email inviata da Mario:", email_out)

    db.close()

if __name__ == "__main__":
    main()