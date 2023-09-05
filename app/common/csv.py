import csv
from typing import List, Dict, Union, Type
from decimal import Decimal


class CSVHandler:
    def __init__(
        self,
        filename: str,
        index_columns: Dict[str, Type],
        non_index_columns: Dict[str, Type],
    ) -> None:
        """
        コンストラクタ：ファイル名とカラム情報を保存

        Parameters:
            filename (str): CSVファイル名
            index_columns (Dict[str, Type]): インデックスとなるカラム名とその型の辞書
            non_index_columns (Dict[str, Type]): インデックスでないカラム名とその型の辞書
        """
        self.filename = filename
        self.index_columns = index_columns
        self.non_index_columns = non_index_columns

    def read(
        self, index_dict: Dict[str, Union[str, int, bool, Decimal]]
    ) -> Dict[str, Union[str, int, bool, Decimal]]:
        """
        CSVファイルを読む

        Parameters:
            index_dict (Dict[str, Union[str, int, bool, Decimal]]): インデックス名と値の辞書型

        Returns:
            Dict[str, Union[str, int, bool, Decimal]]: 該当する行のデータ（辞書型）
        """
        # CSVファイルを読み込む
        with open(self.filename, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if all(row[key] == str(value) for key, value in index_dict.items()):
                    # 型変換を行いつつ、該当する行のデータを返す
                    return {
                        col: self.index_columns[col](row[col])
                        if col in self.index_columns
                        else self.non_index_columns[col](row[col])
                        for col in row.keys()
                    }

            # 存在しない場合辞書型で返す
        new_row = {}
        for k in self.index_columns.keys():
            new_row[k] = index_dict.get(k, None)
        for k in self.non_index_columns.keys():
            new_row[k] = None
        return new_row

    def write(
        self, index_dict: Dict[str, Union[str, int, bool, Decimal]]
    ) -> Dict[str, Union[str, int, bool, Decimal]]:
        """
        CSVファイルに書く（更新または追加）

        Parameters:
            index_dict (Dict[str, Union[str, int, bool, Decimal]]): 書き込む行のデータ（辞書型）

        Returns:
            Dict[str, Union[str, int, bool, Decimal]]: 更新後の行のデータ（辞書型）
        """
        rows = []
        updated = False  # 行が更新されたかどうかのフラグ
        with open(self.filename, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if all(
                    row[key] == str(index_dict.get(key, ""))
                    for key in self.index_columns.keys()
                ):
                    # 該当する行を更新
                    row.update(index_dict)
                    updated = True
                rows.append(row)

        # 行が更新されなかった場合は、新しい行を追加
        if not updated:
            rows.append(index_dict)

        # CSVファイルを更新
        with open(self.filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(
                file,
                fieldnames=list(self.index_columns.keys())
                + list(self.non_index_columns.keys()),
            )
            writer.writeheader()
            writer.writerows(rows)

        return self.read(index_dict)
