from dataclasses import dataclass


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
