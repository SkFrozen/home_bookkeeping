from datetime import datetime

from pydantic import BaseModel


class CustomeBaseSchema(BaseModel):
    class Config:
        json_encoders = {
            datetime: lambda v: v.strftime("%d-%m-%Y %H:%M:%S"),
        }
