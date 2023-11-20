import os
import subprocess
import json


FOLDERS = ['first-stratum']


def get_bugid_from_bugdir(bugdir: str):
    parts = bugdir.split('-')
    return "-".join(parts[:len(parts)-1]) + ":" + parts[len(parts)-1]


def collect_facts(bugid: str, full_bugdir_path: str):
    subprocess.run(["bgp", "clone", "--bugids", bugid])
    console_output = subprocess.run(["bgp", "extract_features", "--bugids", bugid], capture_output=True)
    decoded_string = console_output.stdout.decode('utf-8')
    json_output = json.loads(decoded_string)

    with open(os.path.join(full_bugdir_path, "bug-data.json"), "w") as f:
        json.dump(json_output, f, indent=4)

    



collect_facts("black:10", "first-stratum/black-10")


