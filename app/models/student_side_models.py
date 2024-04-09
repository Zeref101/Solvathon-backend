from pydantic import BaseModel
from datetime import datetime


class AmbulanceRequest(BaseModel):
    reg_num: str
    issue: str
    approved: bool = False
    datetime_created: datetime = datetime.now()

    def to_firebase(self):
        data_dict = dict(self)
        data_dict["datetime_created"] = self.datetime_created.isoformat()
        return data_dict
