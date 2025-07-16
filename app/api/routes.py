from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()

templates = Jinja2Templates(directory="Frontend/templates")

@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("base.html", {"request": request})

@router.get("/inbox", response_class=HTMLResponse)
async def inbox(request: Request):
    return templates.TemplateResponse("inbox.html", {"request": request})
