from models.common_schemas import GetCurrentTime
from pydantic import BaseModel


class GetUserRegisteredEvents(BaseModel):
    pass


class GetEventDetails(BaseModel):
    source: str
