from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from datetime import datetime

from sqlalchemy import ForeignKey, Table, Column, Integer, PrimaryKeyConstraint, func


class Base(DeclarativeBase): ...


class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    email: Mapped[str]
    registered_at: Mapped[datetime] = mapped_column(default=func.now())

    # courses: Mapped[list["Course"]] = relationship(
    #     secondary="association", back_populates="students"
    # )
