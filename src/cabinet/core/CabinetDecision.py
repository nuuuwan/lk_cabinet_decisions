from dataclasses import dataclass
from functools import cached_property
from typing import Generator

from utils import Log

from scraper import AbstractDoc
from utils_future import WWW

log = Log("CabinetDecision")


class CabinetDecisionsWebMixin:
    @classmethod
    def get_doc_from_url_details(
        cls, num, date_str, description, url_details
    ) -> "CabinetDecision | None":
        www_details = WWW(url_details)
        soup = www_details.soup
        if not soup:
            return None
        div_title = soup.find("div", class_="cab_heading_text_e")
        title_text = div_title.text.strip()
        assert date_str in title_text
        div_body = soup.find("div", class_="cab_normal_text_e")
        decision_details = div_body.text.strip()
        return CabinetDecision(
            num=num,
            date_str=date_str,
            description=description,
            url_metadata=url_details,
            lang="en",
            decision_details=decision_details,
        )

    @classmethod
    def gen_docs_from_url_date(
        cls, date_str, url_date
    ) -> Generator["CabinetDecision", None, None]:
        www_date = WWW(url_date)
        soup = www_date.soup
        if not soup:
            return
        tables = soup.find_all("table")
        if len(tables) < 2:
            return
        for tr in tables[1].find_all("tr"):
            tds = tr.find_all("td")
            assert len(tds) >= 2
            num = tds[0].text.strip()
            a = tds[1].find("a")
            description = a.text.strip()
            url_details = cls.URL_BASE + a["href"]

            doc = cls.get_doc_from_url_details(
                num, date_str, description, url_details
            )
            if doc:
                yield doc

    @classmethod
    def gen_url_dates_from_url_year(
        cls, year_str, url_year
    ) -> Generator[tuple[str, str], None, None]:
        www_year = WWW(url_year)
        soup = www_year.soup
        if not soup:
            return
        table = soup.find("table")
        for tr in table.find_all("tr"):
            for td in tr.find_all("td"):
                a = td.find("a")
                date_str = a.text.strip()
                assert (
                    len(date_str) == 10
                    and date_str[2] == "-"
                    and date_str[5] == "-"
                )
                assert date_str[:4] == year_str
                url_date = cls.URL_BASE + a["href"]
                yield date_str, url_date

    @classmethod
    def gen_urls_years(cls) -> Generator[tuple[str, str], None, None]:
        www_home = WWW(cls.URL_DECISIONS)
        soup = www_home.soup
        if not soup:
            return
        ul = soup.find("ul", class_="menu")
        for li in ul.find_all("li"):
            a = li.find("a")
            year_str = a.text.strip()
            assert len(year_str) == 4 and year_str.isdigit()
            url_year = cls.URL_BASE + a["href"]
            yield year_str, url_year


@dataclass
class CabinetDecision(AbstractDoc, CabinetDecisionsWebMixin):
    decision_details: str

    URL_BASE = "https://www.cabinetoffice.gov.lk/cab/index.php"
    URL_DECISIONS = (
        URL_BASE + "?option=com_content&view=article&id=63&Itemid=43&lang=en"
    )

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
