from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Menggunakan SQLite untuk development (tidak perlu MySQL)
DATABASE_URL = "sqlite:///./ppd_database.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
