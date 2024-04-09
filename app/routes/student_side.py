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
