import os
import shutil
from fastapi import APIRouter, File, Form, Request, Depends, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from routes.route import router
from config.database import client, db, collection_name
from schema.schemas import list_serial, individual_serial_odpoved, individual_serial_portfolio
from datetime import datetime
from utils.functions import get_year, get_image_paths, slugify

router_prezentacia = APIRouter(tags=["prezentacia"])

# Static and template directories
router_prezentacia.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Directory where images are stored
IMAGE_DIR = "static/img"


@router_prezentacia.get("/", response_class=HTMLResponse)
async def home(request: Request, current_year: dict = Depends(get_year)):
    return templates.TemplateResponse("home.html", {"request": request, **current_year})

@router_prezentacia.get("/portfolio", response_class=HTMLResponse)
async def portfolio_view(request: Request, current_year: dict = Depends(get_year)):
    """Return the portfolio page."""
    return templates.TemplateResponse("portfolio.html", {"request": request, **current_year})

@router_prezentacia.get("/portfolio_short", response_class=HTMLResponse)
async def portfolio_view(request: Request, current_year: dict = Depends(get_year)):
    """Return the portfolio page."""
    portfolio_data = list_serial(db.portfolio_data.find(), res_func='individual_serial_portfolio')
    # print(portfolio_data)
    return templates.TemplateResponse("portfolio_short.html", {"request": request, "portfolio_data": portfolio_data, **current_year})

@router_prezentacia.get("/portfolio/items", response_class=HTMLResponse)
async def portfolio_items(request: Request, current_year: dict = Depends(get_year)):
    """
    Return the portfolio items page.

    The page displays a list of portfolio items, including images and descriptions.

    The data is currently hard-coded for demonstration purposes. In the future, it
    should be replaced with a database query.
    """
    def remove_before_slash(value):
        if '/' in value:
            return value.split('/', 1)[1]
        return value

    data = list_serial(db.portfolio_data.find(), res_func='individual_serial_portfolio')
    # PATH = 'templates/projekty'
    # portfolio_data = [{'title': f, 'path': os.path.join(PATH, f)} for f in os.listdir('templates/projekty')]
    for projekt in data:
        projekt['slug'] = os.path.join('projekty', slugify(projekt['title']))
        projekt['text'] = [p for p in projekt['text'].splitlines() if p != '']
        # print(projekt)
        # print(f"updating DB db.hradil.portfolio_data with slug: {projekt['slug']}")   
        db.portfolio_data.update_one({'title': projekt['title']}, {'$set': {'slug': projekt['slug']}})
        projekt['slug_id'] = remove_before_slash(projekt['slug'])
    return templates.TemplateResponse("partials/portfolio_items.html", {"request": request, "portfolio_data": data, **current_year})


@router_prezentacia.get("/projekty/{slug}", response_class=HTMLResponse)
async def projekt(request: Request, slug: str, current_year: dict = Depends(get_year)):
    # print('slug', slug)
    projekt = individual_serial_portfolio(db.portfolio_data.find_one({'slug': f'projekty/{slug}'}))
    projekt['text'] = [p for p in projekt['text'].splitlines() if p != '']
    # print(projekt)
    return templates.TemplateResponse("projekt.html", {"request": request, "data": projekt, **current_year})

@router_prezentacia.get("/kontakt", response_class=HTMLResponse)
async def contact_view(request: Request, current_year: dict = Depends(get_year)):
    """Return the contact page."""
    return templates.TemplateResponse("kontakt.html", {"request": request, **current_year})

@router_prezentacia.post("/kontakt")
async def kontakt(fname: str = Form(...), lname: str = Form(...), phone: str = Form(...), email: str = Form(...), message: str = Form(...)):
    db.odpovede.insert_one({"fname": fname, 
                            "lname": lname, 
                            "phone": phone, 
                            "email": email, 
                            "message": message, 
                            "date": datetime.now()
                            })
    response_content = f"<p>Ďakujem veľmi pekne {fname} {lname} za zanechanie správy! Vaša správa \"{message}\" bola zaznamenaná.</p><p>telefónne číso: {phone}</p><p>email: {email}</p>"
    return HTMLResponse(content=response_content)


@router_prezentacia.get("/galeria", response_class=HTMLResponse)
async def galeria(request: Request):
    # List image file paths
    images = os.listdir(IMAGE_DIR)
    image_paths = get_image_paths(image_dir=IMAGE_DIR)
    return templates.TemplateResponse("galeria.html", {"request": request, "images": image_paths})

@router_prezentacia.get("/galeria/items", response_class=HTMLResponse)
async def gallery_items(request: Request):
    images = os.listdir(IMAGE_DIR)
    image_paths = get_image_paths(image_dir=IMAGE_DIR)
    return templates.TemplateResponse("partials/gallery_items.html", {"request": request, "images": image_paths})

@router_prezentacia.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    file_location = f"{IMAGE_DIR}/{file.filename}"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"info": "Image uploaded successfully"}

