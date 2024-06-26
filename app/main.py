from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
import firebase_admin
from firebase_admin import credentials
from app.routes.authentication import UserSignup, UserLogin, signup, login, get_user
from app.routes import authentication, health_center_routes, student_side

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

app.include_router(authentication.router)
app.include_router(health_center_routes.router, prefix="/health_center")
app.include_router(student_side.router, prefix="/student_side")


@app.get("/")
def read_root():
    return {"Hello": "World"}
