from pydantic import BaseModel
from models.common_schemas import GetCurrentTime


class GetSlots(BaseModel):
    date: str
    expertId: str


class GetSarathiSchedules(BaseModel):
    expertName: str
