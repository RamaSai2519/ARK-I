from pydantic import BaseModel


class CancelSchedule(BaseModel):
    schedule_id: str
