import json
import os
import random
import pandas as pd

stratum_path = "../preliminary-study/first-stratum"
first_stratum_path = os.listdir(stratum_path)

data = {
    "Project": [],
    "Bug_id": [],
    "1.3.1: Buggy file name": [],
    "1.3.2: Buggy file scope invoked function signature": [],
    "1.2.1: Buggy class declaration": [],
    "1.2.2: buggy class docstring": [],
    "1.2.3: Buggy class scope invoked method signature": [],
    "1.1.2: buggy function docstring": [],
    "2.2.3: Variable runtime value": [],
    "2.2.4: Variable runtime type": [],
    "2.2.5: Angelic value": [],
    "2.2.6: Angelic type": [],
    "2.1.1: Test code": [],
    "2.1.2: Test file name": [],
    "2.2.1: Error message": [],
    "2.2.2: Error stack trace": [],
    "3.1.1: Github linked issue title": [],
    "3.1.2: Github linked issue description": [],
    "cot: Chain of Thought prompt technique": [],
    "Pass Test": [],
    "result_filename": []
}

for bug_dir in first_stratum_path:
    project_name = bug_dir.rsplit('-', 1)[0]
    bug_id = bug_dir.rsplit('-', 1)[1]

    bug_path = os.path.join(stratum_path, bug_dir)
    result_files = [path for path in os.listdir(bug_path) if "result" in path]

    for result_file_name in result_files:
        with open(os.path.join(bug_path, result_file_name), "r") as result_file:
            result = json.load(result_file)
            pass_test = result[f"{project_name}:{bug_id}"]

        used_facts = [int(char) for char in result_file_name[:17]]

        data["Project"].append(project_name)
        data["Bug_id"].append(bug_id)

        data["1.3.1: Buggy file name"].append(used_facts[0])
        data["1.3.2: Buggy file scope invoked function signature"].append(used_facts[1])
        data["1.2.1: Buggy class declaration"].append(used_facts[2])
        data["1.2.2: buggy class docstring"].append(used_facts[3])
        data["1.2.3: Buggy class scope invoked method signature"].append(used_facts[4])
        data["1.1.2: buggy function docstring"].append(used_facts[5])
        data["2.2.3: Variable runtime value"].append(used_facts[6])
        data["2.2.4: Variable runtime type"].append(used_facts[7])
        data["2.2.5: Angelic value"].append(used_facts[8])
        data["2.2.6: Angelic type"].append(used_facts[9])
        data["2.1.1: Test code"].append(used_facts[10])
        data["2.1.2: Test file name"].append(used_facts[11])
        data["2.2.1: Error message"].append(used_facts[12])
        data["2.2.2: Error stack trace"].append(used_facts[13])
        data["3.1.1: Github linked issue title"].append(used_facts[14])
        data["3.1.2: Github linked issue description"].append(used_facts[15])
        data["cot: Chain of Thought prompt technique"].append(used_facts[16])

        data["Pass Test"].append(pass_test)
        data["result_filename"].append(result_file_name)

df = pd.DataFrame(data)
df.to_excel(os.path.join("..", "preliminary-study", "first_stratum_raw_result.xlsx"), index=False)
