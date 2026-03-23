import os
import psycopg2

from dotenv import load_dotenv

load_dotenv()

def get_connection(dbname=None):
    """Подключение к базе данных PostgreSQL."""
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        database=dbname,
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"))

    return conn

def create_database(dbname):
    """Создание БД."""
    conn = get_connection("postgres")
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f"DROP DATABASE IF EXISTS {dbname}")
    cur.execute(f"CREATE DATABASE {dbname}")

    conn.close()

def create_tables(dbname):
    """Создание таблиц."""
    conn = get_connection(dbname)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute("CREATE TABLE employers"
                "(employer_id INTEGER PRIMARY KEY,"
                "name_emp VARCHAR(100),"
                "site_url VARCHAR(100))"
                )
    cur.execute("CREATE TABLE vacancies"
                "(employer_id INTEGER,"
                "name_vac VARCHAR(100),"
                "salary_from INTEGER,"
                "salary_to INTEGER,"
                "salary_currency VARCHAR(10),"
                "alternate_url TEXT)"
                )
    cur.execute("ALTER TABLE vacancies ADD CONSTRAINT fk_vacancies_employers "
                "FOREIGN KEY (employer_id) REFERENCES employers (employer_id)"
                )
    conn.close()


# conn = get_connection("hh_parser")
# conn.autocommit = True
# cur = conn.cursor()
#
# cur.execute("INSERT INTO")
#
# conn.close()