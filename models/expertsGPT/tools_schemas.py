from pydantic import BaseModel
from models.common_schemas import GetCurrentTime


class GetTimings(BaseModel):
    expertId: str


class GetSarathiSchedules(BaseModel):
    expertName: str
