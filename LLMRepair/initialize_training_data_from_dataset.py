import json
import os.path
import shutil

from utils import print_in_red

dataset = "16-16-dataset"

dataset_path = os.path.join("..", "experiment-initialization-resources", "datasets-list", dataset + ".json")
if not os.path.exists(dataset_path):
    print_in_red(f"dataset: {dataset} not exist")
else:
    with open(dataset_path, "r") as dataset_file:
        bug_list: dict = json.load(dataset_file)

    for project in bug_list.keys():
        for bid in bug_list[project]:
            bug_data_source = os.path.join("..", "experiment-initialization-resources", "bug-data", project, str(bid))
            if not os.path.exists(bug_data_source):
                print_in_red(f"no bug data for {project}:{bid}")
                continue

            project_destination = os.path.join("..", "training-data", dataset, project)
            bug_destination = os.path.join("..", "training-data", dataset, project, str(bid))

            if os.path.exists(bug_destination):
                shutil.rmtree(bug_destination)

            shutil.copytree(bug_data_source, os.path.join(project_destination, os.path.basename(bug_data_source)))
