import subprocess

import json
from analysis.libfuzzer import build_fuzzer, run_fuzzer


CLANG = r"C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Tools\Llvm\x64\bin\clang.exe"
EVIDENCE= {"test": '',
           "stages":{}}

def json_write(evidence):

    with open(f'./results/libfuzz.json', 'w') as file:
        json.dump(evidence, file, indent= 4)

def collect_evidence(stage:str, passed:bool, result:subprocess.CompletedProcess):

    EVIDENCE["stages"][stage] =  passed
    EVIDENCE[stage] = {
                        "passed":passed,
                        "return_code":result.returncode,
                        "stdout":result.stdout,
                        "stderr":result.stderr,
                    }

def build_regression_test():

    stage = "build_regression_test"
    command = [
        CLANG,
        "-g",
        "-fsanitize=address",
        "./target/libfuzz/target.c",
        "./target/libfuzz/test_target.c",
        "-o",
        "test.exe",
    ]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )

    print(stage,"\nExit code:", result.returncode)

    if result.returncode == 0:
        print("Build successful")
        collect_evidence(stage, True, result)
    else:
        collect_evidence(stage, False, result)
        raise Exception(f"Build Failed:\n{result.stderr}")

def verify_test():

    stage = "verify_test"
    command = [
        "./test.exe"
    ]

    result = subprocess.run(
            command,
            capture_output=True,
            text=True,
        )

    print(stage,"\nExit code:", result.returncode)
    
    if result.returncode == 0:
        print("Verified")
        print(result.stdout)
        collect_evidence(stage, True, result)
    else:
        collect_evidence(stage, False, result)
        raise Exception(f"Verification failed:\n{result.stderr}\n{result.stdout}")
    


    print(stage,"\nExit code:", result.returncode)

    if result.returncode == 0:
        print("Fuzzer build successful")
        collect_evidence(stage, True, result)
    else:
        collect_evidence(stage, False, result)
        raise Exception(f"Fuzzer build failed:\n{result.stderr}")

def replay_crash(reproducer:str):

    stage = "replay_crash"
    command = [
            "fuzzer.exe",
            reproducer
        ]

    result = subprocess.run(
                command,
                capture_output=True,
                text=True
            )
    print(stage,"\nExit code:", result.returncode)
    
    if result.returncode == 0:
        print("Crash did not occur, patch successful")
        print(result.stdout)
        collect_evidence(stage, True, result)
    else:
        collect_evidence(stage, False, result)
        raise Exception(f"Crash occured, patch failed:\n{result.stderr}")

    print(stage,"\nExit code:", result.returncode)

    if result.returncode == 0:
        print("No error detected")
        print(result.stdout)
        collect_evidence(stage, True, result)
    else:
        collect_evidence(stage, False, result)
        raise Exception(f"Error detected:\n{result.stderr}")

def verify_initiate():
    
    try:
        build_regression_test()
        verify_test()
        build_fuzzer()
        replay_crash("crash-ac45abaaef4dd6870924cfef9f0e842869951e8b")
        run_fuzzer()
        print("Verification Passed")
        EVIDENCE["test"] = True
        
    except Exception as e:
        EVIDENCE["test"] = False
        print("Verification Failed")
        print(e)
    
    finally:
        json_write(EVIDENCE)
