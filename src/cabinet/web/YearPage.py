from functools import cached_property

from cabinet.web.CabinetWebPage import CabinetWebPage
from cabinet.web.DayPage import DayPage


class YearPage(CabinetWebPage):
    def __init__(self, year, url):
        params = CabinetWebPage.get_params_from_url(url)

        if not all(
            [
                params["option"] == "com_content",
                params["view"] == "article",
                "id" in params,
                "Itemid" in params,
                len(year) == 4,
                year.isdigit(),
            ]
        ):
            raise ValueError(
                "Invalid params for YearPage: "
                + str(dict(year=year, params=params))
            )

        super().__init__(**params)
        self.year = year

    @cached_property
    def day_page_idx(self):
        soup = self.soup

        tables = soup.find_all("table", width="85%")
        table = tables[1]
        td_list = table.find_all("td")

        idx = {}
        for td in td_list:
            url = td.find("a")["href"]
            date_str = td.text.strip()
            params = CabinetWebPage.get_params_from_url(url)
            idx[date_str] = DayPage(
                date_str=date_str,
                params=params,
            )

        return idx

    def get_day_page(self, date_str):
        if date_str not in self.day_page_idx:
            raise ValueError(f"Day {date_str} not found .")
        return self.day_page_idx[date_str]
