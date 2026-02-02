# datbase connection and session management

from curses import echo
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.config import settings


# create the database engine
# verifys connection is alive with pool_pre_ping
engine =create_engine (settings.DATABASE_URL, pool_pre_ping=True, echo=settings.DEBUG) 

# create database sessions

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()   

# Base class for all models to inherit from
Base = declarative_base()

def get_db():
    # dependency to get DB session
    # this ensurres each requests has its own session and is closed after use
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        