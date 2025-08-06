from fastapi import APIRouter, Form, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from datetime import datetime, timezone
from predict_spam import predict_spam  # Your spam detection function
from app import crud  # Your DB access layer
from app.database import get_db  # Dependency to get a DB session
from app.database.db import engine, Base, SessionLocal
from sqlalchemy.orm import sessionmaker, Session
from app.database import crud, models, schemas

Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal() 
router = APIRouter()

@router.post("/send", response_class=HTMLResponse)
async def post_send_email(request: Request,
                          recipient: str = Form(...),
                          subject: str = Form(...),
                          content: str = Form(...),
                          db: Session = Depends(get_db)):
    
    mittente = request.query_params.get("user_mail")
    if not mittente:
        return HTMLResponse("Mittente mancante nell'URL", status_code=400)

    # Log the incoming email
    print("EMAIL INVIATA:")
    print(f"Mittente: {mittente}")  # MANCANTE
    print(f"Destinatario: {recipient}")
    print(f"Oggetto: {subject}")
    print(f"Contenuto: {content}")

    # Check for spam
    spam_result = predict_spam(subject, content)
    is_spam = spam_result['is_spam']
    spam_reasons = spam_result['spam_reasons']
    spam_probability = spam_result['spam_probability']
    url = spam_result['contains_url']

    # Prendo id del destinatario
    utente_sorgente = crud.get_user_by_email(db, mittente)
    utente_destinario = crud.get_user_by_email(db, recipient)

    if not utente_sorgente or not utente_destinario:
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
        url=url,
        stato_spam=is_spam,
        spam_reason=spam_reasons,
        spam_probability=spam_probability
    )

    return RedirectResponse(url="/inbox?sent=true", status_code=303)
