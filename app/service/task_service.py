import datetime
import os


class TaskDictService:
    @classmethod
    def remove_wav_files(cls):
        path = "./tmp/wav/"
        files = os.listdir(path)
        now = datetime.datetime.now()

        for file in files:
            _, ext = os.path.splitext(file)
            if ext != ".wav":
                continue

            mtime = datetime.datetime.fromtimestamp(os.path.getmtime(path + file))
            # 2日経った音声データを削除する
            if (now - mtime).days > 2:
                os.remove(path + file)
