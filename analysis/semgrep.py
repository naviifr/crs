import subprocess
import sys
import json

def initiate_semgrep():
    command = [
        "semgrep",
        r"--config=./rules/memory.yml",
        "--json",
        "./target/static.c"
    ]

    result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace"
        )

    print("\nExit code:", result.returncode)

    if result.returncode == 0:
        print("Analysis successful")
        write_json(result.stdout)

    else:
        print("Error occured")
        print(result.stdout)
        print(result.stderr)


def write_json(evidence):

    data = json.loads(evidence)

    with open(f'./results/analysis.json', 'w') as file:
            json.dump(parse_json(data), file, indent= 4)
    print("Evidence Written")

def parse_json(data):

    findings = []

    for result in data["results"]:
        finding = {
            "rule_id": result["check_id"],
            "file": result["path"],
            "start_line": result["start"]["line"],
            "start_col": result["start"]["col"],
            "end_line": result["end"]["line"],
            "end_col": result["end"]["col"],
            "message": result["extra"]["message"],
            "severity": result["extra"]["severity"]
        }

        findings.append(finding)

    return findings

try:
    initiate_semgrep()


except Exception as e:
    print(str(e))
    sys.exit(2)