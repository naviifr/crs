from dataclasses import dataclass

@dataclass
class Result:
    source: str
    type: str
    file: str
    line: int
    message: str
    severity: str
    evidence: dict