import re
from typing import Generator

from utils import Log

from scraper import AbstractDoc
from utils_future import WWW

log = Log("CabinetDecisionsWebMixin")


class CabinetDecisionsWebMixin:

    URL_BASE = "https://www.cabinetoffice.gov.lk"
    URL_DECISION_WITHOUT_LANG = (
        URL_BASE
        + "/cab/index.php"
        + "?option=com_content&view=article&id=63&Itemid=43"
    )

    @classmethod
    def get_doc_from_url_details(
        cls, num, date_str, description, url_details, lang
    ):
        www_details = WWW(url_details)
        soup = www_details.soup
        if not soup:
            log.error(f"[{www_details}] no soup.")
            return None
        assert len(lang) == 2
        lang_short = lang[0]
        div_title = soup.find("div", id=f"cab_heading_text_{lang_short}")
        decision_details_title = div_title.text.strip()
        assert date_str in decision_details_title
        div_body = soup.find("div", id=f"cab_normal_text_{lang_short}")
        decision_details_body = div_body.text.strip()
        return cls(
            num=num,
            date_str=date_str,
            description=description,
            url_metadata=url_details,
            lang=lang,
            decision_details_title=decision_details_title,
            decision_details_body=decision_details_body,
        )

    @staticmethod
    def __clean_url__(url):
        url = re.sub(r"\s+", "", url)
        return url

    @classmethod
    def gen_docs_from_url_date(
        cls, date_str, url_date, lang
    ) -> Generator["AbstractDoc", None, None]:
        www_date = WWW(url_date)
        soup = www_date.soup
        if not soup:
            log.error(f"[{www_date}] no soup.")
            return
        tables = soup.find_all("table", attrs={"width": "95%"})
        if len(tables) < 2:
            log.warning(f"[{www_date}] incorrect decision table.")
            return
        table = tables[1]
        for tr in reversed(table.find_all("tr")):
            tds = tr.find_all("td")
            if len(tds) < 2:
                continue
            num = tds[0].text.strip()
            a = tds[1].find("a")
            description = a.text.strip()
            url_details = f'{cls.URL_BASE}/cab/{a["href"]}'
            url_details = cls.__clean_url__(url_details)
            doc = cls.get_doc_from_url_details(
                num, date_str, description, url_details, lang
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
            log.error(f"[{www_year}] no soup.")
            return
        tables = soup.find_all("table", attrs={"width": "85%"})
        assert len(tables) == 2
        table = tables[1]
        data_str_set = set()  # HACK to prevent duplicates
        for tr in reversed(table.find_all("tr")):
            for td in reversed(tr.find_all("td")):
                a = td.find("a")
                date_str = a.text.strip()
                assert (
                    len(date_str) == 10
                    and date_str[4] == "-"
                    and date_str[7] == "-"
                ), date_str
                assert date_str[:4] == year_str
                if date_str in data_str_set:
                    continue
                data_str_set.add(date_str)

                url_date = f'{cls.URL_BASE}/cab/{a["href"]}'
                yield date_str, url_date

    @classmethod
    def gen_url_years_for_url_decision(
        cls, url_decision
    ) -> Generator[tuple[str, str], None, None]:
        www_home = WWW(url_decision)
        soup = www_home.soup
        if not soup:
            log.error(f"[{www_home}] no soup.")
            return
        ul = soup.find("ul", class_="menu")
        year_str_set = set()  # HACK to prevent duplicates
        for li in ul.find_all("li"):
            a = li.find("a")
            year_str = a.text.strip()
            if len(year_str) == 4 and year_str.isdigit():
                if year_str in year_str_set:
                    continue
                year_str_set.add(year_str)
                url_year = f'{cls.URL_BASE}/{a["href"]}'
                yield year_str, url_year

    @classmethod
    def gen_url_decisions(cls) -> Generator[tuple[str, str], None, None]:
        for lang in ["en", "si", "ta"]:
            yield lang, f"{cls.URL_DECISION_WITHOUT_LANG}&lang={lang}"

    @classmethod
    def gen_docs(cls) -> Generator["AbstractDoc", None, None]:
        for lang, url_decision in cls.gen_url_decisions():
            for year_str, url_year in cls.gen_url_years_for_url_decision(
                url_decision
            ):
                for date_str, url_date in cls.gen_url_dates_from_url_year(
                    year_str, url_year
                ):
                    yield from cls.gen_docs_from_url_date(
                        date_str, url_date, lang
                    )
