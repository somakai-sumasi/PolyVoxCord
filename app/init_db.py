from model import *
from common.db_setting import Base, ENGINE

Base.metadata.create_all(bind=ENGINE)
