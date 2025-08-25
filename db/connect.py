from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker

# url_to_db = "sqlite:///mynotes.db"
url_to_db = "postgresql+psycopg2:://admin:password@localhost:5432/hw_6_db"
engine = create_engine(url_to_db)
Session = sessionmaker(bind=engine)
session = Session()
