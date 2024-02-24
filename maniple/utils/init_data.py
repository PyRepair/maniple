import argparse
import json
import os.path
import shutil

from maniple.utils.misc import print_in_red, print_in_yellow


def init_data(output_dir: str, dataset):
    """
    Initialize the dataset by copying the bug data from the experiment-initialization-resources/bug-data to the
    output directory. The bug data is organized in the following way:
    - output_dir
        - project1
            - bug1
                - bug_data
                    - ...
            - bug2
                - bug_data
                    - ...
        - project2
            - bug1
                - bug_data
                    - ...
            - bug2
                - bug_data
                    - ...
    """
    if dataset is None:
        print_in_yellow("no dataset specified, using default dataset: 16-16-dataset")
        dataset = "16-16-dataset"

    init_data_folder = os.path.join(
        os.getcwd(),
        "experiment-initialization-resources"
    )

    dataset_path = os.path.join(
        init_data_folder,
        "datasets-list",
        dataset + ".json",
    )

    if not os.path.exists(dataset_path):
        print_in_red(f"dataset: {dataset} not exist, please ensure experiment-initialization-resources folder is under current working directory")
    else:
        with open(dataset_path, "r") as dataset_file:
            bug_list: dict = json.load(dataset_file)

        for project in bug_list.keys():
            for bid in bug_list[project]:
                bug_data_source = os.path.join(
                    init_data_folder,
                    "bug-data",
                    project,
                    str(bid),
                )
                if not os.path.exists(bug_data_source):
                    print_in_red(f"no bug data for {project}:{bid}")
                    continue

                project_destination = os.path.join(output_dir, project)
                bug_destination = os.path.join(output_dir, project, str(bid))

                if os.path.exists(bug_destination):
                    shutil.rmtree(bug_destination)

                shutil.copytree(
                    bug_data_source,
                    os.path.join(
                        project_destination, os.path.basename(bug_data_source)
                    ),
                )

                for root, dirs, files in os.walk(bug_destination):
                    for file in files:
                        if "prompt.md" in file:
                            os.remove(os.path.join(root, file))


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("output_dir", help="the name of the dataset to initialize")
    arg_parser.add_argument(
        "--dataset", help="the name of the dataset to initialize", required=False
    )
    args = arg_parser.parse_args()

    init_data(args.output_dir, args.dataset)
