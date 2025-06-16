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
    TIME_FORMAT = "%Y-%m"

    @cached_property
    def time_str_to_n(self):
        cabinet_decisions = CabinetDecision.list_all()
        time_str_to_n = {}
        for decision in cabinet_decisions:
            time_str = decision.date_str[:7]  # TIME_FORMAT
            if time_str not in time_str_to_n:
                time_str_to_n[time_str] = 0
            time_str_to_n[time_str] += 1
        return time_str_to_n

    def __prepare_data__(self):

        time_str_to_n = self.time_str_to_n
        n_decisions = sum(time_str_to_n.values())
        time_strs = sorted(list(time_str_to_n.keys()))
        dates = [
            datetime.strptime(d, CabinetDecisionChart.TIME_FORMAT)
            for d in time_str_to_n
        ]
        series = pd.Series(time_str_to_n.values(), index=dates)

        return series, time_strs, n_decisions

    def __draw_chart__(self):
        series, time_strs, n_decisions = self.__prepare_data__()
        plt.figure(figsize=(8, 4.5))
        plt.bar(
            series.index,
            series.values,
            width=pd.Timedelta(days=24),
            color="grey",
            label="Decisions per Month",
        )
        plt.plot(
            series.rolling(window=12, min_periods=1).mean(),
            label="12-Month Moving Avg",
            linewidth=2,
            color="black",
        )

        plt.title(
            f"{n_decisions} Cabinet Decisions in Sri Lanka"
            + f" ({time_strs[0]} - {time_strs[-1]})"
        )
        plt.xlabel("Date")
        plt.ylabel("Cabinet Decisions")
        plt.xticks(rotation=45)
        plt.grid(True, axis="y")
        plt.legend(loc="best")
        plt.tight_layout()

    def __annotate_chart_single__(self, start_str, end_str, label, color):
        ax = plt.gca()

        start_date = datetime.strptime(
            start_str[:7], CabinetDecisionChart.TIME_FORMAT
        )
        end_date = datetime.strptime(
            end_str[:7], CabinetDecisionChart.TIME_FORMAT
        )
        mid_date = start_date + (end_date - start_date) / 2

        ax.axvspan(
            start_date,
            end_date,
            facecolor=color,
            alpha=0.2,
            edgecolor="white",
            linewidth=1,
        )
        ax.text(mid_date, 110, label, ha="center", va="center", fontsize=6)

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
