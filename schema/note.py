from datetime import datetime

from pydantic import BaseModel


class NoteUpdateSchema(BaseModel):
    content: str | None = ''
    due: datetime | None = None
    done: bool = False
    favorite: bool = False


class NoteResponseSchema(BaseModel):
    content: str
    due: datetime | None = None
    done: bool
    favorite: bool
