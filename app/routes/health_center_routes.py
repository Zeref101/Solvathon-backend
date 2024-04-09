from fastapi import APIRouter, HTTPException

from app.models.health_care_model import PatientInfo
from firebase_admin import auth, firestore
from app.db import get_db

router = APIRouter()


@router.post("/add/")
async def add_patient(patient_info: PatientInfo):
    db = get_db()
    try:
        patients_collection = db.collection("patients")
        doc_ref = patients_collection.add(patient_info.to_firebase())
        return {"message": "Patient added successfully", "doc_id": doc_ref[1].id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
