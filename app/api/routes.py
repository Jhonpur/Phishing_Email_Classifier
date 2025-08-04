from fastapi import APIRouter, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse,StreamingResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import sessionmaker
from app.database.db import engine, Base, SessionLocal
from app.database import crud, models, schemas
from app.utils.pdf_generator import generate_report
from datetime import datetime, timedelta
from io import BytesIO

router = APIRouter()
templates = Jinja2Templates(directory="Frontend/templates")

Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal() 

# Dati per spam
MOCK_SPAM_EMAILS = [
    {
        "id": 201,
        "sender": "noreply@fake-bank.com",
        "subject": "URGENTE: Verifica il tuo conto",
        "preview": "Il tuo conto verrà bloccato se non verifichi entro 24 ore...",
        "date": datetime.now() - timedelta(hours=5),
        "content": "ATTENZIONE: Il tuo conto bancario verrà sospeso. Clicca qui per verificare.",
        "is_read": False
    }
]
#from fastapi import FastAPI, HTTPException
#from pydantic import BaseModel
#from fastapi.responses import JSONResponse
#app = FastAPI()
# 
#class LoginData(BaseModel):
#    email: str
#    password: str
# 
#@app.get("/", response_class=HTMLResponse)
#def get_login(request: Request):
#    return templates.TemplateResponse("login.html", {"request": request})
#    
## Endpoint API per il login
#@app.post("/login")
#def login(data: LoginData):
#    if data.email == "admin@email.com" and data.password == "123":
#        return {
#            "token": "jwt_token_fake_123",
#            "user": {
#                "email": data.email,
#                "name": "Admin"
#            }
#        }
#    return JSONResponse(status_code=401, content={"detail": "Credenziali errate"})

@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("base.html", {"request": request})


def format_email_date(date):
    today = datetime.today().date()
    if date.date() == today:
        return date.strftime("%H:%M")  # solo orario se è oggi
    return date.strftime("%d/%m")      # altrimenti giorno/mese


@router.get("/inbox", response_class=HTMLResponse)
async def inbox(request: Request, user_mail: str, selected_email_id: int = None):
    user = crud.get_user_by_email(db, user_mail)
    if not user:
        raise HTTPException(status_code=404, detail="User not found") # oppure si ritorn un messagio

    # Ottengo tutte le email ricevute
    emails = user.received

    # Prendiamo solo le mail che non hanno status delete = 1/2
    emails = [email for email in emails if not crud.get_user_email_delete_status(db, user.id, email.id)]

    # Ordina email per data (più recenti prima)
    sorted_emails = sorted(emails, key=lambda x: x.data, reverse=True)

    # Controllo stato per pop-up di conferma email inviata
    sent = request.query_params.get("sent") == "true"

    # Controllo stato di eliminazione per visualizzazione email
    # Aggiungi date formattate
    for email in sorted_emails:
        email.formatted_date = format_email_date(email.data)
        email.is_read = crud.get_user_email_read_status(db, user.id, email.id)
        
        # Aggiungi info extra da database a ogni email
    #for email in sorted_emails:
    #    email.formatted_date = format_email_date(email.data)
    #    # Qui leggiamo dal database se la mail è letta
    #    read_status = crud.get_user_email_read_status(db, user.id, email.id)
    #    email.is_read = read_status  # puoi usare anche email.stato_read, ma meglio is_read per templat

    selected_email = None
    if selected_email_id:
        selected_email = next((email for email in sorted_emails if email.id == selected_email_id), None)
        # Segna come letta se selezionata
        if selected_email:
            crud.update_user_email_read_status(db, user.id, selected_email.id)
    
    return templates.TemplateResponse("inbox.html", {
        "request": request,
        "emails": sorted_emails,
        "selected_email": selected_email,
        "sent": sent,
        "user_mail": user_mail
    })

# Caricamento del form
@router.get("/send", response_class=HTMLResponse)
async def send_get(request: Request, user_mail: str, reply_to: int = None, forward: int = None):
    user = crud.get_user_by_email(db, user_mail)
    if not user:
        raise HTTPException(status_code=404, detail="Utente non trovato")

    email_data = {
        "destinatario": "",
        "oggetto": "",
        "descrizione": ""
    }
    # DA AGGIORNARE PER COLLEGAMENTO AL DB, NON HO AGGIORNATO ANCORA I BOTTONI RISPONDI E INOLTRA NEI TEMPLATE
    if reply_to:
        # Risposta → Recupera email e precompila il destinatario e l’oggetto
        original = crud.get_email_by_id(db, reply_to)
        if original:
            email_data["destinatario"] = original.email_sorgente
            email_data["oggetto"] = f"Re: {original.oggetto}"
            email_data["descrizione"] = f"\n\n--- Messaggio originale ---\n{original.descrizione}"

    elif forward:
        # Inoltro → Recupera email e precompila oggetto e testo (destinatario vuoto)
        original = crud.get_email_by_id(db, forward)
        if original:
            email_data["oggetto"] = f"Fwd: {original.oggetto}"
            email_data["descrizione"] = f"\n\n--- Messaggio inoltrato ---\nDa: {original.email_sorgente}\n{original.descrizione}"

    return templates.TemplateResponse("send.html", {
        "request": request,
        "user_mail": user_mail,
        "email_data": email_data
    })

# Invio del form
@router.post("/send", response_class=HTMLResponse)
async def post_send_email(request: Request, recipient: str = Form(...), subject: str = Form(...), content: str = Form(...)
):
    # Per ora stampa nel terminale o log — da sostituire con salvataggio nel DB
    print("EMAIL INVIATA:")
    print(f"Destinatario: {recipient}")
    print(f"Oggetto: {subject}")
    print(f"Contenuto: {content}")

    # In futuro: salva email nel database, triggera classificatore spam, ecc.

    # mostra pop-up di successo in inbox
    return RedirectResponse(url="/inbox?sent=true", status_code=303)


@router.get("/sent", response_class=HTMLResponse)
async def sent(request: Request, user_mail: str, email_id: int = None):
    user = crud.get_user_by_email(db, user_mail)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # 1. Ottieni le email inviate da questo utente
    emails = crud.get_emails_sent_by_user(db, user.id)

    # Prendiamo solo le mail che non hanno status delete = 1/2
    emails = [email for email in emails if not crud.get_user_email_delete_status(db, user.id, email.id)]

    # Ordina email per data (più recenti prima)
    sorted_emails = sorted(emails, key=lambda x: x.data, reverse=True)

    # 2. Formatta la data per ogni email e imposta come lette
    for email in emails:
        email.formatted_date = format_email_date(email.data)
        email.is_read = True  # Forza lo stato come "letto" per le email inviate

    # 3. Trova l’email selezionata
    selected_email = None
    if email_id:
        selected_email = next((email for email in emails if email.id == email_id), None)
        if selected_email:
            selected_email.is_read = True  # opzionale, qui è puramente visivo

    # 4. Passa tutto al template
    return templates.TemplateResponse("sent.html", {
        "request": request,
        "emails": sorted_emails,
        "selected_email": selected_email,
        "user_mail": user_mail
    })


@router.get("/spam", response_class=HTMLResponse)
async def spam(request: Request, email_id: int = None):
    sorted_emails = sorted(MOCK_SPAM_EMAILS, key=lambda x: x["date"], reverse=True)
    
    for email in sorted_emails:
        email["formatted_date"] = format_email_date(email["date"])
    
    selected_email = None
    if email_id:
        selected_email = next((email for email in sorted_emails if email["id"] == email_id), None)
        if selected_email:
            selected_email["is_read"] = True
    
    return templates.TemplateResponse("spam.html", {
        "request": request,
        "emails": sorted_emails,
        "selected_email": selected_email
    })


@router.get("/trash", response_class=HTMLResponse)
async def trash(request: Request, user_mail: str, email_id: int = None):
    user = crud.get_user_by_email(db, user_mail)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Recupera le email eliminate per l'utente
    emails = crud.get_deleted_emails_by_user(db, user.id)

    # Mostriamo solo le mail con stato_deletee 1 (mail solo spostate nel cestino)
    emails = [email for email in emails if crud.get_user_email_delete_status(db, user.id, email.id) == 1]

    # Ordina email per data (più recenti prima)
    sorted_emails = sorted(emails, key=lambda x: x.data, reverse=True)

    # Aggiunge formattazione data e stato lettura
    for email in emails:
        email.formatted_date = format_email_date(email.data)
        email.is_read = crud.get_user_email_read_status(db, user.id, email.id)

    # Recupera email selezionata
    selected_email = None
    if email_id:
        selected_email = next((email for email in emails if email.id == email_id), None)
        if selected_email:
            crud.update_user_email_read_status(db, user.id, selected_email.id)

    return templates.TemplateResponse("trash.html", {
        "request": request,
        "emails": sorted_emails,
        "selected_email": selected_email,
        "user_mail": user_mail
    })


# Sposta le mail nel cestino
@router.post("/delete_email", response_class=HTMLResponse)
async def delete_email(request: Request, user_mail: str = Form(...), email_id: int = Form(...), current_page: str = Form(...)):
    # 1. Otteniamo l’utente
    user = crud.get_user_by_email(db, user_mail)
    if not user:
        raise HTTPException(status_code=404, detail="Utente non trovato")

    # 2. Eseguiamo la "cancellazione logica"
    crud.update_user_email_delete_status(db, user.id, email_id)

    # 3. Reindirizziamo alla pagina da cui l’utente proviene
    return RedirectResponse(url=f"/{current_page}?user_mail={user_mail}", status_code=303)


# Le elimina definitivamente dal db (non vero, cambia solo stato a 2)
@router.post("/delete_forever", response_class=HTMLResponse)
async def delete_forever_email(
    request: Request,
    user_mail: str = Form(...),
    email_id: int = Form(...),
):
    user = crud.get_user_by_email(db, user_mail)
    if not user:
        raise HTTPException(status_code=404, detail="Utente non trovato")

    crud.delete_user_emai_definitivelyl(db, user.id, email_id)

    # Dopo la cancellazione, torna al cestino
    return RedirectResponse(url=f"/trash?user_mail={user_mail}", status_code=303)


@router.get("/report_pdf", response_class=StreamingResponse)
def report_category(user_mail:str):
    user = crud.get_user_by_email(db, user_mail)
    #user = crud.get_user_by_id(db, user_id.id)
    if not user:
        raise HTTPException(status_code=404, detail="Utente non trovato")
    try:
        pdf_bytes = generate_report(db, user.id)
        return StreamingResponse(BytesIO(pdf_bytes),
                                 media_type="application/pdf",
                                 headers={"Content-Disposition": f"attachment; filename=rapport_categorie_{user.nome}.pdf"})
    except Exception as e:
        print("Errore:", e)
        raise HTTPException(status_code=404, detail=str(e))