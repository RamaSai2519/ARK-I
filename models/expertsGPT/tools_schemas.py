from pydantic import BaseModel


class GetSarathiDetails(BaseModel):
    phoneNumber: str


class GetTimings(BaseModel):
    expertId: str


class GetSarathiSchedules(BaseModel):
    expertName: str
