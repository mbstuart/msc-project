from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine, desc

db_string = "postgres://theme-extractor:tepassword@localhost:5432/theme-extractor"

engine = create_engine(db_string)
sessionmaker = sessionmaker()
sessionmaker.configure(bind=engine)

def get_session():
    session = sessionmaker();
    return session;