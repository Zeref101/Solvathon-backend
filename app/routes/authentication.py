from fastapi import HTTPException, Response
import firebase_admin
from firebase_admin import auth, firestore
from app.models.authentication_model import UserSignup, UserLogin
from fastapi import APIRouter
from typing import List
from pydantic import BaseModel
from fastapi import Query


router = APIRouter()


class Doctor(BaseModel):
    id: str
    details: str
    email: str
    name: str
    reviews: float
    specialist: str


@router.post("/signup")
async def signup(user: UserSignup):
    try:
        user_record = auth.create_user(
            email=user.email,
            password=user.password
        )
        if user_record:
            db = firestore.client()
            user_ref = db.collection('Users').document(user_record.uid)
            user_ref.set({
                'college_email': user.email
            })
        return {"message": "User created successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/student/login")
async def login(user: UserLogin, response: Response):
    try:
        user_record = auth.get_user_by_email(user.email)
        if not user_record:
            raise HTTPException(status_code=400, detail="Invalid credentials")

        db = firestore.client()
        doc_ref = db.collection('Users').document(user_record.uid)
        doc = doc_ref.get()
        if doc.exists:

            user_info = doc.to_dict()

            response.set_cookie(
                key="jwt", value=user_record.uid, max_age=86400)

            return user_info
        else:
            raise HTTPException(
                status_code=400, detail="User not found in Student collection")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/user/{uid}")
async def get_user(uid: str):
    try:
        db = firestore.client()
        user_doc = db.collection('Users').document(uid).get()
        if user_doc.exists:
            return user_doc.to_dict()
        else:
            raise HTTPException(status_code=404, detail="User not found")
    except firestore.FirestoreError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/doctor/login")
async def Doctorlogin(user: UserLogin, response: Response):
    try:
        user_record = auth.get_user_by_email(user.email)
        if not user_record:
            raise HTTPException(status_code=400, detail="Invalid credentials")

        db = firestore.client()
        doc_ref = db.collection('Doctor').document(user_record.uid)
        doc = doc_ref.get()
        if doc.exists:

            user_info = doc.to_dict()

            response.set_cookie(
                key="uid", value=user_record.uid, max_age=86400)

            return user_info
        else:
            raise HTTPException(
                status_code=400, detail="User not found in Student collection")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/doctor/getalldocs", response_model=List[Doctor])
async def get_all_docs():
    try:
        db = firestore.client()
        docs = db.collection('Doctor').stream()

        all_docs = []
        for doc in docs:
            doc_dict = doc.to_dict()
            doc_dict['id'] = doc.id
            all_docs.append(doc_dict)

        return all_docs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/doctor/getDetails", response_model=Doctor)
async def get_doctor(doctor_id: str = Query(...)):
    print("hello")
    try:
        db = firestore.client()
        doc = db.collection('Doctor').document(doctor_id).get()

        if not doc.exists:
            raise HTTPException(status_code=404, detail="Doctor not found")

        doc_dict = doc.to_dict()
        doc_dict['id'] = doc.id

        return doc_dict
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
