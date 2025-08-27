from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.future import select

from db.connect import url_to_db
from db.models import Group

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


if __name__ == "__main__":
    seed_groups()
