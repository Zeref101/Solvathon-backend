from fastapi import HTTPException, Response
import firebase_admin
from firebase_admin import auth, firestore
from app.models.authentication_model import UserSignup, UserLogin
from fastapi import APIRouter

router = APIRouter()


@router.post("/signup")
async def signup(user: UserSignup):
    try:
        user_record = auth.create_user(email=user.email, password=user.password)
        if user_record:
            db = firestore.client()
            user_ref = db.collection("Users").document(user_record.uid)
            user_ref.set({"college_email": user.email})
        return {"message": "User created successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login")
async def login(user: UserLogin, response: Response):
    try:
        user_record = auth.get_user_by_email(user.email)
        if not user_record:
            raise HTTPException(status_code=400, detail="Invalid credentials")
        response.set_cookie(key="uid", value=user_record.uid, max_age=86400)
        return {"uid": user_record.uid}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/user/{uid}")
async def get_user(uid: str):
    try:
        db = firestore.client()
        user_doc = db.collection("Users").document(uid).get()
        if user_doc.exists:
            return user_doc.to_dict()
        else:
            raise HTTPException(status_code=404, detail="User not found")
    except firestore.FirestoreError as e:
        raise HTTPException(status_code=500, detail=str(e))
