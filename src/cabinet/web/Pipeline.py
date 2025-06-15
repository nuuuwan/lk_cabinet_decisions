import os

from utils import Log, TSVFile

from cabinet.web.ContentsPage import ContentsPage

log = Log("Pipeline")


class Pipeline:
    CABINET_DESICIONS_TABLE_PATH = os.path.join(
        "data", "cabinet_decision.tsv"
    )

    def get_cabinet_decision_list(self, limit):
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

    def run(self, limit):
        decision_list = self.get_cabinet_decision_list(limit)
        d_list = [decision.to_dict() for decision in decision_list]
        TSVFile(self.CABINET_DESICIONS_TABLE_PATH).write(d_list)
        log.info(
            f"Saved {len(decision_list)} decisions"
            + f" to {self.CABINET_DESICIONS_TABLE_PATH}"
        )
