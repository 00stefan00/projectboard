from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from models.models import User
from schemas.auth_schemas import SystemUser
from schemas.auth_schemas import TokenSchema
from schemas.auth_schemas import UserAuth
from schemas.auth_schemas import UserOut
from starlette.requests import Request
from utils import auth_utils
from utils.auth_utils import get_current_user
from utils.auth_utils import get_hashed_password

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.post('/signup', summary="Create new user", response_model=UserOut)
async def create_user(data: UserAuth):
    # querying database to check if user already exist
    user = User.get_users()
    if user is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exist"
        )
    user = User(
        email=data.email,
        hashed_password=get_hashed_password(data.password),
        full_name="anonymouse"
    )
    
    return user


@router.get("/logoff", response_class=HTMLResponse)
async def logoff(request: Request):
    data = {
        "request": request
    }
    response = templates.TemplateResponse("homepage.html", data)
    response.delete_cookie("access_token")
    return response


@router.get("/login", response_class=HTMLResponse)
async def loginpage(request: Request):
    data = {
        "request": request
    }
    return templates.TemplateResponse("login.html", data)


@router.post('/login', summary="Create access and refresh tokens for user", response_model=TokenSchema)
async def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends()):
    
    found_user = None
    for user in User.get_users():
        if user.email == form_data.username:
            found_user = user

    if found_user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )

    hashed_pass = found_user.hashed_password
    if not auth_utils.verify_password(form_data.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )

    access_token = auth_utils.create_access_token(user.email)
    refresh_token = auth_utils.create_refresh_token(user.email)

    data = {
        "page": "Home page",
        "request": request,
        "user": UserOut(**user.dict())
    }
    response = templates.TemplateResponse("homepage.html", data)
    response.set_cookie(
        key="access_token", value=f"Bearer {access_token}", httponly=True
    )
    response.set_cookie(
        key="refresh_token", value=f"Bearer {refresh_token}", httponly=True
    )
    return response


@router.get('/me', summary='Get details of currently logged in user', response_model=UserOut)
async def get_me(user: SystemUser = Depends(get_current_user)):
    return user
