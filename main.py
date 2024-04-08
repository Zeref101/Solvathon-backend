from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
import firebase_admin
from firebase_admin import credentials, auth
from pydantic import BaseModel
from routes.authentication import UserSignup, UserLogin, signup, login, get_user


if not firebase_admin._apps:
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class UserSignup(BaseModel):
    email: str
    password: str
    name: str


class UserLogin(BaseModel):
    email: str
    password: str


@app.post("/signup")
async def signup_endpoint(user: UserSignup):
    return await signup(user)


@app.post("/login")
async def login_endpoint(user: UserLogin, response: Response):
    return await login(user, response)


@app.get("/user/{uid}")
async def getUser(uid: str):
    return await get_user(uid)


@app.get("/")
def read_root():
    return {"Hello": "World"}
