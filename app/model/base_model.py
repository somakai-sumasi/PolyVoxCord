from typing import Dict, Union, Type
from common.csv import CSVHandler


class BaseModel(CSVHandler):
    def __init__(
        self,
        filename: str,
        index_values: Dict[str, Union[str, int, bool]],
        index_columns: Dict[str, Type],
        non_index_columns: Dict[str, Type],
    ):
        super().__init__(filename, index_columns, non_index_columns)
        self.index_values = index_values
        self.data = self.read(index_values)

    def refresh(self):
        """CSVから最新のデータを読み込む"""
        self.data = self.read(self.index_values)

    def save(self):
        """現在のデータをCSVに保存する"""
        self.write(self.data)
