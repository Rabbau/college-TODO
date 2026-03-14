from datetime import datetime

from pydantic import BaseModel


class NoteUpdateSchema(BaseModel):
    content: str | None = ''
    due: datetime | None = None
    done: bool = False
    favorite: bool = False
    # made by kirill
    importance: str | None = None
    # made by kirill


class NoteResponseSchema(BaseModel):
    content: str
    due: datetime | None = None
    done: bool
    favorite: bool
    # made by kirill
    importance: str
    # made by kirill