from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker

# url_to_db = "sqlite:///mynotes.db"
url_to_db = "postgresql+psycopg://admin:password@localhost:5432/books_db"
engine = create_engine(url_to_db)
Session = sessionmaker(bind=engine)
session = Session()
