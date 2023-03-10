from jose import JWTError, jwt
from fastapi import Depends
from fastapi.exceptions import HTTPException
from datetime import datetime, timedelta
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer

from base.base_config import setting
from database.config import get_db
from models import user


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/login")

SECRET_KEY = setting.secret_key
ALGORITHM = setting.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = setting.access_token_expire_time

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict, expire_time=ACCESS_TOKEN_EXPIRE_MINUTES):
    to_encode = data.copy()
    if expire_time:
        expire = datetime.utcnow() + timedelta(minutes=expire_time)
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, SECRET_KEY)
    return token


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY)
        user_id: str = payload.get('sub')
        if user_id is None:
            raise HTTPException(
                detail="Invalid token", status_code=400)
    except JWTError:
        raise HTTPException(
            detail="Invalid token", status_code=400)
    db = get_db().__next__()
    curr_user = db.query(user.User).get(user_id)
    if curr_user is None:
        raise HTTPException(
            detail="No user Found", status_code=400)
    return curr_user
