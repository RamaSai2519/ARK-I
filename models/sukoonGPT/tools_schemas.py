from pydantic import BaseModel


class EventsandMeetupsAssistant(BaseModel):
    prompt: str


class RegisterUserForEvent(BaseModel):
    event_slug: str
