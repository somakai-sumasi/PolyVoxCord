from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os

load_dotenv()
DB_NAME = os.getenv("DB_NAME")
DATABASE = "sqlite:///./db/" + DB_NAME

ENGINE = create_engine(DATABASE, echo=False)
Base = declarative_base()

session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=ENGINE))
