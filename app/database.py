import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Load variables from .env
load_dotenv()

# Get the database URL from .env
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# Create the SQLAlchemy engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a SessionLocal class for database requests
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the Base class that all models will inherit from
Base = declarative_base()

# Dependency to get the DB session in your routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()