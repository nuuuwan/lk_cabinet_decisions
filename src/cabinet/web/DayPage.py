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
