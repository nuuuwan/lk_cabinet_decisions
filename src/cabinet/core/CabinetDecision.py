import os
from dataclasses import dataclass
from functools import cached_property

from utils import Hash, JSONFile, Log

log = Log("CabinetDecision")


@dataclass
class CabinetDecision:
    date_str: str
    decision_num: int
    title: str
    source_url: str
    decision_details: str

    @cached_property
    def title_hash(self):
        return Hash.md5(self.title)

    @staticmethod
    def __object_key__(date_str, decision_num, title):
        title_hash = Hash.md5(title)[:4]
        return f"{date_str}-{decision_num:03d}-{title_hash}"

    @cached_property
    def key(self):
        return self.__object_key__(self.date_str, self.decision_num, self.title)

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

        year = date_str[:4]
        dir_year = os.path.join(
            "data",
            "cabinet_decisions",
            year,
        )
        if not os.path.exists(dir_year):
            os.makedirs(dir_year)

        return os.path.join(
            dir_year,
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
