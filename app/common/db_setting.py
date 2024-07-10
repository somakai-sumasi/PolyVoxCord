from config.db import DB_NAME
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

DATABASE = "sqlite:///./db/" + DB_NAME

ENGINE = create_engine(DATABASE, echo=False)
Base = declarative_base()

session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=ENGINE))
