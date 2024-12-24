from pydantic import BaseModel


class SaveUserCity(BaseModel):
    city: str


class SaveUserName(BaseModel):
    name: str


class SaveUserBirthDate(BaseModel):
    birthDate: str


class GetUserDetails(BaseModel):
    pass


class ExpertsAssistant(BaseModel):
    query: str


class ServicesAssistant(BaseModel):
    query: str
