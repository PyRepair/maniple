import json
import os
from prompt_generator import PromptGenerator

database_path = os.path.join("..", "experiment-initialization-resources", "bug-data")
bitvector_path = os.path.join("..", "experiment-initialization-resources", "strata-bitvectors")

for file in os.listdir(bitvector_path):
    if "0" not in file:
        with open(os.path.join(bitvector_path, file), "r") as input_bitvector_file:
            bitvector_strata = json.load(input_bitvector_file)

# print(bitvector_strata)

projects = os.listdir(database_path)
for project in projects:
    project_folder_path = os.path.join(database_path, project)
    if not os.path.isdir(project_folder_path):
        continue

    for bid in os.listdir(project_folder_path):
        bug_dir_path = os.path.join(project_folder_path, bid)
        if not os.path.isdir(bug_dir_path):
            continue

        # if project != "pandas":
        #     continue
        #
        # if bid != "122":
        #     continue

        try:
            prompt_generator = PromptGenerator(database_path, project, bid, bitvector_strata)

        except Exception as e:
            print(f"{project}:{bid} fail to extract facts in prompt")
            print(e)
            print()
