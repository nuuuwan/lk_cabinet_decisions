from utils import Log

from cabinet.web.ContentsPage import ContentsPage

log = Log("Pipeline")


class Pipeline:

    def get_cabinet_decision_list(self, limit: int = 10):
        contents_page = ContentsPage()
        decision_list = []
        for year, year_page in contents_page.year_page_idx.items():
            log.debug(f"Processing {year}")
            for day, day_page in year_page.day_page_idx.items():
                log.debug(f"\tProcessing {day}")
                for (
                    decision_details_page
                ) in day_page.decision_details_page_list:
                    cabinet_decision = decision_details_page.cabinet_decision
                    decision_list.append(cabinet_decision)
                    if len(decision_list) >= limit:
                        return decision_list

        return decision_list
