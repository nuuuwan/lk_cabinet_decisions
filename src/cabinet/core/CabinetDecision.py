from dataclasses import dataclass


@dataclass
class CabinetDecision:
    decision_num: int
    title: str
    decision_details: str

    def to_dict(self):
        return {
            "decision_num": self.decision_num,
            "title": self.title,
            "decision_details": self.decision_details,
        }
