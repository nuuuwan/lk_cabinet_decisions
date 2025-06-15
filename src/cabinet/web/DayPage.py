from functools import cached_property

from cabinet.web.CabinetWebPage import CabinetWebPage
from cabinet.web.DecisionDetailsPage import DecisionDetailsPage


class DayPage(CabinetWebPage):
    def __init__(self, day_str, params):
        if not all(
            [
                params.get("option") == "com_content",
                params.get("view") == "article",
                "id" in params,
                "Itemid" in params,
                params.get("dDate") == day_str,
                len(day_str) == 10,  # Format: YYYY-MM-DD
            ]
        ):
            raise ValueError(
                "Invalid params for DayPage: "
                + str(dict(day_str=day_str, params=params))
            )

        super().__init__(**params)
        self.day_str = day_str

    @cached_property
    def decision_details_page_list(self):
        soup = self.soup
        table = soup.find_all("table", width="95%")[1]
        decision_details_page_list = []
        for tr in table.find_all("tr"):
            td_list = tr.find_all("td")
            decision_num = int(td_list[0].text.strip())
            title = td_list[1].text.strip()
            href = td_list[1].find("a")["href"]
            params = CabinetWebPage.get_params_from_url(href)

            decision_details_page_list.append(
                DecisionDetailsPage(params, decision_num, title)
            )
        return decision_details_page_list
