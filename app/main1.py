from model.read_limit import ReadLimit
from common.csv import CSVHandler

# FILE = "app/data/ReadLimit.csv"
# INDEX_COLUMNS = {"guild_id": int}
# NON_INDEX_COLUMNS = {"limit": int}
# csv = CSVHandler(FILE, INDEX_COLUMNS, NON_INDEX_COLUMNS)
# print(csv.read({"guild_id": 1}))
# print(csv.write({"guild_id": 1, "limit":4}))
limit = ReadLimit({"guild_id": 100})
limit.limit = 100
