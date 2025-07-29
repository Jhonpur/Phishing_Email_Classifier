# dove si trovano  gli endpoints
from fastapi import FastAPI,  HTTPException
from fastapi.responses import StreamingResponse
import random as rd
from datetime import datetime, timezone
from sqlalchemy.orm import sessionmaker
#from passlib.context import CryptContext # per la gestione delle password
#from database import db, crud, schemas, models
#from app.database.models import User, Email

from io import BytesIO
from app.utils.pdf_generator import generate_report
from app.database.db import engine, Base, SessionLocal
from app.database import crud, models, schemas


Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal() 
app = FastAPI()

#pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") # per la gestione delle password


@app.get("/")
def lire_racine():
    return {"message": "Bienvenue !"}

"""quando ricevo una mail, scansiono il messaggio per determinare se è spam oppure no."""
def scansiona_spam():
   return  rd.randint(0,1)




"""aggiungere l'id dell'utente come parametro nelle url"""

@app.post("/login")
def login(data: dict):
    us = crud.get_user_by_email(db, data["email"]) # verificare se la mail non esiste gia 
    if us:
        raise HTTPException(status_code=401, detail="mail gia esistente nel database")
    
    users = crud.get_all_users(db)
    for user in users:
        if user.email == data["email"] and user.password == data["password"]:
            return {"user_id": user.id}
    raise HTTPException(status_code=401, detail="Credenziali non valide")




#end point per fare il login di un utente
@app.get("/login/i")
def login():
    return {'message':'hello bello, funziona tutto bene !'}





#end point per inviare una email
@app.post("/user/send", response_model=schemas.EmailOut)
def send_email(email: schemas.EmailCreate):
    # Recupera gli utenti mittente e destinatario
    utente_sorgente = crud.get_user_by_email(db, email.email_sorgente)
    utente_destinatario = crud.get_user_by_email(db, email.email_destinatario)

    if not utente_sorgente or not utente_destinatario:
        raise HTTPException(status_code=404, detail="Sender or recipient not found") # oppure si ritorna un messaggio 

    # Crea l'email
    email_obj = crud.create_email_with_user_relation(
        db=db,
        user_id_sorgente=utente_sorgente.id,
        user_id_destinatario=utente_destinatario.id,
        email_sorgente=email.email_sorgente,
        email_destinatario=email.email_destinatario,
        descrizione=email.descrizione,
        oggetto=email.oggetto,
        data= datetime.now(timezone.utc),
        stato_spam = scansiona_spam()
    )

    return schemas.EmailOut.model_validate(email_obj) # non ancora sicuro di quello che deve ritornare se un messaggio o altra cosa




#end point per visualizzare le mail ricevute da un utente
@app.get("/user/inbox", response_model=list[schemas.EmailOut])
def get_inbox(user_mail: str):
    user = crud.get_user_by_email(db, user_mail)
    if not user:
        raise HTTPException(status_code=404, detail="User not found") # oppure si ritorn un messagio

    emails = user.received
    return [schemas.EmailOut.model_validate(email) for email in emails] # in formato json




#end point per visualizzare le mail inviate da un utente
@app.get("/user/sent", response_model=list[schemas.EmailOut])
def get_sent(user_mail: str):
    user = crud.get_user_by_email(db, user_mail)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    emails = user.sent
    return [schemas.EmailOut.model_validate(email) for email in emails]    # in formato json




#end point per visualizzare le mail segnate come spam
@app.get("/user/spam", response_model=list[schemas.EmailOut])
def get_spam(user_mail: str):
    user = crud.get_user_by_email(db, user_mail)
    if not user:
        raise HTTPException(status_code=404, detail="User not found") # o si ritorna un messaggio

    emails = [email for email in user.received if email.stato_spam]
    return [schemas.EmailOut.model_validate(email) for email in emails]




#end point per visualizzare le mail segnate come delete
@app.get("/user/trash", response_model=list[schemas.EmailOut])
def get_trash(user_mail: str):
    user = crud.get_user_by_email(db, user_mail)
    if not user:
        raise HTTPException(status_code=404, detail="User not found") # oppure si ritorna un messagio

    emails = crud.get_deleted_emails_by_user(db,user.id)
    return [schemas.EmailOut.model_validate(email) for email in emails]


#end point per eliminare una mail
@app.post("/user/delete/", response_model=schemas.EmailOut)
def delete_email(user_mail: str, email_id: int):
    user = crud.get_user_by_email(db, user_mail)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    email = crud.get_email_by_id(db, email_id)
    if not email or email.utente_id_destinatario != user.id:
        raise HTTPException(status_code=404, detail="Email not found")
    crud.update_user_email_delete_status(db, user.id, email.id)  #
    #crud.delete_email(db, email.id)
    return schemas.EmailOut.model_validate(email)


#end point per ristorare una mail eliminata in non eliminata
@app.post("/user/restore/", response_model=schemas.EmailOut)
def restore_received_email(user_mail: str, email_id: int):
    user = crud.get_user_by_email(db, user_mail)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    emails = crud.get_deleted_emails_by_user(db, user.id)
    email = next((e for e in emails if e.id == email_id), None)
    if not email or not hasattr(email, "user_emails") or not any(ue.stato_delete for ue in email.user_emails if ue.user_id == user.id):
        raise HTTPException(status_code=404, detail="Email not found or not in trash")


    crud.restore_user_email(db, user.id, email.id)
    return schemas.EmailOut.model_validate(crud.get_email_by_id(db, email.id))


#end point per leggere una mail/ segnare una mail come letta
@app.post("/user/read/", response_model=schemas.EmailOut)
def read_email(user_mail: str, email_id: int):
    user = crud.get_user_by_email(db, user_mail)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    email = crud.get_email_by_id(db, email_id)
    if not email or email.utente_id_destinatario != user.id:
        raise HTTPException(status_code=404, detail="Email not found")

    crud.update_user_email_read_status(db, user.id, email.id)
    #crud.mark_email_as_read(db, user.id, email.id)
    return schemas.EmailOut.model_validate(email)


#end point che genera il report pdf delle mail spam, con dentro le statistiche su tutte le mail
"""il documento pdf conterra:
-numero totale di mail ricevute
-numero di mail inviate
-numero di mail spam
-numero di mail lette
-numero di mail non lette
-numero di mail cancellate
e ci sara anche un grafico a barra o torta per visualizzare queste statistiche """
@app.get("/user/report/pdf")
def report_category(user_mail:str):
    user = crud.get_user_by_email(db, user_mail)
    #user = crud.get_user_by_id(db, user_id.id)
    try:
        pdf_bytes = generate_report(db, user.id)
        return StreamingResponse(BytesIO(pdf_bytes),
                                 media_type="application/pdf",
                                 headers={"Content-Disposition": f"attachment; filename=rapport_categorie_{user.nome}.pdf"})
    except Exception as e:
        print("Errore:", e)
        raise HTTPException(status_code=404, detail=str(e)) 