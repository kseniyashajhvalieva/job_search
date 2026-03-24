from typing import Any

import requests


def get_employer_info(id: int) -> dict[str, Any]:
    """Информация о работодателе."""
    response = requests.get(f"https://api.hh.ru/employers/{id}")
    return response.json()


def get_vacancies_by_employer(employer_id: int) -> dict[str, Any]:
    """Информация о вакансиях."""
    response = requests.get(f"https://api.hh.ru/vacancies?employer_id={employer_id}&per_page=10")
    return response.json()
