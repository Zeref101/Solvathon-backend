from typing import List
from fastapi import APIRouter, HTTPException

from app.models.health_care_model import BasicPatientInfo, PatientInfo
from firebase_admin import auth, firestore
from app.db import get_db
from app.hardcorder import WARDEN_EMAIL, MOTHER_EMAIL

router = APIRouter()


import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


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


@router.post("/add/")
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
