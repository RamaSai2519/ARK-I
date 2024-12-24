from pydantic import BaseModel


class GetTimings(BaseModel):
    expertId: str


class GetSarathiSchedules(BaseModel):
    expertName: str
