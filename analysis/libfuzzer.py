import subprocess
import json

CLANG = r"C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Tools\Llvm\x64\bin\clang.exe"
EVIDENCE= {"test": '',
           "stages":{}}
                    
    
def build_fuzzer():

    stage = "build_fuzzer"
    command = [
        CLANG,
        "-g", 
        "-fsanitize=fuzzer,address",
        "./target/libfuzz/target.c",
        "./target/libfuzz/fuzz_target.c",
        "-o",
        "fuzzer.exe",
    ]

    result = subprocess.run(
            command,
            capture_output=True,
            text=True
        )

    print(stage,"\nExit code:", result.returncode)

    if result.returncode == 0:
        print("Fuzzer build successful")
        collect_evidence(stage, True, result)
    else:
        collect_evidence(stage, False, result)
        raise Exception(f"Fuzzer build failed:\n{result.stderr}")

def run_fuzzer():

    stage = "run_fuzzer"
    command = [
         "fuzzer.exe",
         "./target/libfuzz/corpus",
         "-max_total_time=10"
    ]

    result = subprocess.run(
                command,
                capture_output=True,
                text=True
            )

    print(stage,"\nExit code:", result.returncode)

    if result.returncode == 0:
        print("No error detected")
        print(result.stdout)
        collect_evidence(stage, True, result)
    else:
        collect_evidence(stage, False, result)
        raise Exception(f"Error detected:\n{result.stderr}")

def collect_evidence(stage:str, passed:bool, result:subprocess.CompletedProcess):

    EVIDENCE["stages"][stage] =  passed
    EVIDENCE[stage] = {
                        "passed":passed,
                        "return_code":result.returncode,
                        "stdout":result.stdout,
                        "stderr":result.stderr,
                       }

def json_write(evidence):

    with open(f'./results/verification.json', 'w') as file:
        json.dump(evidence, file, indent= 4)

def libfuzzer_initiate():
    try:

        build_fuzzer()
        run_fuzzer()
        print("Fuzzing done")
        EVIDENCE["libfuzz"] = True

    except Exception as e:
        EVIDENCE["libfuzz"] = False
        print("Fuzzing Failed")
        print(e)
    
    finally:
        json_write(EVIDENCE)


