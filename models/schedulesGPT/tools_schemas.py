from pydantic import BaseModel


class CancelSchedule(BaseModel):
    _id: str
