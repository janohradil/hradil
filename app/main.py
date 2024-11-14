import os
import shutil
from fastapi import FastAPI, File, Request, Depends, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from datetime import datetime

app = FastAPI()

# Static and template directories
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# Directory where images are stored
IMAGE_DIR = "app/static/img"

# Dependency to provide the current year
def get_year():
    """Return the current year as a dictionary."""
    current_year = datetime.now().year
    return {"year": current_year}

def get_image_paths(exclude_substr: list[str]=['orig', '.png', '.ico']):
    # List image file paths
    images = os.listdir(IMAGE_DIR)
    cond = lambda img: not any(substr in img for substr in exclude_substr)
    image_paths = [f"/static/img/{img}" for img in images if cond(img)]
    return image_paths

@app.get("/", response_class=HTMLResponse)
async def home(request: Request, current_year: dict = Depends(get_year)):
    return templates.TemplateResponse("home.html", {"request": request, **current_year})

@app.get("/portfolio", response_class=HTMLResponse)
async def portfolio_view(request: Request, current_year: dict = Depends(get_year)):
    """Return the portfolio page."""
    return templates.TemplateResponse("portfolio.html", {"request": request, **current_year})

@app.get("/portfolio/items", response_class=HTMLResponse)
async def portfolio_items(request: Request, current_year: dict = Depends(get_year)):
    # Example portfolio data
    """
    Return the portfolio items page.

    The page displays a list of portfolio items, including images and descriptions.

    The data is currently hard-coded for demonstration purposes. In the future, it
    should be replaced with a database query.
    """
    portfolio_data = [
        {"title": "Drevený stôl", "description": "Ručne zhotovený drevený jedálenský stôl.", "img": "/static/img/table.jpg"},
        {"title": "Kuchynské skrine", "description": "Na mieru zhotovené kuchynské skrine.", "img": "/static/img/kuch_skrine.jpg"},
        {"title": "Oltár", "description": "Oltárny stôl na liturgické účely.", "img": "/static/img/oltar.jpg"},
        {"title": "Oltár", "description": "Anbóna na liturgické účely.", "img": "/static/img/anbona.jpg"}
    ]
    return templates.TemplateResponse("partials/portfolio_items.html", {"request": request, "portfolio_data": portfolio_data, **current_year})


@app.get("/kontakt", response_class=HTMLResponse)
async def contact_view(request: Request, current_year: dict = Depends(get_year)):
    """Return the contact page."""
    return templates.TemplateResponse("kontakt.html", {"request": request, **current_year})


@app.get("/galeria", response_class=HTMLResponse)
async def galeria(request: Request):
    # List image file paths
    images = os.listdir(IMAGE_DIR)
    image_paths = get_image_paths()
    return templates.TemplateResponse("galeria.html", {"request": request, "images": image_paths})

@app.get("/galeria/items", response_class=HTMLResponse)
async def gallery_items(request: Request):
    images = os.listdir(IMAGE_DIR)
    image_paths = get_image_paths()
    return templates.TemplateResponse("partials/gallery_items.html", {"request": request, "images": image_paths})

@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    file_location = f"{IMAGE_DIR}/{file.filename}"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"info": "Image uploaded successfully"}
