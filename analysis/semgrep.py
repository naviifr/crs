import subprocess
import sys
import json
from core.models import Result

def analyze():
    command = [
        "semgrep",
        r"--config=./rules/memory.yml",
        "--json",
        "./target/semgrep/static.c"
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

    with open(f'./results/semgrep.json', 'w') as file:
            json.dump(parse_json(data), file, indent= 4)
    print("Evidence Written")

def parse_json(data):

    result = data["results"][0]

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

    print(finding)

    Result("semgrep", finding["rule_id"], 
            finding["file"],
            finding["start_line"],
            finding["message"],
            finding["severity"],
            data)

    return finding

def semgrep_initiate():
    
    try:
        analyze()

    except Exception as e:
        print(str(e))
        sys.exit(2)

