import os
from functools import cached_property

from utils import JSONFile, Log, TSVFile

from cabinet.web.ContentsPage import ContentsPage

log = Log("Pipeline")


class Pipeline:
    DIR_CABINET_DECISIONS = os.path.join("data", "cabinet_decisions")
    CABINET_DESICIONS_TABLE_PATH = os.path.join("data", "cabinet_decisions.tsv")

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

    @cached_property
    def data_file_path_list(self):
        data_file_path_list = []
        for year in os.listdir(self.DIR_CABINET_DECISIONS):
            dir_year = os.path.join(self.DIR_CABINET_DECISIONS, year)
            for year_and_month in os.listdir(dir_year):
                dir_year_and_month = os.path.join(dir_year, year_and_month)
                for file_name in os.listdir(dir_year_and_month):
                    file_path = os.path.join(dir_year_and_month, file_name)
                    if not file_path.endswith(".json"):
                        continue
                    data_file_path_list.append(file_path)
        return data_file_path_list

    @cached_property
    def data_list(self):
        data_list = []
        for file_path in self.data_file_path_list:
            data = JSONFile(file_path).read()
            data_list.append(data)
        data_list.sort(key=lambda x: x["key"], reverse=True)
        return data_list

    def build_table(self):
        data_list = self.data_list
        TSVFile(self.CABINET_DESICIONS_TABLE_PATH).write(data_list)
        log.info(
            f"Wrote {len(data_list)} decisions"
            + f" to {self.CABINET_DESICIONS_TABLE_PATH}"
        )

    def run(self, limit):
        self.get_cabinet_decision_list(limit)
        self.build_table()
