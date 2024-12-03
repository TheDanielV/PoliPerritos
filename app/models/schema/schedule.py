# app/models/schema/schedule.py

from pydantic import BaseModel

from app.models.domain.schedule import Day


class ScheduleBase(BaseModel):
    day: Day
    start_hour: str
    end_hour: str


class ScheduleCreate(ScheduleBase):
    pass


class ScheduleResponse(ScheduleBase):

    class Config:
        from_attributes = True
