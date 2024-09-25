from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
SQLALCHEMY_DATABASE_URL = "postgresql://root:password1@localhost:5432/ttrello"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

'''

docker run -d -p 5432:5432 -e POSTGRES_DB=ttrello -e POSTGRES_USER=root -e POSTGRES_PASSWORD=password1 --name ttrello_cont postgres:latest

'''
