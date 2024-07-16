from common.db_setting import ENGINE, Base
from model import *  # noqa: F401, F403

Base.metadata.create_all(bind=ENGINE)
