from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from models.models import create_db_and_tables, Projectinfo
from endpoints.auth import basicAuth, login
from endpoints import backlog


app = FastAPI()
app.include_router(basicAuth.router)
app.include_router(backlog.router)
app.include_router(login.router)

app.add_exception_handler(basicAuth.NotAuthenticatedException, basicAuth.authentication_exception_handler)


templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

create_db_and_tables()


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    data = {
        "page": "Home page"
    }
    return templates.TemplateResponse("homepage.html", {"request": request, "data": data})


@app.get("/page/{page_name}", response_class=HTMLResponse)
async def page(request: Request, page_name: str):
    data = {
        "page": page_name
    }
    return templates.TemplateResponse("homepage.html", {"request": request, "data": data})


@app.get("/timeline", response_class=HTMLResponse)
async def timeline(request: Request):
    items = Projectinfo.get_projectinfo()
    data = {
        "items": items
    }
    return templates.TemplateResponse("timeline.html", {"request": request, "data": data})


@app.post("/api/projectinfo")
async def create_projectinfo(projectinfo: Projectinfo):
    return projectinfo
