from functools import cached_property

from utils import File, Log

log = Log("ReadMe")


class ReadMe:
    PATH = "README.md"

    @cached_property
    def lines(self):
        return [
            "# Cabinet Decisions",
            "This repository contains sturctured data about cabinet desisions"
            + " in Sri Lanka - updated in real-time.",
        ]

    def write(self):
        File(self.PATH).write("\n\n".join(self.lines))
        log.info(f"Wrote {self.PATH}")
