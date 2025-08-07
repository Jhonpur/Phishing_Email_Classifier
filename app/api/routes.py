from fastapi import APIRouter, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse,StreamingResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import sessionmaker, Session
from app.database.db import engine, Base, SessionLocal
from app.database import crud, models, schemas
from app.utils.pdf_generator import generate_report
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo
from io import BytesIO
from predict_spam import predict_spam  # Your spam detection function

router = APIRouter()
templates = Jinja2Templates(directory="Frontend/templates")

Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal() 


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("base.html", {"request": request})


def format_email_date(date):
    # Se l'orario non ha timezone, assumiamo che sia in UTC e lo convertiamo
    if date.tzinfo is None:
        date = date.replace(tzinfo=ZoneInfo("UTC"))

    # Convertiamo da UTC a Europe/Rome
    date = date.astimezone(ZoneInfo("Europe/Rome"))
    now = datetime.now(ZoneInfo("Europe/Rome"))

    if date.date() == now.date():
        return date.strftime("%H:%M")
    return date.strftime("%d/%m")


@router.get("/inbox", response_class=HTMLResponse)
async def inbox(request: Request, user_mail: str, selected_email_id: int = None):
    user = crud.get_user_by_email(db, user_mail)
    if not user:
        raise HTTPException(status_code=404, detail="User not found") # oppure si ritorn un messagio

    # Ottengo tutte le email ricevute
    emails = user.received

    # Prendiamo solo le mail che non hanno status delete = 1/2, e che non siano spam
    emails = [email for email in emails if not crud.get_user_email_delete_status(db, user.id, email.id)and not email.stato_spam]

    # Ordina email per data (più recenti prima)
    sorted_emails = sorted(emails, key=lambda x: x.data, reverse=True)

    # Controllo stato per pop-up di conferma email inviata
    sent = request.query_params.get("sent") == "true"

    # Aggiungi date formattate
    for email in sorted_emails:
        email.formatted_date = format_email_date(email.data)
        email.is_read = crud.get_user_email_read_status(db, user.id, email.id)


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
        "user_mail": user_mail,
        "current_page": "inbox"
    })

# Caricamento del form
@router.get("/send", response_class=HTMLResponse)
async def send_get(request: Request, user_mail: str, reply_to: int = None, forward: int = None):
    user = crud.get_user_by_email(db, user_mail)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    email_data = {
        "destinatario": "",
        "oggetto": "",
        "descrizione": ""
    }
    
    if reply_to:
        # Risposta → Recupera email e precompila il destinatario e l’oggetto
        original = crud.get_email_by_id(db, reply_to)
        if original:
            email_data["destinatario"] = original.email_sorgente
            email_data["oggetto"] = f"Re: {original.oggetto}"
            email_data["descrizione"] = f"\n\n--- Original message ---\n{original.descrizione}"

    elif forward:
        # Inoltro → Recupera email e precompila oggetto e testo (destinatario vuoto)
        original = crud.get_email_by_id(db, forward)
        if original:
            email_data["oggetto"] = f"Fwd: {original.oggetto}"
            email_data["descrizione"] = f"\n\n--- Message forwarded ---\nFrom: {original.email_sorgente}\n{original.descrizione}"

    return templates.TemplateResponse("send.html", {
        "request": request,
        "user_mail": user_mail,
        "email_data": email_data,
        "reply_to": reply_to,
        "forward": forward,
        "current_page": "send"
    })

# Invio del form
@router.post("/send", response_class=HTMLResponse)
async def post_send_email(request: Request,
                          user_mail: str = Form(...),
                          recipient: str = Form(...),
                          subject: str = Form(...),
                          content: str = Form(...),
                          reply_to: int = Form(None),
                          #db: Session = Depends(get_db)
                          ):
    mittente = user_mail
    #mittente = request.query_params.get("user_mail")
    if not mittente:
        return HTMLResponse("Sender missing from URL", status_code=400)

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
    #email_id_risposta = crud.get_email_by_id(db, email_id)

    if not utente_sorgente or not utente_destinario:
        return HTMLResponse(content="Invalid sender or recipient", status_code=400)

    # Save the email to the DB
    crud.create_email_with_user_relation(
        db=db,
        user_id_sorgente=utente_sorgente.id,
        user_id_destinatario=utente_destinario.id,
        email_sorgente=mittente,
        email_destinatario=recipient,
        descrizione=content,
        oggetto=subject,
        data=datetime.now(timezone.utc),
        url=url,
        stato_spam=is_spam,
        spam_reason=spam_reasons,
        spam_probability=int(spam_probability*100),
        email_id_risposta=reply_to
    )

    return RedirectResponse(url=f"/inbox?user_mail={mittente}&sent=true", status_code=303)


@router.get("/sent", response_class=HTMLResponse)
async def sent(request: Request, user_mail: str, email_id: int = None):
    user = crud.get_user_by_email(db, user_mail)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Ottieniamo le email inviate da questo utente
    emails = crud.get_emails_sent_by_user(db, user.id)

    # Prendiamo solo le mail che non hanno status delete = 1/2
    emails = [email for email in emails if not crud.get_user_email_delete_status(db, user.id, email.id)]

    # Ordina email per data (più recenti prima)
    sorted_emails = sorted(emails, key=lambda x: x.data, reverse=True)

    # Formatta la data per ogni email e imposta come lette
    for email in emails:
        email.formatted_date = format_email_date(email.data)
        email.is_read = True  # Forza lo stato come "letto" per le email inviate

    # Recupera l’email selezionata
    selected_email = None
    if email_id:
        selected_email = next((email for email in emails if email.id == email_id), None)
        if selected_email:
            selected_email.is_read = True  # opzionale, qui è puramente visivo

    # Passa tutto al template
    return templates.TemplateResponse("sent.html", {
        "request": request,
        "emails": sorted_emails,
        "selected_email": selected_email,
        "user_mail": user_mail,
        "current_page": "sent"
    })


@router.get("/spam", response_class=HTMLResponse)
async def spam(request: Request, user_mail: str, email_id: int = None):
    user = crud.get_user_by_email(db, user_mail)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Ottieni le email di spam per l’utente
    emails = crud.get_spam_emails_by_user(db, user.id)

    # Ordina email per data (più recenti prima)
    sorted_emails = sorted(emails, key=lambda x: x.data, reverse=True)

    # Aggiungi date formattate e stato lettura
    for email in emails:
        email.formatted_date = format_email_date(email.data)
        email.is_read = crud.get_user_email_read_status(db, user.id, email.id)

    # Seleziona email se specificato
    selected_email = None
    if email_id:
        selected_email = next((email for email in emails if email.id == email_id), None)
        if selected_email:
            crud.update_user_email_read_status(db, user.id, selected_email.id)

    return templates.TemplateResponse("spam.html", {
        "request": request,
        "emails": sorted_emails,
        "selected_email": selected_email,
        "user_mail": user_mail,
        "current_page": "spam"
    })


@router.get("/trash", response_class=HTMLResponse)
async def trash(request: Request, user_mail: str, email_id: int = None):
    user = crud.get_user_by_email(db, user_mail)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Recupera le email eliminate per l'utente
    emails = crud.get_deleted_emails_by_user(db, user.id)

    # Mostriamo solo le mail con stato_delete 1 (mail solo spostate nel cestino)
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
        "user_mail": user_mail,
        "current_page": "trash"
    })


# Sposta le mail nel cestino
@router.post("/delete_email", response_class=HTMLResponse)
async def delete_email(request: Request, user_mail: str = Form(...), email_id: int = Form(...), current_page: str = Form(...)):
    # 1. Otteniamo l’utente
    user = crud.get_user_by_email(db, user_mail)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

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
        raise HTTPException(status_code=404, detail="User not found")

    crud.delete_user_emai_definitivelyl(db, user.id, email_id)

    # Dopo la cancellazione, torna al cestino
    return RedirectResponse(url=f"/trash?user_mail={user_mail}", status_code=303)


@router.get("/report_pdf", response_class=StreamingResponse)
def report_category(user_mail:str):
    user = crud.get_user_by_email(db, user_mail)
    #user = crud.get_user_by_id(db, user_id.id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    try:
        pdf_bytes = generate_report(db, user.id)
        return StreamingResponse(BytesIO(pdf_bytes),
                                 media_type="application/pdf",
                                 headers={"Content-Disposition": f"attachment; filename=rapport_categorie_{user.nome}.pdf"})
    except Exception as e:
        print("Error:", e)
        raise HTTPException(status_code=404, detail=str(e))