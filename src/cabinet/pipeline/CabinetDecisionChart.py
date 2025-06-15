import os
from datetime import datetime
from functools import cached_property

import matplotlib.pyplot as plt
import pandas as pd
from utils import Log

from cabinet.core import CabinetDecision

log = Log("CabinetDecisionChart")


class CabinetDecisionChart:
    IMAGE_PATH = os.path.join("images", "cabinet_decision_chart.png")

    @cached_property
    def date_to_n(self):
        cabinet_decisions = CabinetDecision.list_all()
        date_to_n = {}
        for decision in cabinet_decisions:
            date_str = decision.date_str
            if date_str not in date_to_n:
                date_to_n[date_str] = 0
            date_to_n[date_str] += 1
        return date_to_n

    def draw(self):
        plt.close()
        date_to_n = self.date_to_n
        date_strs = sorted(list(date_to_n.keys()))
        dates = [datetime.strptime(d, "%Y-%m-%d") for d in date_to_n]
        series = pd.Series(date_to_n.values(), index=dates)

        full_index = pd.date_range(
            start=series.index.min(), end=series.index.max(), freq="D"
        )
        daily_series = series.reindex(full_index).interpolate(method="time")
        moving_avg = daily_series.rolling(window=7).mean()

        plt.figure(figsize=(8, 4.5))
        plt.bar(
            series.index,
            series.values,
            width=3,
            color="pink",
            label="Event per Day",
        )
        plt.plot(
            moving_avg.index,
            moving_avg.values,
            linewidth=2,
            label="Last 7-days",
            color="red",
        )
        plt.title(
            "Cabinet Decisions in Sri Lanka"
            + f" ({date_strs[0]} - {date_strs[-1]})"
        )
        plt.xlabel("Date")
        plt.ylabel("Cabinet Decisions")
        plt.xticks(rotation=45)
        plt.grid(True, axis="y")
        plt.legend()
        plt.tight_layout()
        plt.savefig(self.IMAGE_PATH, dpi=150)
        plt.close()
        log.info(f"Wrote {self.IMAGE_PATH}")
