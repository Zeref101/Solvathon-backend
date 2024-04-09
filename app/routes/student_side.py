from fastapi import APIRouter

from app.db import get_db
from app.models.student_side_models import AmbulanceRequest

router = APIRouter()


@router.post("/order_ambulance")
def order_ambulance(amb_data: AmbulanceRequest):
    db = get_db()
    ambulance_req_ref = db.collection("ambulance_req")
    ambulance_req_ref.add(amb_data.to_firebase())
    return {"message": "Ambulance request added successfully"}


@router.get("/get_ambulance_requests")
def get_ambulance_requests():
    db = get_db()
    ambulance_req_ref = db.collection("ambulance_req")
    ambulance_req = ambulance_req_ref.stream()
    return [doc.to_dict() for doc in ambulance_req]


@router.get("/get_pending_ambulance_requests")
def get_pending_ambulance_requests():
    db = get_db()
    ambulance_req_ref = db.collection("ambulance_req")
    ambulance_req = ambulance_req_ref.where("approved", "==", False).stream()
    return [doc.to_dict() for doc in ambulance_req]
