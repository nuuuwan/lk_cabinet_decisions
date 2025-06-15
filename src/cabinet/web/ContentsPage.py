from functools import cached_property

from cabinet.web.CabinetWebPage import CabinetWebPage
from cabinet.web.YearPage import YearPage


class ContentsPage(CabinetWebPage):
    def __init__(self):
        super().__init__(
            option="com_content",
            view="article",
            id="60",
            Itemid="104",
            lang="en",
        )

    @cached_property
    def year_page_idx(self):
        soup = self.soup
        div = soup.find("div", class_="moduletable")
        ul = div.find("ul")
        li_list = ul.find_all("li")
        year_and_url = []
        for li in li_list:
            a = li.find("a")
            url = a["href"]
            year = a.text.strip()
            if not year.isdigit() or len(year) != 4:
                continue
            year_and_url.append((year, url))

        year_and_url.sort(key=lambda x: x[0], reverse=True)
        return {year: YearPage(year, url) for year, url in year_and_url}

    def get_year_page(self, year):
        if year not in self.year_page_idx:
            raise ValueError(f"Year {year} not found.")
        return self.year_page_idx[year]
