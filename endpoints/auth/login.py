"""This is an example usage of fastapi-sso.
"""
from fastapi import APIRouter
from starlette.requests import Request
from fastapi.templating import Jinja2Templates


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/login/")
def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


# @router.post("/login/")
# async def submit_form(request: Request):
#     form_data = await request.form()
#     email = form_data.get("email")
#     password = form_data.get("password")

#     try:
#         projectinfo.save_to_database()
#     except (TypeError, IntegrityError) as sql_error:
#         data = {
#             "error_message": sql_error
#         }
#         return templates.TemplateResponse("/errors/http500.html", {"request": request, "data": data})
    
#     return RedirectResponse("/backlog", status_code=303)
