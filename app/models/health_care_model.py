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


class PatientInfo(BaseModel):
    name: str
    block: Block
    room: int
    disease: str
    date: datetime.date
    prescription_given: List[str]
    remarks: List[str]
    reg_num: str

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
