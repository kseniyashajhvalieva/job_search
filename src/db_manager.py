import os
import psycopg2

from dotenv import load_dotenv

load_dotenv()

def get_connection(dbname=None):
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        database=dbname,
        user="postgres",
        password=os.getenv("DB_PASSWORD"))

    return conn

conn = get_connection("postgres")
conn.autocommit = True
cur = conn.cursor()

cur.execute("DROP DATABASE IF EXISTS hh_parser")
cur.execute("CREATE DATABASE hh_parser")

conn.close()

conn = get_connection("hh_parser")
conn.autocommit = True
cur = conn.cursor()

cur.execute("CREATE TABLE employers"
            "(employer_id INTEGER PRIMARY KEY,"
            "name_emp VARCHAR(100),"
            "site_url VARCHAR(100))"
            )
cur.execute("CREATE TABLE vacansies"
            "(employer_id INTEGER,"
            "name_vac VARCHAR(100),"
            "salary_from INTEGER,"
            "salary_to INTEGER,"
            "salary_currency VARCHAR(10),"
            "alternate_url TEXT)"
            )
cur.execute("ALTER TABLE vacansies ADD CONSTRAINT fk_vacansies_employers "
            "FOREIGN KEY (employer_id) REFERENCES employers (employer_id)"
            )
conn.close()