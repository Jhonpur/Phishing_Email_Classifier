"""(serve solo per testare localmente)"""

"""
#from sqlalchemy.orm import Session
from app.database.db import engine, Base, SessionLocal
from app.database.models import *
from app.database.crud import *
from app.database.schemas import *
import random as rd #  solo per il test 
from datetime import datetime, timezone

# Crea le tabelle nel database
Base.metadata.create_all(bind=engine)
from sqlalchemy.orm import sessionmaker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
"""

"""
def sep():
    print("=" *50)"""

"""
def scansiona_spam():
    num = rd.randint(0,1)
    return {'is_spam': num,
             'spam_probability': rd.randint(0,100) if num == 1 else 0, # Simula una probabilità di spam casuale, 
            'spam_reason': ["phishing","link malevole","marketing agressivo"] if num == 1 else None # Simula una probabilità di spam casuale e un motivo opzionale
    } 
"""
    
"""
def main():
    db = SessionLocal()

    # SOLO PER TEST: elimina tutti gli utenti e le email
    db.query(Email).delete()
    db.query(User).delete()
    db.query(UserEmail).delete()  # Elimina le relazioni tra utenti ed email
    db.commit()

    # Crea due utenti
    user1_schema = UserCreate( nome="ANGE BONHEUR", cognome="KADJA FOMEKON", email="angebonheur@email.com",password="password123",genere = "m")
    user2_schema = UserCreate(nome="LORENZO", cognome="POURPOUR", email="lorenzopourpour@email.com",password="password456", genere ='m')
    user3_schema = UserCreate(nome="GABRIELLE", cognome="GRECCO", email="gabriellegrecco@email.com",password="passwor890", genere = 'm')


    user1 = create_user(db, **user1_schema.model_dump())
    user2 = create_user(db, **user2_schema.model_dump())
    user3 = create_user(db, **user3_schema.model_dump())
    print("Utenti creati:", user1, user2, user3)
    
    sep()
    sep()
    sep()

    # Crea una email da Mario ad Anna
    dict1 = scansiona_spam() # Simula la scansione per spam
    email_schema1 = EmailCreate(
        email_sorgente=user1.email,
        email_destinatario=user2.email,
        descrizione="Ciao lore, come stai?",
        oggetto="Saluti",
        data=datetime.now(timezone.utc),
        #stato_spam = dict['is_spam'],
        #spam_probability = dict['spam_probability'],
        #spam_reason = dict['spam_reason'],
    )

    dict2 = scansiona_spam() # Simula la scansione per spam
    email_schema2 = EmailCreate(
        email_sorgente=user2.email,
        email_destinatario=user1.email,
        descrizione="bene ange e tu ?",
        email_id_risposta = 1, # risposta alla prim mail
        data=datetime.now(timezone.utc),
        #stato_spam = scansiona_spam()
    )

    dict3 = scansiona_spam() # Simula la scansione per spam
    email_schema3 = EmailCreate(
        email_sorgente=user1.email,
        email_destinatario=user2.email,
        descrizione="bene, senti dobbiamo preparare una sorpresa per GABRI. si è appena laureato dobbiamo fargli un regalino.cosa ne pensi?",
        email_id_risposta = 2, # risposta alla seconda  mail
        data=datetime.now(timezone.utc),
        #stato_spam = scansiona_spam()
    )

    dict4 = scansiona_spam() # Simula la scansione per spam
    email_schema4 = EmailCreate(
        email_sorgente=user2.email,
        email_destinatario=user1.email,
        descrizione="ah buona idea. ne parliamo intorno a un sprizt? domani dopo il lavoro a porta nuova",
        email_id_risposta = 3, # risposta alla terza mail
        data=datetime.now(timezone.utc),
        #stato_spam = scansiona_spam()
    )

    dict5 = scansiona_spam() # Simula la scansione per spam
    email_schema5 = EmailCreate(
        email_sorgente=user1.email,
        email_destinatario=user2.email,
        descrizione="ok . vabbin",
        email_id_risposta = 4, # risposta alla quarta mail
        data=datetime.now(timezone.utc),
        #stato_spam = scansiona_spam()
    )

    email1 = create_email_with_user_relation(db, user_id_sorgente = get_user_by_email(db,email_schema1.email_sorgente).id,user_id_destinatario = get_user_by_email(db,email_schema1.email_destinatario).id,**email_schema1.model_dump(),stato_spam= dict1['is_spam'], spam_probability=dict1['spam_probability'], spam_reason=dict1['spam_reason'])
    email2 = create_email_with_user_relation(db, user_id_sorgente = get_user_by_email(db,email_schema2.email_sorgente).id,user_id_destinatario = get_user_by_email(db,email_schema2.email_destinatario).id,**email_schema2.model_dump(),stato_spam= dict2['is_spam'], spam_probability=dict2['spam_probability'], spam_reason=dict2['spam_reason'])
    email3 = create_email_with_user_relation(db, user_id_sorgente = get_user_by_email(db,email_schema3.email_sorgente).id,user_id_destinatario = get_user_by_email(db,email_schema3.email_destinatario).id,**email_schema3.model_dump(),stato_spam= dict3['is_spam'], spam_probability=dict3['spam_probability'], spam_reason=dict3['spam_reason'])
    email4 = create_email_with_user_relation(db, user_id_sorgente = get_user_by_email(db,email_schema4.email_sorgente).id,user_id_destinatario = get_user_by_email(db,email_schema4.email_destinatario).id,**email_schema4.model_dump(),stato_spam= dict4['is_spam'], spam_probability=dict4['spam_probability'], spam_reason=dict4['spam_reason'])
    email5 = create_email_with_user_relation(db, user_id_sorgente = get_user_by_email(db,email_schema5.email_sorgente).id,user_id_destinatario = get_user_by_email(db,email_schema5.email_destinatario).id,**email_schema5.model_dump(),stato_spam= dict5['is_spam'], spam_probability=dict5['spam_probability'], spam_reason=dict5['spam_reason'])


    dict6 = scansiona_spam() # Simula la scansione per spam
    email_schema6 = EmailCreate(
        email_sorgente=user1.email,
        email_destinatario=user3.email,
        descrizione="il capibarra è l'animale piu simpatico al mondo . non ha nessun predattore e mangia solo erba ",
        #email_id_risposta = 4, # risposta alla quarta mail
        data=datetime.now(timezone.utc),
        #stato_spam = scansiona_spam()
    )

    dict7 = scansiona_spam() # Simula la scansione per spam
    email_schema7 = EmailCreate(
        email_sorgente=user2.email,
        email_destinatario=user3.email,
        descrizione="gentile gabri, mi serve il tuo curriculum per preparare il collocquio conosciutivo. grazie per l'attenzione",
        #email_id_risposta = 4, # risposta alla quarta mail
        data=datetime.now(timezone.utc),
        #stato_spam = scansiona_spam()
    )
 
    dict8 = scansiona_spam() # Simula la scansione per spam
    email_schema8 = EmailCreate(
        email_sorgente=user3.email,
        email_destinatario=user1.email,
        descrizione="salve ange. perfavore mi puoi mandare l'indirizzo della cena di sta sera? grazie",
        #email_id_risposta = 4, # risposta alla quarta mail
        data=datetime.now(timezone.utc),
        #stato_spam = scansiona_spam()
    )

    email6 = create_email_with_user_relation(db, user_id_sorgente = get_user_by_email(db,email_schema6.email_sorgente).id,user_id_destinatario = get_user_by_email(db,email_schema6.email_destinatario).id,**email_schema6.model_dump(),stato_spam= dict6['is_spam'], spam_probability=dict6['spam_probability'], spam_reason=dict6['spam_reason'])
    email7 = create_email_with_user_relation(db, user_id_sorgente = get_user_by_email(db,email_schema7.email_sorgente).id,user_id_destinatario = get_user_by_email(db,email_schema7.email_destinatario).id,**email_schema7.model_dump(),stato_spam= dict7['is_spam'], spam_probability=dict7['spam_probability'], spam_reason=dict7['spam_reason'])
    email8 = create_email_with_user_relation(db, user_id_sorgente = get_user_by_email(db,email_schema8.email_sorgente).id,user_id_destinatario = get_user_by_email(db,email_schema8.email_destinatario).id,**email_schema8.model_dump(),stato_spam= dict8['is_spam'], spam_probability=dict8['spam_probability'], spam_reason=dict8['spam_reason'])


    print("Email inviata:", email1,email2,email3,email4,email5,email6,email7,email8)
    sep()
    sep()

    # Recupera Mario e stampa le sue email inviate
    

    ange = get_user_by_id(db, user1.id)
    print("Email inviate da Mario:", ange.sent)
    sep()

    #update_user_email_delete_status(db,user1.id, 2)
    #update_user_email_delete_status(db,user1.id, 8)

    for email in ange.sent:
        email_out = EmailOut.model_validate(email) #si converte la mail in uno schema Pydantic per l'output
        print("Email inviata da Mario:", email_out)

    db.close()
    sep()

    print(get_unread_emails_by_user(db, user_id = 1))
    sep()
"""

"""
if __name__ == "__main__":
    main()
    """