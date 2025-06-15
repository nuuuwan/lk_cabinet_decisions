import os
from dataclasses import dataclass
from functools import cached_property

from utils import JSONFile, Log

log = Log("CabinetDecision")


@dataclass
class CabinetDecision:
    date_str: str
    decision_num: int
    title: str
    source_url: str
    decision_details: str

    def to_dict(self):
        return {
            "date_str": self.date_str,
            "decision_num": self.decision_num,
            "title": self.title,
            "source_url": self.source_url,
            "decision_details": self.decision_details,
        }

    @staticmethod
    def __json_file_path__(date_str, decision_num, title):
        title_short = "".join(
            c if c.isalnum() else "_" for c in title.lower()[:20]
        )
        return os.path.join(
            "data",
            "cabinet_decisions",
            f"{date_str}-{decision_num:03d}-{title_short}.json",
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
