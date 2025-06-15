import os
from dataclasses import dataclass
from functools import cached_property

from utils import Hash, JSONFile, Log, TSVFile

log = Log("CabinetDecision")


@dataclass
class CabinetDecision:
    date_str: str
    decision_num: int
    title: str
    source_url: str
    decision_details: str

    DIR_CABINET_DECISIONS = os.path.join("data", "cabinet_decisions")
    CABINET_DESICIONS_TABLE_PATH = os.path.join(
        "data", "cabinet_decisions.tsv"
    )

    @cached_property
    def title_hash(self):
        return Hash.md5(self.title)

    @staticmethod
    def __object_key__(date_str, decision_num, title):
        title_hash = Hash.md5(title)[:4]
        return f"{date_str}-{decision_num:03d}-{title_hash}"

    @cached_property
    def key(self):
        return self.__object_key__(
            self.date_str, self.decision_num, self.title
        )

    def to_dict(self):
        return {
            "key": self.key,
            "title": self.title,
            "source_url": self.source_url,
            "decision_details": self.decision_details,
            "date_str": self.date_str,
            "decision_num": self.decision_num,
        }

    @staticmethod
    def __json_file_path__(date_str, decision_num, title):

        year = date_str[:4]  # YYYY format
        year_and_month = date_str[:7]  # YYYY-MM format
        dir_year_and_month = os.path.join(
            "data", "cabinet_decisions", year, year_and_month
        )

        if not os.path.exists(dir_year_and_month):
            os.makedirs(dir_year_and_month)

        return os.path.join(
            dir_year_and_month,
            CabinetDecision.__object_key__(date_str, decision_num, title)
            + ".json",
        )

    @cached_property
    def json_file_path(self):
        return self.__json_file_path__(
            self.date_str, self.decision_num, self.title
        )

    @cached_property
    def json_file(self):
        return JSONFile(self.json_file_path)

    def write(self):
        self.json_file.write(self.to_dict())
        log.debug(f"Wrote {self.json_file_path}")

    @staticmethod
    def from_params(date_str, decision_num, title):
        json_file_path = CabinetDecision.__json_file_path__(
            date_str, decision_num, title
        )
        if os.path.exists(json_file_path):

            data = JSONFile(json_file_path).read()

            assert data["date_str"] == date_str
            assert data["decision_num"] == decision_num
            assert data["title"] == title

            if not all(
                [
                    data["date_str"] == date_str,
                    data["decision_num"] == decision_num,
                    data["title"] == title,
                ]
            ):
                raise ValueError(
                    "Invalid params for CabinetDecision.from params "
                    + str(
                        dict(
                            date_str=date_str,
                            decision_num=decision_num,
                            title=title,
                            data=data,
                        )
                    )
                )

            return CabinetDecision(
                date_str=data["date_str"],
                decision_num=data["decision_num"],
                title=data["title"],
                source_url=data["source_url"],
                decision_details=data["decision_details"],
            )

        return None

    @staticmethod
    def __get_data_file_path_list__():
        data_file_path_list = []
        for year in os.listdir(CabinetDecision.DIR_CABINET_DECISIONS):
            dir_year = os.path.join(
                CabinetDecision.DIR_CABINET_DECISIONS, year
            )
            for year_and_month in os.listdir(dir_year):
                dir_year_and_month = os.path.join(dir_year, year_and_month)
                for file_name in os.listdir(dir_year_and_month):
                    file_path = os.path.join(dir_year_and_month, file_name)
                    if not file_path.endswith(".json"):
                        continue
                    data_file_path_list.append(file_path)
        return data_file_path_list

    @staticmethod
    def __get_data_list__():
        data_list = []
        for file_path in CabinetDecision.__get_data_file_path_list__():
            data = JSONFile(file_path).read()
            data_list.append(data)
        data_list.sort(key=lambda x: x["key"], reverse=True)
        return data_list

    @staticmethod
    def list_all():
        return [
            CabinetDecision(
                date_str=data["date_str"],
                decision_num=data["decision_num"],
                title=data["title"],
                source_url=data["source_url"],
                decision_details=data["decision_details"],
            )
            for data in CabinetDecision.__get_data_list__()
        ]

    @staticmethod
    def build_table():
        data_list = CabinetDecision.__get_data_list__()
        TSVFile(CabinetDecision.CABINET_DESICIONS_TABLE_PATH).write(data_list)
        log.info(
            f"Wrote {len(data_list)} decisions"
            + f" to {CabinetDecision.CABINET_DESICIONS_TABLE_PATH}"
        )

    @cached_property
    def decision_details_cleaned(self):
        x = self.decision_details
        x = x.replace("*", "\n\n*")
        return x.lstrip("- ")
