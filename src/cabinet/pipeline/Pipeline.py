import random

from utils import Log

from cabinet.core import CabinetDecision
from cabinet.pipeline.CabinetDecisionChart import CabinetDecisionChart
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
        year_pages = list(contents_page.year_page_idx.value())
        random.shuffle(year_pages)
        for year_page in year_pages:
            for day, day_page in year_page.day_page_idx.items():
                log.debug(f"Processing {day}")
                for (
                    decision_details_page
                ) in day_page.decision_details_page_list:
                    is_hot = False
                    if not decision_details_page.cabinet_decision_cold:
                        n_hot += 1
                        is_hot = True

                    cabinet_decision = decision_details_page.cabinet_decision
                    decision_list.append(cabinet_decision)
                    if is_hot:
                        log.debug(
                            f"🟢 {n_hot}/{max_n_hot} Added {cabinet_decision.key} 🆕"
                        )
                    if n_hot >= max_n_hot:
                        return decision_list

        log.info("✅ Add decisions added to database!")
        return decision_list

    def run(self, max_n_hot):
        self.get_cabinet_decision_list(max_n_hot)
        CabinetDecision.build_table()
        CabinetDecisionChart().draw()
        ReadMe().write()
