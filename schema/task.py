from datetime import datetime

from pydantic import BaseModel


class TaskBase(BaseModel):
    name: str
    pomodoro: int | None = None
    category_id: int | None = None
    due: datetime | None = None


class TaskCreateSchema(TaskBase):
    pass


class TaskStatusUpdateSchema(BaseModel):
    due: datetime | None = None
    done: bool | None = None
    favorite: bool | None = None


class Task(BaseModel):
    id: int
    name: str
    pomodoro: int | None = None
    category_id: int
    user_id: int
    due: datetime | None = None
    done: bool
    favorite: bool
    notes_preview: str | None = None

    class Config:
        from_attributes = True
