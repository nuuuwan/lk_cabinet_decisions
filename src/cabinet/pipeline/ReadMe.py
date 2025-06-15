from functools import cached_property

from utils import File, Log

from cabinet.core import CabinetDecision

log = Log("ReadMe")


class ReadMe:
    PATH = "README.md"

    @cached_property
    def header_lines(self):
        return [
            "# Cabinet Decisions 🇱🇰",
            "",
            "This repository contains sturctured data about cabinet desisions"
            + " in Sri Lanka 🇱🇰 - updated in real-time.",
            "[TSV Table of Cabinet Decisions]"
            + f"({CabinetDecision.CABINET_DESICIONS_TABLE_PATH})",
            "",
        ]

    @cached_property
    def summary_lines(self):
        cabinet_decisions = CabinetDecision.list_all()
        latest_decisions = cabinet_decisions[0]
        earliest_decision = cabinet_decisions[-1]
        n_cabinet_decisions = len(cabinet_decisions)
        return [
            "## Summary",
            "",
            "|:--|--:|",
            f"| Total Decisions in Database   | **{
                n_cabinet_decisions:,}**     |",
            f"| Latest decision in Database   | **{
                latest_decisions.date_str}** |",
            f"| Earliest decision in Database | **{
                earliest_decision.date_str}** |",
            "",
        ]

    @cached_property
    def latest_decisions_lines(self):
        N_LATEST = 10
        cabinet_decisions = CabinetDecision.list_all()
        latest_decisions = cabinet_decisions[:N_LATEST]
        lines = [f"## Latest Decisions ({N_LATEST})", ""]
        for i_decision, decision in enumerate(latest_decisions, start=1):
            lines.extend(
                [
                    f"### {i_decision}) {decision.title}",
                    "",
                    f"*{decision.date_str}*, *#{decision.decision_num}*",
                    "",
                    f"*Source:* [{
                        decision.source_url}]({
                        decision.source_url})",
                    "",
                    f"{decision.decision_details_cleaned}",
                    "",
                ]
            )
        return lines

    @cached_property
    def lines(self):
        return (
            self.header_lines
            + self.summary_lines
            + self.latest_decisions_lines
        )

    def write(self):
        File(self.PATH).write("\n".join(self.lines))
        log.info(f"Wrote {self.PATH}")
