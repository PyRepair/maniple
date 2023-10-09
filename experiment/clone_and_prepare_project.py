import os
import subprocess
import json

WORK_DIR = os.getcwd()
BENCHMARK_PATH = os.path.join(WORK_DIR, "..", "benchmarks")


def prepare_local_PyRepair_repo():
    os.chdir(BENCHMARK_PATH)

    if os.path.exists("PyRepair"):
        os.chdir("PyRepair")
        subprocess.run(["git", "pull"], check=True)

    else:
        # git clone
        subprocess.run(["git", "clone", "git@github.com:PyRepair/PyRepair.git"], check=True)

        os.chdir("PyRepair")
        subprocess.run(["python3.11", "-m", "pip", "install", "-r", "requirements.txt", "--break-system-packages"],
                       check=True)
        os.chdir("benchmark_wrangling/BugsInPy")
        subprocess.run(["python3.11", "-m", "pip", "install", "-r", "requirements.txt", "--break-system-packages"],
                       check=True)

        subprocess.run(["python3.11", "bgp.py", "update_bug_records"], check=True)

    os.chdir(WORK_DIR)


def clone_and_prepare_bug(project_name: str, bug_id: int):
    prepare_success_file_path = os.path.join(BENCHMARK_PATH, project_name, str(bug_id), ".prepare_success")
    prepare_failure_file_path = os.path.join(BENCHMARK_PATH, project_name, str(bug_id), ".prepare_failure")

    if os.path.exists(prepare_success_file_path) or os.path.exists(prepare_failure_file_path):
        print(f"Bug {bug_id} already prepared")
        return

    os.chdir(BENCHMARK_PATH)

    os.makedirs(project_name, exist_ok=True)
    os.chdir(project_name)

    os.makedirs(str(bug_id), exist_ok=True)
    os.chdir(str(bug_id))

    try:
        subprocess.run(["cp", "-r", os.path.join(BENCHMARK_PATH, "PyRepair"), "."], check=True)

        os.chdir("PyRepair/benchmark_wrangling/BugsInPy")

        subprocess.run(["python3.11", "bgp.py", "clone", "--bug_list", f"{project_name}:{bug_id}"],
                       check=True)

        prep_output = subprocess.run(["python3.11", "bgp.py", "prep", "--bug_list", f"{project_name}:{bug_id}"],
                                     check=True, capture_output=True, text=True)

        stdout = prep_output.stdout
        if "TestStatus.USAGE_ERROR" in stdout:
            with open(prepare_failure_file_path, "w") as f:
                f.write(stdout)
        else:
            with open(prepare_success_file_path, "w") as f:
                f.write(stdout)

    except subprocess.CalledProcessError as e:
        print(f"Error while cloning and preparing bug {bug_id}: {e}")
        with open(prepare_failure_file_path, "w") as f:
            f.write(str(e))

    finally:
        os.chdir(BENCHMARK_PATH)


if __name__ == '__main__':
    test_bugs_file = os.path.join(WORK_DIR, "..", "database", "subsets-list", "106-subset.json")

    os.makedirs(BENCHMARK_PATH, exist_ok=True)

    prepare_local_PyRepair_repo()

    with open(test_bugs_file) as f:
        test_bugs = json.load(f)

        for project in test_bugs.keys():
            for _bug_id in test_bugs[project]:
                clone_and_prepare_bug(project, _bug_id)

    os.chdir(WORK_DIR)
