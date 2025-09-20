import re
from typing import Generator

from scraper import AbstractDoc
from utils_future import WWW


class CabinetDecisionsWebMixin:

    URL_BASE = "https://www.cabinetoffice.gov.lk"
    URL_DECISIONS = (
        URL_BASE
        + "/cab/index.php"
        + "?option=com_content&view=article&id=63&Itemid=43&lang=en"
    )

    @classmethod
    def get_doc_from_url_details(
        cls, num, date_str, description, url_details
    ):
        www_details = WWW(url_details)
        soup = www_details.soup
        if not soup:
            return None
        div_title = soup.find("div", id="cab_heading_text_e")
        decision_details_title = div_title.text.strip()
        assert date_str in decision_details_title
        div_body = soup.find("div", id="cab_normal_text_e")
        decision_details_body = div_body.text.strip()
        return cls(
            num=num,
            date_str=date_str,
            description=description,
            url_metadata=url_details,
            lang="en",
            decision_details_title=decision_details_title,
            decision_details_body=decision_details_body,
        )

    @staticmethod
    def __clean_url__(url):
        url = re.sub(r"\s+", "", url)
        return url

    @classmethod
    def gen_docs_from_url_date(
        cls, date_str, url_date
    ) -> Generator["AbstractDoc", None, None]:
        www_date = WWW(url_date)
        soup = www_date.soup
        assert soup
        tables = soup.find_all("table", attrs={"width": "95%"})
        assert len(tables) == 3
        table = tables[1]
        for tr in table.find_all("tr"):
            tds = tr.find_all("td")
            assert len(tds) == 2
            num = tds[0].text.strip()
            a = tds[1].find("a")
            description = a.text.strip()
            url_details = f'{cls.URL_BASE}/cab/{a["href"]}'
            url_details = cls.__clean_url__(url_details)
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
        assert soup
        tables = soup.find_all("table", attrs={"width": "85%"})
        assert len(tables) == 2
        table = tables[1]
        for tr in table.find_all("tr"):
            for td in tr.find_all("td"):
                a = td.find("a")
                date_str = a.text.strip()
                assert (
                    len(date_str) == 10
                    and date_str[4] == "-"
                    and date_str[7] == "-"
                ), date_str
                assert date_str[:4] == year_str
                url_date = f'{cls.URL_BASE}/cab/{a["href"]}'
                yield date_str, url_date

    @classmethod
    def gen_urls_years(cls) -> Generator[tuple[str, str], None, None]:
        www_home = WWW(cls.URL_DECISIONS)
        soup = www_home.soup
        assert soup
        ul = soup.find("ul", class_="menu")
        for li in ul.find_all("li"):
            a = li.find("a")
            year_str = a.text.strip()
            assert len(year_str) == 4 and year_str.isdigit()
            url_year = f'{cls.URL_BASE}/{a["href"]}'
            yield year_str, url_year
