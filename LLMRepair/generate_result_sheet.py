import json
import os
import pandas as pd

dataset_name = "106-dataset"
database_path = os.path.join("..", "training-data", dataset_name, "bugs-data")
result_sheet_folder = os.path.join("..", "training-data", "result-sheet", dataset_name)

if not os.path.exists(result_sheet_folder):
    os.makedirs(result_sheet_folder)

use_strata = 1
only_available_fact_strata = 1

if use_strata == 1:
    data = {
        "Project": [],
        "Bug_id": [],
        "Strata 1:": [],
        "Strata 2": [],
        "Strata 3": [],
        "Strata 4": [],
        "Strata 5": [],
        "Strata 6": [],
        "Strata 7": [],
        "Pass Test": [],
        "result_filename": []
    }
else:
    data = {
        "Project": [],
        "Bug_id": [],
        "1.1.1 Buggy function code": [],
        "1.1.2 buggy function docstring": [],
        "1.2.1 Buggy class declaration": [],
        "1.2.2 buggy class docstring": [],
        "1.2.3 Buggy class scope invoked method signature": [],
        "1.3.1 Buggy file name": [],
        "1.3.2 Buggy file scope invoked function signature": [],
        "1.4.1 Test code": [],
        "1.4.2 Test file name": [],
        "2.1.1 Error message": [],
        "2.1.2 Error stack trace": [],
        "2.1.3 Variable runtime value": [],
        "2.1.4 Variable runtime type": [],
        "2.1.5 Angelic value": [],
        "2.1.6 Angelic type": [],
        "3.1.1 Github linked issue title": [],
        "3.1.2 Github linked issue description": [],
        "cot Chain of Thought prompt technique": [],
        "Pass Test": [],
        "result_filename": []
    }

count = 0
for project_name in os.listdir(database_path):
    project_path = os.path.join(database_path, project_name)
    for bug_id in os.listdir(project_path):
        bug_path = os.path.join(project_path, bug_id)
        for result_file_name in os.listdir(bug_path):
            if "_result_1.json" not in result_file_name:
                continue

            with open(os.path.join(bug_path, result_file_name), "r") as result_file:
                result = json.load(result_file)
                pass_test = result[f"{project_name}:{bug_id}"]

            with open(os.path.join(bug_path, result_file_name.replace("result", "response")), "r") as response_file:
                response = json.load(response_file)
                if only_available_fact_strata == 0:
                    fact_bitvector: dict = response[project_name][0]["bitvector"]
                    strata_bitvector: dict = response[project_name][0]["strata"]
                else:
                    fact_bitvector: dict = response[project_name][0]["available_bitvector"]
                    strata_bitvector: dict = response[project_name][0]["available_strata"]

            data["Project"].append(project_name)
            data["Bug_id"].append(bug_id)

            if use_strata == 1:
                data["Strata 1:"].append(strata_bitvector["1"])
                data["Strata 2"].append(strata_bitvector["2"])
                data["Strata 3"].append(strata_bitvector["3"])
                data["Strata 4"].append(strata_bitvector["4"])
                data["Strata 5"].append(strata_bitvector["5"])
                data["Strata 6"].append(strata_bitvector["6"])
                data["Strata 7"].append(strata_bitvector["7"])
            else:
                data["1.1.1 Buggy function code"].append(fact_bitvector["1.1.1"])
                data["1.1.2 buggy function docstring"].append(fact_bitvector["1.1.2"])
                data["1.2.1 Buggy class declaration"].append(fact_bitvector["1.2.1"])
                data["1.2.2 buggy class docstring"].append(fact_bitvector["1.2.2"])
                data["1.2.3 Buggy class scope invoked method signature"].append(fact_bitvector["1.2.3"])
                data["1.3.1 Buggy file name"].append(fact_bitvector["1.3.1"])
                data["1.3.2 Buggy file scope invoked function signature"].append(fact_bitvector["1.3.2"])
                data["1.4.1 Test code"].append(fact_bitvector["1.4.1"])
                data["1.4.2 Test file name"].append(fact_bitvector["1.4.2"])
                data["2.1.1 Error message"].append(fact_bitvector["2.1.1"])
                data["2.1.2 Error stack trace"].append(fact_bitvector["2.1.2"])
                data["2.1.3 Variable runtime value"].append(fact_bitvector["2.1.3"])
                data["2.1.4 Variable runtime type"].append(fact_bitvector["2.1.4"])
                data["2.1.5 Angelic value"].append(fact_bitvector["2.1.5"])
                data["2.1.6 Angelic type"].append(fact_bitvector["2.1.6"])
                data["3.1.1 Github linked issue title"].append(fact_bitvector["3.1.1"])
                data["3.1.2 Github linked issue description"].append(fact_bitvector["3.1.2"])
                data["cot Chain of Thought prompt technique"].append(fact_bitvector["cot"])

            data["Pass Test"].append(pass_test)
            data["result_filename"].append(result_file_name)

df = pd.DataFrame(data)
if use_strata == 1:
    df.to_excel(os.path.join(result_sheet_folder, "raw_result_strata.xlsx"), index=False)
else:
    df.to_excel(os.path.join(result_sheet_folder, "raw_result_fact.xlsx"), index=False)
