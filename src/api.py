import requests


def get_employer_info(id):
    """ Информация о работодателе."""
    response = requests.get(f"https://api.hh.ru/employers/{id}")
    return response.json()
