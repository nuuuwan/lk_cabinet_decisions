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

    def __prepare_data__(self):
        date_to_n = self.date_to_n
        date_strs = sorted(list(date_to_n.keys()))
        dates = [datetime.strptime(d, "%Y-%m-%d") for d in date_to_n]
        series = pd.Series(date_to_n.values(), index=dates)

        full_index = pd.date_range(
            start=series.index.min(), end=series.index.max(), freq="D"
        )
        daily_series = series.reindex(full_index).interpolate(method="time")
        moving_avg = daily_series.rolling(window=7).mean()

        return series, moving_avg, date_strs

    def __draw_chart__(self):
        series, _, date_strs = self.__prepare_data__()
        plt.figure(figsize=(8, 4.5))
        plt.bar(
            series.index,
            series.values,
            width=3,
            color="grey",
            label="Event per Day",
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

    def __annotate_chart_single__(self, start_str, end_str, label, color):
        ax = plt.gca()

        start_date = datetime.strptime(start_str, "%Y-%m-%d")
        end_date = datetime.strptime(end_str, "%Y-%m-%d")
        mid_date = start_date + (end_date - start_date) / 2

        ax.axvspan(
            start_date,
            end_date,
            facecolor=color,
            alpha=0.1,
            edgecolor="white",
            linewidth=1,
        )
        ax.text(mid_date, 20, label, ha="center", va="center", fontsize=6)

    def __annotate_chart__(self):

        periods = [
            ("2010-04-23", "2013-01-28", "MR3", "blue"),
            ("2013-01-28", "2015-01-09", "MR4", "blue"),
            ("2015-01-12", "2015-08-17", "S1", "green"),
            ("2015-08-24", "2018-10-26", "S2", "green"),
            ("2018-10-29", "2018-12-15", "S3", "maroon"),
            ("2018-12-20", "2019-11-21", "S4", "green"),
            ("2019-11-21", "2020-08-12", "GR1", "maroon"),
            ("2020-08-12", "2022-04-03", "GR2", "maroon"),
            ("2022-04-18", "2022-07-14", "GR3,4", "maroon"),
            ("2022-07-22", "2024-09-23", "W", "green"),
            ("2024-09-24", "2024-11-18", "D1", "red"),
            ("2024-11-18", "2029-11-18", "D2", "red"),
        ]

        for start_str, end_str, label, color in periods:
            self.__annotate_chart_single__(start_str, end_str, label, color)

    def draw(self):
        plt.close()
        self.__draw_chart__()
        self.__annotate_chart__()
        plt.savefig(self.IMAGE_PATH, dpi=150)
        plt.close()
        log.info(f"Wrote {self.IMAGE_PATH}")
