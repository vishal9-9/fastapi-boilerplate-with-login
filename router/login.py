from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from helpers.response_parser import response
from helpers import oauth
from database.config import get_db
from models import user
from schemas.register import RegisterSchema

router = APIRouter(tags=["Account"])


@router.get('/')
def index():
    return response(message="The server is working", code=200, data=None)


@router.post('/register')
def register(payload: RegisterSchema, db: Session = Depends(get_db)):
    try:
        if payload:
            if db.query(user.User).filter(user.User.username == payload.username).first():
                return response(message="User already present", code=400, data=None)
            payload.password = oauth.get_password_hash(payload.password)
            db_item = user.User(**payload.dict())
            db.add(db_item)
            db.commit()
            return response(message="Account created Successfully", code=201, data=None)
    except Exception as err:
        raise HTTPException(status_code=500, detail={
                            "status": f"Internal Server Error Occurred. {err}"})


@router.post('/login')
def login(
        # payload: RegisterSchema,
        form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    try:
        if form_data:
            payload = RegisterSchema(username='', password='')
            if form_data:
                payload.username = form_data.username
                payload.password = form_data.password
            data = db.query(user.User).filter(
                user.User.username == payload.username).first()
            if user is None:
                return response(message="User not found", code=404, data=None)
            verify = oauth.verify_password(payload.password, data.password)
            if verify:
                token = oauth.create_access_token({"sub": f"{data.id}"})
                return response(message="Login successful", code=200, access_token=token)
            return response(message="Invalid credentials", code=400, data=None)
    except Exception as err:
        raise HTTPException(status_code=500, detail={
                            "status": f"Internal Server Error Occurred. {err}"})


@router.get('/home')
def home(current_user: user.User = Depends(oauth.get_current_user)):
    if current_user:
        return response(message="You're at home", code=200, data={"current_user": current_user.username, "id": current_user.id})
