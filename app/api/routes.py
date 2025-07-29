from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from datetime import datetime, timedelta

router = APIRouter()
templates = Jinja2Templates(directory="Frontend/templates")

# Dati per simulare email dal database
MOCK_EMAILS = [
    {
        "id": 1,
        "sender": "noreply@banca-intesa.com",
        "subject": "Benvenuto in AGM Email",
        "preview": "Grazie per aver scelto il nostro servizio email. Questa è la tua inbox...",
        "date": datetime.now(),
        "content": "Gentile cliente, la informiamo che il suo conto è stato temporaneamente bloccato. Clicchi sul link per riattivarlo immediatamente.",
        "is_read": False
    },
    {
        "id": 2,
        "sender": "sistema@agmemail.com",
        "subject": "Notifica di sistema",
        "preview": "Il tuo account è stato configurato correttamente. Ora puoi...",
        "date": datetime.now() - timedelta(days=1),
        "content": "Il tuo account AGM Email è stato configurato correttamente. Puoi iniziare a usare tutte le funzionalità.",
        "is_read": True
    },
    {
        "id": 3,
        "sender": "privacy@agmemail.com",
        "subject": "Aggiornamento privacy",
        "preview": "Abbiamo aggiornato la nostra informativa sulla privacy...",
        "date": datetime.now() - timedelta(days=2),
        "content": "La nostra informativa sulla privacy è stata aggiornata per garantire maggiore trasparenza sui dati che raccogliamo.",
        "is_read": True
    },
    {
        "id": 4,
        "sender": "paypal-security@pp-verify.com",
        "subject": "Verifica urgente account PayPal",
        "preview": "Il tuo account PayPal necessita di verifica immediata per evitare...",
        "date": datetime.now() - timedelta(hours=3),
        "content": "ATTENZIONE: Il tuo account PayPal verrà sospeso tra 24 ore se non verifichi immediatamente la tua identità cliccando qui.",
        "is_read": False
    },
    {
        "id": 5,
        "sender": "newsletter@techcrunch.com",
        "subject": "Le ultime novità tech della settimana",
        "preview": "Scopri le startup più innovative del momento e le ultime...",
        "date": datetime.now() - timedelta(days=3),
        "content": "Questa settimana nel mondo tech: nuove AI breakthrough, acquisizioni miliardarie e le startup da tenere d'occhio.",
        "is_read": True
    }
]

# Dati per email inviate
MOCK_SENT_EMAILS = [
    {
        "id": 101,
        "recipient": "cliente@example.com",
        "subject": "Risposta alla tua richiesta",
        "preview": "Grazie per averci contattato. In allegato trovi...",
        "date": datetime.now() - timedelta(hours=2),
        "content": "Gentile Cliente, grazie per la sua richiesta. In allegato trova la documentazione richiesta.",
        "is_read": True
    },
    {
        "id": 102,
        "recipient": "team@agmemail.com",
        "subject": "Meeting di domani",
        "preview": "Ricordo a tutti il meeting di domani alle 10:00...",
        "date": datetime.now() - timedelta(days=1),
        "content": "Ciao team, ricordo a tutti il meeting di domani alle 10:00 in sala riunioni.",
        "is_read": True
    }
]

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

# Dati per cestino
MOCK_TRASH_EMAILS = [
    {
        "id": 301,
        "sender": "old-newsletter@example.com",
        "subject": "Newsletter vecchia",
        "preview": "Contenuto di una newsletter eliminata...",
        "date": datetime.now() - timedelta(days=7),
        "content": "Questa è una newsletter che hai eliminato la settimana scorsa.",
        "is_read": True
    }
]

@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("base.html", {"request": request})


def format_email_date(email_date):
    now = datetime.now()
    today = now.date()
    yesterday = today - timedelta(days=1)
    
    if email_date.date() == today:
        return email_date.strftime("%H:%M")
    elif email_date.date() == yesterday:
        return "Ieri"
    else:
        return email_date.strftime("%d/%m")


@router.get("/inbox", response_class=HTMLResponse)
async def inbox(request: Request, email_id: int = None):
    # Ordina email per data (più recenti prima)
    sorted_emails = sorted(MOCK_EMAILS, key=lambda x: x["date"], reverse=True)

    sent = request.query_params.get("sent") == "true"

    
    # Aggiungi date formattate
    for email in sorted_emails:
        email["formatted_date"] = format_email_date(email["date"])
    
    selected_email = None
    if email_id:
        selected_email = next((email for email in sorted_emails if email["id"] == email_id), None)
        # Segna come letta se selezionata
        if selected_email:
            selected_email["is_read"] = True
    
    return templates.TemplateResponse("inbox.html", {
        "request": request,
        "emails": sorted_emails,
        "selected_email": selected_email,
        "sent": sent
    })

# Caricamento del form
@router.get("/send", response_class=HTMLResponse)
async def get_send_email(request: Request):
    return templates.TemplateResponse("send.html", {"request": request})

# Invio del form
@router.post("/send", response_class=HTMLResponse)
async def post_send_email(
    request: Request,
    recipient: str = Form(...),
    subject: str = Form(...),
    content: str = Form(...)
):
    # Per ora stampa nel terminale o log — sostituirai con salvataggio nel DB
    print("EMAIL INVIATA:")
    print(f"Destinatario: {recipient}")
    print(f"Oggetto: {subject}")
    print(f"Contenuto: {content}")

    # In futuro: salva email nel database, triggera classificatore spam, ecc.

    # Esempio di risposta: mostra messaggio di successo
    return RedirectResponse(url="/inbox?sent=true", status_code=303)


@router.get("/sent", response_class=HTMLResponse)
async def sent(request: Request, email_id: int = None):
    sorted_emails = sorted(MOCK_SENT_EMAILS, key=lambda x: x["date"], reverse=True)
    
    for email in sorted_emails:
        email["formatted_date"] = format_email_date(email["date"])
    
    selected_email = None
    if email_id:
        selected_email = next((email for email in sorted_emails if email["id"] == email_id), None)
        if selected_email:
            selected_email["is_read"] = True
    
    return templates.TemplateResponse("sent.html", {
        "request": request,
        "emails": sorted_emails,
        "selected_email": selected_email
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
async def trash(request: Request, email_id: int = None):
    sorted_emails = sorted(MOCK_TRASH_EMAILS, key=lambda x: x["date"], reverse=True)
    
    for email in sorted_emails:
        email["formatted_date"] = format_email_date(email["date"])
    
    selected_email = None
    if email_id:
        selected_email = next((email for email in sorted_emails if email["id"] == email_id), None)
        if selected_email:
            selected_email["is_read"] = True
    
    return templates.TemplateResponse("trash.html", {
        "request": request,
        "emails": sorted_emails,
        "selected_email": selected_email
    })