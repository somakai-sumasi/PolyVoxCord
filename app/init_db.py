from common.db_setting import ENGINE, Base
from model import *

Base.metadata.create_all(bind=ENGINE)
