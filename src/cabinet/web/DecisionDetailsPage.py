from functools import cached_property

from cabinet.core.CabinetDecision import CabinetDecision
from cabinet.web.CabinetWebPage import CabinetWebPage


class DecisionDetailsPage(CabinetWebPage):

    def __init__(self, params, date_str, decision_num, title):
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
        self.date_str = date_str
        self.decision_num = decision_num
        self.title = title

    @cached_property
    def decision_details(self):
        soup = self.soup
        content_div = soup.find("div", id="cab_normal_text_e")
        return content_div.text.strip()

    @cached_property
    def __cabinet_decision_hot__(self):
        return CabinetDecision(
            date_str=self.date_str,
            decision_num=self.decision_num,
            title=self.title,
            source_url=self.url,
            decision_details=self.decision_details,
        )

    @property
    def cabinet_decision_cold(self):
        return CabinetDecision.from_params(
            date_str=self.date_str,
            decision_num=self.decision_num,
            title=self.title,
        )

    @cached_property
    def cabinet_decision(self):
        cabinet_decision_cold = self.cabinet_decision_cold
        if cabinet_decision_cold:
            return cabinet_decision_cold

        cabinet_decision_hot = self.__cabinet_decision_hot__
        cabinet_decision_hot.write()
        return cabinet_decision_hot
