from pydantic import BaseModel
from shared.schemas import Persona
from models.common_schemas import GetCurrentTime


class User(BaseModel):
    phoneNumber: str
    name: str
    city: str
    email: str
    birthDate: str
    customerPersona: Persona


class UpdateUserDetails(BaseModel):
    user: User


class GetUserDetails(BaseModel):
    pass


class ExpertsAssistant(BaseModel):
    prompt: str


class ServicesAssistant(BaseModel):
    prompt: str


class SchedulesAssistant(BaseModel):
    prompt: str


class ConnectNow(BaseModel):
    user_id: str
    expert_id: str


class ConnectLater(BaseModel):
    user_id: str
    job_time: str
    expert_id: str
