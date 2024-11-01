from datetime import datetime

from pydantic import BaseModel, field_validator, ConfigDict, Field


class TaskScheme(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str
    author: str
    description: str
    deadline: str

    @field_validator("deadline")
    @classmethod
    def check_if_correct_deadline(cls, v):
        try:
            deadline_date = datetime.strptime(v, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Deadline must be in the format YYYY-MM-DD")
        if deadline_date < datetime.now():
            raise ValueError("Deadline must be in the future")
        return deadline_date.isoformat()[:10:]


class TaskPut(TaskScheme):
    name: str = Field(None)
    author: str
    description: str = Field(None)
    deadline: str = Field(None)


class TaskDelete(BaseModel):
    user: str
