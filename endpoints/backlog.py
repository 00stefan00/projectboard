"""This is an example usage of fastapi-sso.
"""
from utils.auth_utils import get_current_user
from fastapi import APIRouter
from fastapi import Depends
from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.exc import IntegrityError
from schemas.auth_schemas import SystemUser
from starlette.requests import Request
from typing import Annotated

from models.models import Projectinfo

templates = Jinja2Templates(directory="templates")
router = APIRouter()


@router.get("/backlog", response_class=HTMLResponse)
async def backlog(request: Request, current_user: Annotated[SystemUser, Depends(get_current_user)]):
    items = Projectinfo.get_projectinfo()
    data = {
        "items": items
    }
    return templates.TemplateResponse("backlog.html", {"request": request, "data": data})


@router.post("/backlog")
async def submit_form(request: Request, current_user: Annotated[SystemUser, Depends(get_current_user)]):
    form_data = await request.form()
    title = form_data.get("title")
    description = form_data.get("description")
    priority = form_data.get("priority")
    load = form_data.get("load")
    owner = form_data.get("owner")
    deadline = form_data.get("deadline")

    projectinfo = Projectinfo(
        name=title,
        description=description,
        priority=priority,
        load=load,
        owner=owner,
        deadline=deadline,
    )

    try:
        projectinfo.save_to_database()
    except (TypeError, IntegrityError) as sql_error:
        data = {
            "error_message": sql_error
        }
        return templates.TemplateResponse("/errors/http500.html", {"request": request, "data": data})
    
    return RedirectResponse("/backlog", status_code=303)
