import os
import shutil
from fastapi import FastAPI, File, Request, Depends, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from routes.route import router
from routes.prezentacia import router_prezentacia
from datetime import datetime

app = FastAPI()

app.include_router(router)
app.include_router(router_prezentacia)


@router.get("/odpovede", response_class=HTMLResponse)
async def ziskaj_odpovede() -> HTMLResponse:
    """
    Get all responses from the database.
    
    Returns:
        HTMLResponse: A rendered HTML template with the responses.
    """
    try:
        odpovede = list_serial(collection_name.find())
    except Exception as e:
        print("error", str(e))
    else: 
        print(odpovede)
        return templates.TemplateResponse("odpovede.html", {"odpovede": odpovede})


@router.post("/odpovede")
async def posli_odpoved(request: Request):
    data = await request.form()
    meno = data.get("meno")
    priezvisko = data.get("priezvisko")
    telefon = data.get("telefon")
    sprava = data.get("sprava")
    odpoved = Odpoved(meno=meno, priezvisko=priezvisko, telefon=telefon, sprava=sprava)
    odpoved_id = collection_name.insert_one(odpoved.dict())
    return {"id": str(odpoved_id.inserted_id)}
