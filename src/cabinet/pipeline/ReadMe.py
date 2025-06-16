import os
from functools import cached_property

from utils import File, Log, Time, TimeFormat

from cabinet.core import CabinetDecision
from cabinet.pipeline.CabinetDecisionChart import CabinetDecisionChart

log = Log("ReadMe")


class ReadMe:
    PATH = "README.md"

    @cached_property
    def header_lines(self):
        return [
            "# 🇱🇰 Cabinet Decisions – Sri Lanka",
            "",
            "A structured, real-time feed of official cabinet",
            "decisions from Sri Lanka.",
            "",
            "Data is available in TSV and JSON formats.",
            "",
            "This is **public data** — free to use, share, and",
            "build on.",
            "",
            "Perfect for researchers, journalists, civic tech",
            "projects, or anyone curious about governance in",
            "Sri Lanka.",
            "",
        ]

    @cached_property
    def chart_lines(self):
        return [
            f"![Cabinet Decision Chart]({CabinetDecisionChart.IMAGE_PATH})",
            "",
        ]

    @cached_property
    def summary_lines(self):
        cabinet_decisions = CabinetDecision.list_all()
        latest_decisions = cabinet_decisions[0]
        earliest_decision = cabinet_decisions[-1]
        n_cabinet_decisions = len(cabinet_decisions)
        last_updated_str = TimeFormat.TIME.format(Time.now())
        return [
            "## Data Summary",
            "",
            "| | |",
            "|:--|--:|",
            f"| Last Updated   | **{last_updated_str}**     |",
            f"| nDecisions   | **{
                n_cabinet_decisions:,}**     |",
            f"| Latest   | **{
                latest_decisions.date_str}** |",
            f"| Earliest | **{
                earliest_decision.date_str}** |",
            "",
        ]

    @cached_property
    def example_json_lines(self):
        latest_decision = CabinetDecision.list_all()[0]
        return [
            "## Example JSON Data for a single Cabinet Decision",
            "",
            "```json",
            f"{latest_decision.to_json()}",
            "```",
            "",
            f"[JSON Source]({latest_decision.local_url})",
            "",
        ]

    @cached_property
    def example_tsv_table_lines(self):
        n_rows_display = 3
        cabinet_decisions = CabinetDecision.list_all()
        n_rows_total = len(cabinet_decisions)
        cabinet_decisions_display = cabinet_decisions[:n_rows_display]

        lines = [
            "| date_str | decision_num | title | source_url | "
            "decision_details | key |",
            "|:--|--:|:--|:--|:--|:--|",
        ]
        for decision in cabinet_decisions_display:
            lines.append(
                f"| {decision.date_str} | "
                f"{decision.decision_num} | "
                f"{decision.title[:20]}... | "
                f"[{decision.source_url[:20]}...]({decision.source_url}) | "
                f"{decision.decision_details[:20]}... | "
                f"{decision.key} |"
            )
        lines.extend(
            [
                "",
                f"(These are the first {n_rows_display}"
                f" of **{n_rows_total:,}**"
                " rows of the full TSV data)",
                "",
            ]
        )
        return lines

    @cached_property
    def example_tsv_lines(self):
        file_size_m = os.path.getsize(
            CabinetDecision.CABINET_DESICIONS_TABLE_PATH
        ) / (1000 * 1000)
        return [
            "## Example TSV Data",
            "",
            f"[Complete TSV]({CabinetDecision.CABINET_DESICIONS_TABLE_PATH})"
            + f" ({file_size_m:.2f} MB)",
            "",
        ] + self.example_tsv_table_lines

    @cached_property
    def last_n_decisions_lines(self):
        N_LATEST = 3
        cabinet_decisions = CabinetDecision.list_all()
        latest_decisions = cabinet_decisions[:N_LATEST]
        lines = [f"## Last {N_LATEST} Cabinet Decisions", ""]
        for i_decision, decision in enumerate(latest_decisions, start=1):
            lines.extend(
                [
                    f"### {i_decision}) {decision.title}",
                    "",
                    f"*{decision.date_str}*, *#{decision.decision_num}*",
                    "",
                    f"[{
                        decision.source_url}]({
                        decision.source_url})",
                    "",
                    f"{decision.decision_details_cleaned}",
                    "",
                ]
            )
        return lines

    @cached_property
    def all_decisions_lines(self):
        cabinet_decisions = CabinetDecision.list_all()
        n_decisions = len(cabinet_decisions)
        lines = [f"## All Cabinet Decisions ({n_decisions:,})", ""]
        for decision in cabinet_decisions:
            lines.append(
                f"- [{decision.date_str}]"
                + f" [{decision.title}]({decision.local_url})",
            )
        return lines

    @cached_property
    def lines(self):
        return (
            self.header_lines
            + self.summary_lines
            + self.chart_lines
            + self.example_json_lines
            + self.example_tsv_lines
            + self.last_n_decisions_lines
            + self.all_decisions_lines
        )

    def write(self):
        File(self.PATH).write("\n".join(self.lines))
        log.info(f"Wrote {self.PATH}")
