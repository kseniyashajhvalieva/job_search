import os

import psycopg2
from dotenv import load_dotenv

load_dotenv()


def get_connection(dbname: str | None = None) -> psycopg2.extensions.connection:
    """Подключение к базе данных PostgreSQL."""
    conn = psycopg2.connect(
        host="localhost", port=5432, database=dbname, user=os.getenv("DB_USER"), password=os.getenv("DB_PASSWORD")
    )

    return conn


def create_database(dbname: str) -> None:
    """Создание БД."""
    conn = get_connection("postgres")
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(f"DROP DATABASE IF EXISTS {dbname}")
    cur.execute(f"CREATE DATABASE {dbname}")

    conn.close()


def create_tables(dbname: str) -> None:
    """Создание таблиц."""
    conn = get_connection(dbname)
    conn.autocommit = True
    cur = conn.cursor()

    cur.execute(
        "CREATE TABLE employers" "(employer_id INTEGER PRIMARY KEY," "name_emp VARCHAR(100)," "site_url VARCHAR(100))"
    )
    cur.execute(
        "CREATE TABLE vacancies"
        "(employer_id INTEGER,"
        "name_vac VARCHAR(100),"
        "salary_from INTEGER,"
        "salary_to INTEGER,"
        "salary_currency VARCHAR(10),"
        "alternate_url TEXT)"
    )
    cur.execute(
        "ALTER TABLE vacancies ADD CONSTRAINT fk_vacancies_employers "
        "FOREIGN KEY (employer_id) REFERENCES employers (employer_id)"
    )
    conn.close()


def insert_employers(dbname: str, employers_tuples: list[tuple[int, str, str]]) -> None:
    """Заполнение таблицы employers данными из API"""
    conn = get_connection(dbname)
    conn.autocommit = True
    cur = conn.cursor()

    cur.executemany("INSERT INTO employers (employer_id, name_emp, site_url) VALUES (%s, %s, %s)",
                    employers_tuples)

    conn.close()


def insert_vacancies(dbname: str, vacancies_tuples: list[tuple[int, str, int | None, int | None, str | None,
str]]) -> None:
    """Заполнение таблицы vacancies данными из API"""
    conn = get_connection(dbname)
    conn.autocommit = True
    cur = conn.cursor()

    cur.executemany(
        "INSERT INTO vacancies (employer_id, name_vac, salary_from, salary_to, salary_currency, "
        "alternate_url) VALUES (%s, %s, %s, %s, %s, %s)",
        vacancies_tuples,
    )

    conn.close()
