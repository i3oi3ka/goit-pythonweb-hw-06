from sqlalchemy import func, desc

from db.models import Student, Grade, Subject, Group, Teacher
from db.connect import session


def select_1():
    return (
        session.query(Student.name, func.avg(Grade.grade).label("avg_grade"))
        .join(Grade)
        .group_by(Student.id)
        .order_by(desc("avg_grade"))
        .limit(5)
        .all()
    )


def select_2(subject: str = "Python"):
    """
    Returns the student with the highest average grade for the specified subject.
    If the subject is not found, returns 'subject not found'.
    """
    subject = session.query(Subject).where(Subject.name.like(subject)).first()
    if not subject:
        return "subject not found"
    return (
        session.query(
            Student.id, Student.name, func.avg(Grade.grade).label("avg_grade")
        )
        .join(Grade, Grade.student_id == Student.id)
        .filter(Grade.subject_id == subject.id)
        .group_by(Student.id)
        .order_by(desc("avg_grade"))
        .first()
    ) or None


def select_3(subject: str = "Python"):
    subject = session.query(Subject).where(Subject.name.like(subject)).first()
    if not subject:
        return "subject not found"
    return (
        session.query(
            Group.id,
            Group.title,
            func.avg(Grade.grade).label("avg_grade"),
        )
        .join(Student, Student.group_id == Group.id)
        .join(Grade, Grade.student_id == Student.id)
        .filter(Grade.subject_id == subject.id)
        .group_by(Group.id, Group.title)
        .all()
    ) or None


def select_4():
    return session.query(func.avg(Grade.grade).label("grade_avg")).all()


def select_5(teacher_name: str = "Darlene Waters"):
    teacher = session.query(Teacher.id).where(Teacher.name == teacher_name).first()
    if not teacher:
        return "teacher not found"
    return session.query(Subject.name).where(Subject.teacher_id == teacher.id).all()


def select_6(group_name: str = "MCS-7"):
    group = session.query(Group.id).where(Group.title == group_name).first()
    if not group:
        return "group not found"
    return session.query(Student.name).where(Student.group_id == group.id).all()


def select_7(group_name: str = "MCS-7", subject: str = "Python"):
    group = session.query(Group.id).where(Group.title == group_name).first()
    subject = session.query(Subject.id).where(Subject.name.like(subject)).first()
    if not subject or not group:
        return "subject or group not found"
    return (
        session.query(Student.name, Grade.grade)
        .join(Grade, Grade.student_id == Student.id)
        .where(Student.group_id == group.id)
        .where(Grade.subject_id == subject.id)
        .all()
    )


def select_8(teacher_name: str = "Keith Smith"):
    teacher = session.query(Teacher).where(Teacher.name == teacher_name).first()
    subjects = session.query(Subject.id).where(Subject.teacher_id == teacher.id).all()

    if not teacher:
        return "teacher not found"
    return (
        session.query(func.avg(Grade.grade)).where(Grade.subject_id.in_(subjects)).all()
    )


if __name__ == "__main__":
    print(select_8())
