
from pydantic import BaseModel, Field, model_validator

class Task(BaseModel):
    id : int | None = None
    name: str | None = None
    pomodoro: int | None = None
    category_id: int 
    user_id: int

    class Config:
        from_attributes = True

    @model_validator(mode="after")
    def check_name_or_count_not_null(self):
        if self.name is None and self.count is None:
            raise ValueError("пустое")
        
        return self
    
class TaskCreateSchema(BaseModel):
    name: str | None = None
    pomodoro: int | None = None
    category_id: int 
