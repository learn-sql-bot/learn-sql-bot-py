from dataclasses import dataclass


@dataclass
class SQLRunnerResult:
    executed: bool
    rows: list = None
    columns: list = None
    errors: list = None

    def has_errors(self) -> bool:
        return len(self.errors) > 0
