from model.base_model import BaseModel


class ReadLimit(BaseModel):
    def __init__(self, index_value):
        FILE = "app/data/ReadLimit.csv"
        INDEX_COLUMNS = {"guild_id": int}
        NON_INDEX_COLUMNS = {"limit": int}

        super().__init__(FILE, index_value, INDEX_COLUMNS, NON_INDEX_COLUMNS)

    @property
    def limit(self) -> int:
        return self.data.get("limit", None)

    @limit.setter
    def limit(self, value: int):
        self.data["limit"] = value
        self.save()
