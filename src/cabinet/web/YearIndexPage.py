from functools import cached_property

from cabinet.web.CabinetWebPage import CabinetWebPage


class YearIndexPage(CabinetWebPage):
    def __init__(self):
        super().__init__(
            option="com_content",
            view="article",
            id="60",
            Itemid="104",
            lang="en",
        )

    @cached_property
    def year_to_year_page_list(self):
        soup = self.soup
        div = soup.find("div", class_="moduletable")
        ul = div.find("ul")
        li_list = ul.find_all("li")
        idx = {}
        for li in li_list:
            href = li.find("a")["href"]
            year = li.text.strip()
            idx[year] = CabinetWebPage.from_url(href)
        return idx
