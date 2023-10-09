import os
import subprocess
import json

WORK_DIR = os.getcwd()
BENCHMARK_PATH = os.path.join(WORK_DIR, "..", "benchmarks")

os.makedirs(BENCHMARK_PATH, exist_ok=True)


def clone_and_prepare_bug(_bug_id):
    os.chdir(BENCHMARK_PATH)
    os.makedirs(_bug_id, exist_ok=True)
    os.chdir(_bug_id)

    # git clone
    subprocess.run(["git", "clone", "git@github.com:PyRepair/PyRepair.git"], check=True)

    os.chdir("PyRepair")
    subprocess.run(["python3.11", "-m", "pip", "install", "-r", "requirements.txt", "--break-system-packages"],
                   check=True)
    os.chdir("benchmark_wrangling/BugsInPy")
    subprocess.run(["python3.11", "-m", "pip", "install", "-r", "requirements.txt", "--break-system-packages"],
                   check=True)
    subprocess.run(["python3.11", "bgp.py", "update_bug_records"], check=True)
    subprocess.run(["python3.11", "bgp.py", "clone", "--bug_list", _bug_id], check=True)
    subprocess.run(["python3.11", "bgp.py", "prep", "--bug_list", _bug_id], check=True)

    os.chdir(BENCHMARK_PATH)


def extract_bug_ids_from_json_file(filename):
    with open(filename, 'r') as file:
        data = json.load(file)

    bug_id_list = [f"{project_name}:{bug_id}" for project_name, bug_ids in data.items() for bug_id in bug_ids]
    return bug_id_list


if __name__ == '__main__':
    result = extract_bug_ids_from_json_file(os.path.join(WORK_DIR, "..", "database", "subsets-list", "106-subset.json"))

    for bug_id in result:
        clone_and_prepare_bug(bug_id)

    os.chdir(WORK_DIR)
