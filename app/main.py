from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api import routes

app = FastAPI()

# Collegamento ai file statici (es. Bootstrap personalizzato, immagini, ecc.)
app.mount("/static", StaticFiles(directory="Frontend/static"), name="static")

# Includi le rotte (es. /inbox)
app.include_router(routes.router)
