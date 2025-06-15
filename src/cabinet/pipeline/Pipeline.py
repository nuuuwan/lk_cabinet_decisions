from utils import Log

from cabinet.core import CabinetDecision
from cabinet.pipeline.ReadMe import ReadMe
from cabinet.web import ContentsPage

log = Log("Pipeline")


class Pipeline:
    # HACK!
    # flake8: noqa: F401
    def get_cabinet_decision_list(self, max_n_hot):
        contents_page = ContentsPage()
        decision_list = []
        n_hot = 0
        for year, year_page in contents_page.year_page_idx.items():
            log.debug(f"Processing {year}")
            for day, day_page in year_page.day_page_idx.items():
                log.debug(f"\tProcessing {day}")
                for (
                    decision_details_page
                ) in day_page.decision_details_page_list:
                    if not decision_details_page.cabinet_decision_cold:
                        n_hot += 1

                    cabinet_decision = decision_details_page.cabinet_decision
                    decision_list.append(cabinet_decision)
                    if n_hot >= max_n_hot:
                        return decision_list

        return decision_list

    def run(self, max_n_hot):
        self.get_cabinet_decision_list(max_n_hot)
        CabinetDecision.build_table()
        ReadMe().write()
