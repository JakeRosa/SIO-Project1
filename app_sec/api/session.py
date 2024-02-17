from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///db.sqlite3", echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
