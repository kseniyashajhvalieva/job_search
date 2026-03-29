from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class Vacancy:
    """Модель вакансии, нормализованная из ответа hh.ru для сохранения в БД."""

    employer_id: int
    name: str
    salary_from: int | None
    salary_to: int | None
    salary_currency: str | None
    alternate_url: str

    @classmethod
    def from_hh_item(cls, item: dict[str, Any]) -> "Vacancy":
        salary = item.get("salary") or {}
        return cls(
            employer_id=int(item["employer"]["id"]),
            name=str(item["name"]),
            salary_from=salary.get("from"),
            salary_to=salary.get("to"),
            salary_currency=salary.get("currency"),
            alternate_url=str(item["alternate_url"]),
        )

    def salary_str(self) -> str:
        """Человекочитаемая зарплата для CLI."""
        if self.salary_from is None and self.salary_to is None:
            return "не указана"
        cur = f" {self.salary_currency}" if self.salary_currency else ""
        if self.salary_from is None:
            return f"до {self.salary_to}{cur}"
        if self.salary_to is None:
            return f"от {self.salary_from}{cur}"
        return f"{self.salary_from}–{self.salary_to}{cur}"