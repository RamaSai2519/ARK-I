from pydantic import BaseModel
from models.common_schemas import GetCurrentTime


class CancelSchedule(BaseModel):
    schedule_id: str


class CreateSchedule(BaseModel):
    job_time: str
    expert_id: str
