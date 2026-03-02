from sqlalchemy import create_engine
from sqlalchemy import declarative_base,sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./exam.db"

engine = create_engine( SQLALCHEMY_DATABASE_URL , connect_args={"check_same_thread": False} )
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()