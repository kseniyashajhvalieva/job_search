from src.db_utils import create_database, create_tables, insert_employers, insert_vacancies
from src.api import get_employer_info, get_vacancies_by_employer
from src.db_manager import DBManager
from src.vacancy import Vacancy


def run_cli():
    create_database("hh_parser")
    create_tables("hh_parser")

    employer_id = [1122462, 39305, 34692, 23427, 907345, 49357, 4509, 1740, 1603745, 1604297]
    employers_data = []
    vacancies_data = []

    for id in employer_id:
        data = get_employer_info(id)
        employers_data.append(data)

    for id in employer_id:
        data = get_vacancies_by_employer(id)
        vacancies_data.append(data['items'])

    employers_tuples = [(emp["id"], emp["name"], emp["site_url"]) for emp in employers_data]
    vacancies = []

    for vac_list in vacancies_data:
        for vac in vac_list:
            vacancies.append(Vacancy.from_hh_item(vac))

    vacancies_tuples = [(v.employer_id, v.name, v.salary_from, v.salary_to, v.salary_currency, v.alternate_url) for v in vacancies]

    insert_employers("hh_parser", employers_tuples)
    insert_vacancies("hh_parser", vacancies_tuples)

    db = DBManager("hh_parser")

    print("\n1. Компании и количество вакансий:")

    for employer_id, name_emp, cnt in db.get_companies_and_vacancies_count():
        print(f"   {name_emp} (id={employer_id}): {cnt}")

    print("\n2. Все вакансии:")

    for employer_id, name_emp, name_vac, salary, currency, url in db.get_all_vacancies():
        salary_str = salary if salary else "не указана"
        currency_str = currency or ""
        print(f"   {name_emp} | {name_vac} | {salary_str} {currency_str} | {url}")

    print("\n3. Средняя зарплата:")

    avg_from, avg_to = db.get_avg_salary()
    print(f"   От: {avg_from}")
    print(f"   До: {avg_to}")

    print("\n4. Вакансии с зарплатой выше средней:")

    for name_vac, salary_from in db.get_vacancies_with_higher_salary():
        print(f"   {name_vac}: от {salary_from}")

    keyword = input("Введите ключевое слово для поиска: ").strip()
    if keyword:
        print(f"\n5. Вакансии с ключевым словом '{keyword}':")
        for (name_vac,) in db.get_vacancies_with_keyword(keyword):
            print(f"   {name_vac}")
    else:
        print("\n5. Ключевое слово не введено")

if __name__ == "__main__":
    run_cli()