from typing import Optional
from database import Base
from sqlalchemy.orm import Mapped, mapped_column


# made by kirill
class UserProfile(Base):
    __tablename__ = "UserProfile"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str] = mapped_column(nullable=False)
# made by kirill

