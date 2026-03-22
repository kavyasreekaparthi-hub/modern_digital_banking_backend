import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. Load environment variables from the .env file
load_dotenv()

# 2. Get the Database URL from environment variables
# This allows the app to use PostgreSQL in production and local dev
DATABASE_URL = os.getenv("DATABASE_URL")

# Fallback for safety (though DATABASE_URL should always be in .env)
if not DATABASE_URL:
    DATABASE_URL = "postgresql://postgres:password@localhost:5432/banking_db"

# 3. Create the SQLAlchemy Engine
# For PostgreSQL, we don't need the 'check_same_thread' argument used in SQLite
engine = create_engine(DATABASE_URL)

# 4. Create a SessionLocal class
# Each instance of this class will be a database session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 5. Create the Base class
# Our database models (User, Bill, Alert, etc.) will inherit from this
Base = declarative_base()

# 6. Dependency: get_db
# This function creates a fresh database session for every request 
# and ensures it is closed after the request is finished.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()