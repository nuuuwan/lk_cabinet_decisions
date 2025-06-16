import random

from utils import Log

from cabinet.core import CabinetDecision
from cabinet.pipeline.CabinetDecisionChart import CabinetDecisionChart
from cabinet.pipeline.ReadMe import ReadMe
from cabinet.web import ContentsPage

log = Log("Pipeline")


class Pipeline:
    def __init__(self, do_shuffle=True):
        log.debug(f"{do_shuffle=}")
        self.do_shuffle = do_shuffle

    @property
    def year_page_list(self):
        contents_page = ContentsPage()
        year_pages = list(contents_page.year_page_idx.values())
        if self.do_shuffle:
            log.debug("Shuffling year pages")
            random.shuffle(year_pages)
        return year_pages

    @staticmethod
    def __process_decision_details_page__(
        decision_details_page, decision_list, max_n_hot, n_hot
    ):
        is_hot = False
        if not decision_details_page.cabinet_decision_cold:
            n_hot += 1
            is_hot = True

        cabinet_decision = decision_details_page.cabinet_decision
        decision_list.append(cabinet_decision)
        if is_hot:
            log.debug(f"🟢 {n_hot}/{max_n_hot} Added {cabinet_decision.key} 🆕")
        return decision_list, n_hot

    def get_cabinet_decision_list(self, max_n_hot):
        decision_list = []
        n_hot = 0
        for year_page in self.year_page_list:
            for day, day_page in year_page.day_page_idx.items():
                log.debug(f"Processing {day}")
                for (
                    decision_details_page
                ) in day_page.decision_details_page_list:
                    decision_list, n_hot = (
                        self.__process_decision_details_page__(
                            decision_details_page,
                            decision_list,
                            max_n_hot,
                            n_hot,
                        )
                    )
                if n_hot >= max_n_hot:
                    log.info(f"🛑 Reached max hot decisions: {max_n_hot}")
                    return decision_list

        log.info("✅ Add decisions added to database!")
        return decision_list

    def run(self, max_n_hot):
        self.get_cabinet_decision_list(max_n_hot)
        CabinetDecision.build_table()
        CabinetDecisionChart().draw()
        ReadMe().write()
