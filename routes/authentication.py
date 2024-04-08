from fastapi import HTTPException, Response
from pydantic import BaseModel
import firebase_admin
from firebase_admin import auth


class UserSignup(BaseModel):
    email: str
    password: str
    name: str


class UserLogin(BaseModel):
    email: str
    password: str


async def signup(user: UserSignup):
    try:
        user_record = auth.create_user(
            email=user.email,
            password=user.password
        )
        return {"uid": user_record.uid}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


async def login(user: UserLogin, response: Response):
    try:
        user_record = auth.get_user_by_email(user.email)
        if not user_record:
            raise HTTPException(status_code=400, detail="Invalid credentials")
        response.set_cookie(key="uid", value=user_record.uid, max_age=86400)
        return {"uid": user_record.uid}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
