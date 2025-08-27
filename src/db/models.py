from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, Integer, DateTime, func, CheckConstraint
from typing import List
from datetime import datetime


class Base(DeclarativeBase):
    pass


class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(50), nullable=False)
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id"), nullable=False)
    registered_at: Mapped[datetime] = mapped_column(default=func.now())

    group: Mapped["Group"] = relationship("Group", back_populates="students")
    grades: Mapped[List["Grade"]] = relationship("Grade", back_populates="student")

    def __repr__(self):
        return f"#{self.id} {self.name} {self.email} {self.registered_at}"


class Group(Base):
    __tablename__ = "groups"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(50), nullable=False)

    students: Mapped[List[Student]] = relationship("Student", back_populates="group")

    def __repr__(self):
        return f"#{self.id} {self.title}"


class Teacher(Base):
    __tablename__ = "teachers"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)

    subjects: Mapped[List["Subject"]] = relationship(
        "Subject", back_populates="teacher"
    )

    def __repr__(self):
        return f"Teacher#{self.id}: {self.name}"


class Subject(Base):
    __tablename__ = "subjects"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    teacher_id: Mapped[int] = mapped_column(
        ForeignKey("teachers.id"), nullable=False
    )  # ВИПРАВЛЕНО

    teacher: Mapped["Teacher"] = relationship("Teacher", back_populates="subjects")
    grades: Mapped[List["Grade"]] = relationship("Grade", back_populates="subject")

    def __repr__(self):
        return f"Subject#{self.id}: {self.name}"


class Grade(Base):
    __tablename__ = "grades"

    id: Mapped[int] = mapped_column(primary_key=True)
    grade: Mapped[int] = mapped_column(Integer, nullable=False)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"), nullable=False)
    subject_id: Mapped[int] = mapped_column(ForeignKey("subjects.id"), nullable=False)
    date: Mapped[datetime] = mapped_column(DateTime, default=func.now(), nullable=False)

    student: Mapped["Student"] = relationship("Student", back_populates="grades")
    subject: Mapped["Subject"] = relationship("Subject", back_populates="grades")

    __table_args__ = (
        CheckConstraint(
            "grade >= 1 AND grade <= 100",
            name="check_grade_range",
        ),
    )

    def __repr__(self):
        return f"Grade#{self.id}: {self.grade}"
