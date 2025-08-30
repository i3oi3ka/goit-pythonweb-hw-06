from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.future import select

from db.connect import url_to_db
from db.models import Group, Student, Teacher, Subject, Grade
import random

fake = Faker()

engine = create_engine(url_to_db, echo=True)


def seed_groups():
    groups_to_seed = ["MCS-6", "MCS-7", "MDS-6", "MDS-7"]

    with Session(engine) as session:
        # Отримуємо всі існуючі групи одразу
        existing_groups_result = session.execute(
            select(Group.title).where(Group.title.in_(groups_to_seed))
        )
        existing_groups = {group[0] for group in existing_groups_result}

        # Створюємо тільки ті групи, яких ще немає
        new_groups = []
        for group in groups_to_seed:
            if group not in existing_groups:
                print(f"Creating new group: {group}")
                new_groups.append(Group(title=group))

        if new_groups:
            session.add_all(new_groups)
            session.commit()

        print(f"Data seeding complete. Created {len(new_groups)} new groups.")


def seed_students():
    with Session(engine) as session:
        groups = session.query(Group.id).all()
        for _ in range(45):
            group_id = random.choice(groups)[0]
            new_student = Student(
                name=fake.name(), email=fake.email(), group_id=group_id
            )
            session.add(new_student)
            session.commit()

    print(f"Data seeding complete. Created 45 new students.")


def seed_teachers():
    with Session(engine) as session:
        for _ in range(5):
            new_teacher = Teacher(name=fake.name(), email=fake.email())
            session.add(new_teacher)
            session.commit()

    print(f"Data seeding complete. Created 5 new teachers.")


def seed_subjects():
    subjects = ["Python", "React", "JavaScript", "HTML", "CSS", "SQL", "Java"]
    with Session(engine) as session:
        teachers = session.query(Teacher.id).all()
        for i in range(7):
            teacher_id = random.choice(teachers)[0]
            new_subject = Subject(name=subjects[i], teacher_id=teacher_id)
            session.add(new_subject)
            session.commit()

    print(f"Data seeding complete. Created 7 new subjects.")


def seed_grades():
    with Session(engine) as session:
        students = session.query(Student.id).all()
        subjects = session.query(Subject.id).all()
        for student in students:
            for i in range(20):
                new_grade = Grade(
                    grade=random.randint(1, 100),
                    student_id=student[0],
                    subject_id=random.choice(subjects)[0],
                    date=fake.date_this_year(),
                )
                session.add(new_grade)
                session.commit()
    print(f"Data seeding complete. Created 20 new foreach students.")


if __name__ == "__main__":
    # seed_groups()
    # seed_students()
    # seed_teachers()
    # seed_subjects()
    seed_grades()
