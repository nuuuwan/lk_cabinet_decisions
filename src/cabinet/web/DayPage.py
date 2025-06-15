from functools import cached_property

from cabinet.core.CabinetDecision import CabinetDecision
from cabinet.web.CabinetWebPage import CabinetWebPage


class DayPage(CabinetWebPage):
    def __init__(self, day_str, params):
        if not all(
            [
                params.get("option") == "com_content",
                params.get("view") == "article",
                "id" in params,
                "Itemid" in params,
                params.get("dDate") == day_str,
            ]
        ):
            raise ValueError("Invalid params for DayPage: " + str(params))

        super().__init__(**params)
        self.day_str = day_str

    @cached_property
    def cabinet_decision_list(self):
        soup = self.soup
        table = soup.find_all("table", width="95%")[1]
        decision_list = []
        for tr in table.find_all("tr"):
            td_list = tr.find_all("td")
            decision_num = int(td_list[0].text.strip())
            title = td_list[1].text.strip()

            decision = CabinetDecision(
                decision_num=decision_num,
                title=title,
            )
            decision_list.append(decision)
        return decision_list
