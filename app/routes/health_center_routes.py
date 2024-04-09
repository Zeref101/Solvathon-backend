from typing import List
from fastapi import APIRouter, HTTPException

from app.models.health_care_model import BasicPatientInfo, PatientInfo
from firebase_admin import auth, firestore
from app.db import get_db
import vonage


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


@router.get("/get/")
def get_patient_data(name: str, disease: str):
    db = get_db()
    patients_ref = db.collection("patients")
    patients = (
        patients_ref.where("name", "==", name).where("disease", "==", disease).stream()
    )

    if not patients:
        raise HTTPException(status_code=404, detail="Patient not found")

    return [doc for doc in patients][0].to_dict()


@router.get("/get_student/{reg_no}")
def get_student_data(reg_no: str):
    db = get_db()
    students_ref = db.collection("students")
    students = students_ref.where("reg_no", "==", reg_no).stream()

    if not students:
        raise HTTPException(status_code=404, detail="Student not found")

    return [doc for doc in students][0].to_dict()
