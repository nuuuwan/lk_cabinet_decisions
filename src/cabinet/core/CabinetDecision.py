from dataclasses import dataclass
from functools import cached_property
from typing import Generator

from utils import Log

from cabinet.core.CabinetDecisionsWebMixin import CabinetDecisionsWebMixin
from scraper import AbstractDoc

log = Log("CabinetDecision")


@dataclass
class CabinetDecision(AbstractDoc, CabinetDecisionsWebMixin):
    decision_details: str

    @classmethod
    def get_doc_class_description(cls) -> str:
        return "A Sri Lanka Cabinet Decision is an official policy or action agreed by the Cabinet of Ministers, shaping governance, law, and national development in the country."  # noqa: E501

    @classmethod
    def get_doc_class_emoji(cls) -> str:
        return "🏛️"

    @cached_property
    def text_from_metadata(self) -> str:
        return "\n\n".join(
            [
                self.description,
                self.decision_details,
            ]
        )

    @classmethod
    def gen_docs(cls) -> Generator["CabinetDecision", None, None]:
        for year_str, url_year in cls.gen_urls_years():
            for date_str, url_date in cls.gen_url_dates_from_url_year(
                year_str, url_year
            ):
                yield from cls.gen_docs_from_url_date(date_str, url_date)
