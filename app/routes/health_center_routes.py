from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
from typing import List
from fastapi import APIRouter, HTTPException, File, UploadFile

from app.models.health_care_model import BasicPatientInfo, PatientInfo, Prescription
from firebase_admin import auth, firestore
from app.db import get_db
from app.hardcorder import WARDEN_EMAIL, MOTHER_EMAIL
from firebase_admin import credentials, firestore, initialize_app, storage
import firebase_admin


# Initialize Firebase Admin SDK
# Replace with your service account key path
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()


router = APIRouter()


def __send_mail(
    sender_email,
    recipient_email,
    subject,
    body,
    smtp_server,
    smtp_port,
    smtp_user,
    smtp_password,
):
    """
    Send an email from `sender_email` to `recipient_email` with the given `subject` and `body`.
    SMTP server details (host, port, user, password) must be provided.

    :param sender_email: Sender's email address
    :param recipient_email: Recipient's email address
    :param subject: Subject of the email
    :param body: Body of the email
    :param smtp_server: SMTP server host
    :param smtp_port: SMTP server port
    :param smtp_user: SMTP user for authentication
    :param smtp_password: SMTP password for authentication
    """
    try:
        # Create a multipart message and set headers
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = recipient_email
        message["Subject"] = subject

        # Add body to email
        message.attach(MIMEText(body, "plain"))

        # Create secure connection with server and send email
        with smtplib.SMTP(host=smtp_server, port=smtp_port) as server:
            server.starttls()  # Secure the connection
            server.login(smtp_user, smtp_password)
            text = message.as_string()
            server.sendmail(sender_email, recipient_email, text)

        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email. Error: {e}")


def send_mail_gmail(recv_mail, subject, body):
    sender_email = "shreyasmohanty0228@gmail.com"
    app_pass = "vhgs bncj mgrw dtqs"

    __send_mail(
        sender_email=sender_email,
        recipient_email=recv_mail,
        subject=subject,
        body=body,
        smtp_server="smtp.gmail.com",
        smtp_port=587,
        smtp_user=sender_email,
        smtp_password=app_pass,
    )


@router.post("/doctor/save-prescription")
async def add_patient(patient_info: PatientInfo):
    db = get_db()
    try:
        patients_collection = db.collection("patients")
        doc_ref = patients_collection.add(patient_info.to_firebase())
        send_mail_gmail(
            WARDEN_EMAIL,
            "Patient Added",
            f"Patient {patient_info.name} has been added successfully.",
        )
        send_mail_gmail(
            MOTHER_EMAIL,
            "Patient Added",
            f"Patient {patient_info.name} has been added successfully.",
        )
        return {"message": "Patient added successfully", "doc_id": doc_ref[1].id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/get/")
def get_patient_data(name: str, disease: str):
    db = get_db()
    patients_ref = db.collection("patients")
    print("Before Firestore query")
    patients = (
    patients_ref.where("name", "==", name).where("disease", "==", disease).stream()
)
    print("After Firestore query")
    patients_list = [doc.to_dict() for doc in patients]
    if not patients_list:
        raise HTTPException(status_code=404, detail="Patient not found")

    return patients_list[0]

@router.get("/getByBlock/")
def get_patient_data(block: str):
    db = get_db()
    patients_ref = db.collection("patients")
    print("Before Firestore query")
    patients = (
    patients_ref.where("block", "==", block).stream()
)
    print("After Firestore query")
    patients_list = [doc.to_dict() for doc in patients]
    if not patients_list:
        raise HTTPException(status_code=404, detail="Patient not found")

    return patients_list

@router.get("/getByStatus/")
def get_patient_data(status: str):
    db = get_db()
    patients_ref = db.collection("patients")
    print("Before Firestore query")
    patients = (
    patients_ref.where("status", "==", status).stream()
)
    print("After Firestore query")
    patients_list = [doc.to_dict() for doc in patients]
    if not patients_list:
        raise HTTPException(status_code=404, detail="Patient not found")

    return patients_list

@router.get("/getEmergency/")
def get_patient_data():
    db = get_db()
    patients_ref = db.collection("emergency")
    print("Before Firestore query")
    patients = (
    patients_ref.stream()
)
    print("After Firestore query")
    patients_list = [doc.to_dict() for doc in patients]
    if not patients_list:
        raise HTTPException(status_code=404, detail="Patient not found")

    return patients_list

@router.get("/get_students/{reg_no}")
def get_student_data(reg_no: str):
    db = get_db()
    students_ref = db.collection("students")
    students = students_ref.where("reg_no", "==", reg_no).stream()

    if not students:
        raise HTTPException(status_code=404, detail="Student not found")

    return [doc for doc in students][0].to_dict()


@router.get("/getPatients")
async def get_all_patients():
    try:
        db = firestore.client()
        patients = db.collection('patients').stream()

        all_patients = []
        for patient in patients:
            patient_dict = patient.to_dict()
            patient_dict['id'] = patient.id
            all_patients.append(patient_dict)

        return all_patients
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# @router.post("/doctor/save-prescription")
# async def save_prescription(prescription: Prescription):
#     try:
#         # Add prescription to Firestore
#         doc_ref = db.collection("Prescriptions").document()
#         doc_ref.set(prescription.dict())
#         return {"message": "Prescription saved successfully"}
#     except Exception as e:
#         raise HTTPException(
#             status_code=500, detail=f"Error saving prescription: {str(e)}"
#         )


@router.post("/upload/")
async def upload_files(files: List[UploadFile] = File(...)):
    urls = []
    for file in files:
        # Upload file to Firebase Storage
        bucket = storage.bucket()
        blob = bucket.blob(file.filename)
        blob.upload_from_file(file.file)

        # Get download URL
        url = blob.generate_signed_url(
            expiration=3600)  # URL expires in 1 hour
        urls.append(url)

    return {"urls": urls}
