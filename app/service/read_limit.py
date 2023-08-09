import csv
import os
import glob

FILE = "app/data/ReadLimt.csv"


def get_limt(guildId: int):
    with open(FILE, "r") as f:
        rows = csv.reader(f)

        for row in rows:
            if int(row[0]) == guildId:
                f.close()
                return int(row[1])

        f.close()
    return 100


def set_limt(guildId: int, limt: int):
    fr = open(FILE, "r")
    csv_data = csv.reader(fr)
    list = [e for e in csv_data]
    fr.close()

    update = 0
    for i in range(len(list)):
        if int(list[i][0]) == guildId:
            list[i][1] = limt
            update = 1

    if update == 0:
        with open(FILE, "a", newline="") as fw:
            writer = csv.writer(fw)
            writer.writerow([guildId, limt])
    else:
        with open(FILE, "w", newline="") as fw:
            writer = csv.writer(fw)
            writer.writerows(list)
    fw.close()

    return 0
