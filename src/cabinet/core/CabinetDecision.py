from dataclasses import dataclass
from functools import cached_property

from utils import Log

from scraper import AbstractDoc

log = Log("CabinetDecision")


@dataclass
class CabinetDecision(AbstractDoc):
    decision_details: str

    @cached_property
    def text_from_metadata(self) -> str:
        return "\n\n".join(
            [
                self.description,
                self.decision_details,
            ]
        )
