import csv
from typing import Dict, Union, Type


class CSVHandler:
    def __init__(
        self,
        filename: str,
        index_columns: Dict[str, Type],
        non_index_columns: Dict[str, Type],
    ):
        # コンストラクタ：ファイル名とカラム情報を保存
        self.filename = filename
        self.index_columns = index_columns
        self.non_index_columns = non_index_columns

    def read(
        self, index_dict: Dict[str, Union[str, int, bool]]
    ) -> Dict[str, Union[str, int, bool]]:
        # CSVファイルを読む
        with open(self.filename, "r") as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                if all(row[k] == str(v) for k, v in index_dict.items()):
                    # 型変換を行い、該当する行を返す
                    return {
                        k: self.index_columns[k](v)
                        if k in self.index_columns
                        else self.non_index_columns[k](v)
                        for k, v in row.items()
                    }

        # 存在しない場合辞書型で返す
        new_row = {}
        for k in self.index_columns.keys():
            new_row[k] = index_dict.get(k, None)
        for k in self.non_index_columns.keys():
            new_row[k] = None
        return new_row

    def write(
        self, row_dict: Dict[str, Union[str, int, bool]]
    ) -> Dict[str, Union[str, int, bool]]:
        # CSVファイルに書く
        rows = []
        updated_row = None

        with open(self.filename, "r") as csv_file:
            reader = csv.DictReader(csv_file)
            headers = reader.fieldnames  # ヘッダーを取得
            for row in reader:
                if all(row[k] == str(row_dict.get(k, "")) for k in self.index_columns):
                    # 更新する行が見つかった場合
                    row.update(row_dict)
                    updated_row = row
                rows.append(row)

        # 新しい行を追加する場合
        if updated_row is None:
            updated_row = row_dict
            rows.append(row_dict)

        # CSVファイルに書き込む
        with open(self.filename, "w", newline="") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=headers)
            writer.writeheader()
            for row in rows:
                writer.writerow(row)

        # 更新後の行を型変換して返す
        return {
            k: self.index_columns[k](v)
            if k in self.index_columns
            else self.non_index_columns[k](v)
            for k, v in updated_row.items()
        }
