from analysis import semgrep, libfuzzer
import verify

try:
    libfuzzer.libfuzzer_initiate()
    semgrep.semgrep_initiate()
    verify.verify_initiate()
    print("done")

except Exception as e:
    print(str(e))