from typing import List
from pydantic import BaseModel
from enum import Enum
import datetime


class Block(str, Enum):
    A = "A"
    B = "B"
    C = "C"
    D1 = "D1"
    D2 = "D2"


class SeverityColorCode(str, Enum):
    red = "red"
    green = "green"
    blue = "blue"


class BasicPatientInfo(BaseModel):
    name: str
    block: Block
    room: int
    disease: str
    date: datetime.date
    status: str



class PatientInfo(BasicPatientInfo):
    medicines: List[dict]
    remarks: str = ""
    reg_num: str
    hospitalization: bool
    severity: int

    def to_firebase(self):
        """
        Convert the model to a dictionary format that is compatible with Firebase.
        In particular, convert datetime.date to a string.
        """
        data_dict = self.dict()
        data_dict["date"] = (
            self.date.isoformat()
        )  # Convert date to ISO 8601 string format
        # Handle any other special data type formatting here.
        return data_dict


class Prescription(BaseModel):
    name: str
    block: str
    room: str
    disease: str
    date: str
    severity: int
    medicines: list
    hospitalization: bool
