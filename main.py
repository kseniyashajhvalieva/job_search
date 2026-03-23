from src.db_utils import create_database, create_tables, insert_employers, insert_vacancies
from src.api import get_employer_info, get_vacancies_by_employer

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
vacancies_tuples = []
for vac_list in vacancies_data:
    for vac in vac_list:
        vacancies_tuples.append((vac["employer"]["id"], vac["name"], vac["salary"]["from"] if vac["salary"] else None, vac["salary"]["to"] if vac["salary"] else None, vac["salary"]["currency"] if vac["salary"] else None, vac["alternate_url"]))

insert_employers("hh_parser", employers_tuples)
insert_vacancies("hh_parser", vacancies_tuples)
