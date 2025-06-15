from functools import cached_property

from cabinet.core.CabinetDecision import CabinetDecision
from cabinet.web.CabinetWebPage import CabinetWebPage


class DecisionDetailsPage(CabinetWebPage):

    def __init__(self, params, decision_num, title):
        if not all(
            [
                params.get("option") == "com_content",
                params.get("view") == "article",
                "id" in params,
                "Itemid" in params,
                "dID" in params,
            ]
        ):
            raise ValueError(
                "Invalid params for DecisionDetailsPage: " + str(params)
            )
        super().__init__(**params)
        self.decision_num = decision_num
        self.title = title

    @cached_property
    def decision_details(self):
        soup = self.soup
        content_div = soup.find("div", id="cab_normal_text_e")
        return content_div.text.strip()

    @cached_property
    def cabinet_decision(self):
        return CabinetDecision(
            decision_num=self.decision_num,
            title=self.title,
            decision_details=self.decision_details,
        )
