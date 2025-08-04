from fastapi import APIRouter, Form, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from datetime import datetime

from predict_spam import predict_spam  # Your spam detection function
from app import crud  # Your DB access layer
from app.database import get_db  # Dependency to get a DB session
from app.database.db import engine, Base, SessionLocal
from sqlalchemy.orm import sessionmaker
from app.database import crud, models, schemas

Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal() 
router = APIRouter()

# MANCA IL REASON

@router.post("/send", response_class=HTMLResponse)
async def post_send_email(  # MI MANCA LA MAIL SORGENTE
    request: Request,
    recipient: str = Form(...),
    subject: str = Form(...),
    content: str = Form(...)
    # db: Session = Depends(get_db)
):
    # Log the incoming email
    print("EMAIL INVIATA:")
    print(f"Mittente: {mittente}")  # MANCANTE
    print(f"Destinatario: {recipient}")
    print(f"Oggetto: {subject}")
    print(f"Contenuto: {content}")

    # Check for spam
    spam_result = predict_spam(subject, content)
    is_spam = spam_result['is_spam']

    # Prendo id del destinatario
    utente_sorgente = crud.get_user_by_email(db, mittente)
    utente_destinario = crud.get_user_by_email(db, recipient)

    if not sender_user or not recipient_user:
        return HTMLResponse(content="Invalid sender or recipient", status_code=400)

    # Save the email to the DB
    crud.create_email(
        db=db,
        utente_id_sorgente=utente_sorgente.id,
        utente_id_destinatario=utente_destinario.id,
        email_sorgente=mittente,
        email_destinatario=recipient,
        descrizione=content,
        oggetto=subject,
        data=datetime.now(timezone.utc),
        stato_spam=is_spam
    )

    # 4. Redirect back to inbox with success notice
    return RedirectResponse(url="/inbox?sent=true", status_code=303)
