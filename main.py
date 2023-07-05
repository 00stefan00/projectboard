from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from endpoints import backlog
from endpoints.auth import login
from fastapi import HTTPException
from models.models import Projectinfo
from models.models import create_db_and_tables
from schemas.auth_schemas import UserOut
from utils.auth_utils import get_current_user


app = FastAPI()
# app.include_router(basicAuth.router)
app.include_router(backlog.router)
app.include_router(login.router)

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

create_db_and_tables()


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    user = await get_current_user(request, request.cookies.get('access_token').split()[-1])

    data = {
        "request": request,
        "page": "Home page",
        "user": UserOut(**user.dict())
    }
    return templates.TemplateResponse("homepage.html", data)


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


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exception):
    data = {
        "page": "Home page",
        "request": request,
        "exception": exception
    }
    return templates.TemplateResponse("login.html", data)
