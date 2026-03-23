from src.db_utils import get_connection

class DBManager:

    def __init__(self, dbname):
        self.dbname = dbname

    def get_companies_and_vacancies_count(self):
        """Получает список всех компаний и количество вакансий у каждой компании"""
        conn = get_connection(self.dbname)
        cur = conn.cursor()
        cur.execute("SELECT employers.employer_id, name_emp, COUNT(DISTINCT name_vac) FROM employers INNER JOIN vacancies "
                    "ON employers.employer_id=vacancies.employer_id GROUP BY employers.employer_id, name_emp")
        data = cur.fetchall()
        conn.close()
        return data

    def get_all_vacancies(self):
        """Получает список всех вакансий с указанием названия компании,
      названия вакансии и зарплаты и ссылки на вакансию."""
        conn = get_connection(self.dbname)
        cur = conn.cursor()
        cur.execute("SELECT employers.employer_id, name_emp, name_vac, salary_from|| ' - ' ||salary_to as salary, "
                    "salary_currency, alternate_url FROM employers INNER JOIN vacancies "
                    "ON employers.employer_id=vacancies.employer_id")
        data = cur.fetchall()
        conn.close()
        return data

    def get_avg_salary(self):
        """Получает среднюю зарплату по вакансиям"""
        conn = get_connection(self.dbname)
        cur = conn.cursor()
        cur.execute("SELECT AVG(salary_from), AVG(salary_to) FROM vacancies")
        data = cur.fetchall()
        conn.close()
        return data

    def get_vacancies_with_higher_salary(self):
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        conn = get_connection(self.dbname)
        cur = conn.cursor()
        cur.execute("SELECT name_vac, salary_from FROM vacancies "
                    "WHERE salary_from > (SELECT AVG(salary_from) FROM vacancies)")
        data = cur.fetchall()
        conn.close()
        return data

    def get_vacancies_with_keyword(self, keyword):
        """Получает список всех вакансий, в названии которых содержатся переданные в метод слова"""
        conn = get_connection(self.dbname)
        cur = conn.cursor()
        cur.execute("SELECT name_vac FROM vacancies WHERE name_vac ILIKE %s", (f"%{keyword}%",))
        data = cur.fetchall()
        conn.close()
        return data
