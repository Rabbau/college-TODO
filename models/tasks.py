from datetime import datetime
from typing import Any, Optional

from sqlalchemy import Boolean, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


# made by kirill
class Tasks(Base):
    __tablename__ = "Tasks"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    pomodoro: Mapped[int] = mapped_column(nullable=False)
    category_id: Mapped[int] = mapped_column(nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("UserProfile.id"), nullable=False)
    due: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    done: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default="false")
    favorite: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, server_default="false")
    # made by kirill
    importance: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="нейтрально",
        server_default="нейтрально",
    )
    # made by kirill


class Categories(Base):
    __tablename__ = "Categories"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    type: Mapped[Optional[str]]
    name: Mapped[str]
# made by kirill


