from db.connect import url_to_db
from sqlalchemy import create_engine

engine = create_engine(url_to_db)
try:
    with engine.connect() as conn:
        print("✅ Database connection successful!")
except Exception as e:
    print(f"❌ Connection failed: {e}")
