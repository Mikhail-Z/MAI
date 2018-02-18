import csv
import psycopg2


def get_icd10_info(filename="icd10_base.csv"):
    icd10_infos = []
    with open(filename, "r") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            icd10_infos.append(dict(row))
    return icd10_infos


def insert_info_to_db(connection_string, icd10_info):
    try:
        conn = psycopg2.connect(connection_string)
        cursor = conn.cursor()
        for row in icd10_info:
            cursor.execute(
                "insert into icd10(doctor_id, parent_id, code, name) values(%s, %s, %s, %s)",
                [
                    int(row["doctor_id"]),
                    None if row["parent_id"] == "" else int(row["parent_id"]),
                    row["code"],
                    row["name"]
                ]
            )
        conn.commit()
    except Exception as e:
        print(e)


rows = get_icd10_info()
connection_string = "dbname='hospitaldb' user='mikhail' host='localhost' password='need4you'"
insert_info_to_db(connection_string, rows)