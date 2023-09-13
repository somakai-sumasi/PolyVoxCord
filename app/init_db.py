from model import *
from common.setting import Base, ENGINE

Base.metadata.create_all(bind=ENGINE)
