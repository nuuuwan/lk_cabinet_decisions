from cabinet.web.CabinetWebPage import CabinetWebPage


class YearPage(CabinetWebPage):
    def __init__(self, year, url):
        params = CabinetWebPage.get_params_from_url(url)

        if not all(
            [
                params["option"] == "com_content",
                params["view"] == "article",
                "id" in params,
                "Itemid" in params,
            ]
        ):
            raise ValueError(
                "Invalid URL parameters for YearPage: " + str(params)
            )

        super().__init__(**params)
        self.year = year
