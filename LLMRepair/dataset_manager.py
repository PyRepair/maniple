import json
from typing import Literal, Union
import os

from utils import NotSupportedError, IGNORED_BUGS

DatasetType = Union[
    Literal["106subset"],
    Literal["395subset"],
    Literal["first-stratum"],
    Literal["second-stratum"],
]


def load_bugids_from_dataset(
    dataset: DatasetType, exclude_projects=[], test_mode=False
):
    current_script_path = os.path.dirname(os.path.abspath(__file__))

    if dataset == "106subset":
        dataset_indices_file_path = os.path.join(
            current_script_path,
            "..",
            "training-data",
            "subsets-list",
            "106-dataset.json",
        )

    elif dataset == "395subset":
        dataset_indices_file_path = os.path.join(
            current_script_path,
            "..",
            "training-data",
            "subsets-list",
            "395-dataset.json",
        )

    elif dataset == "first-stratum":
        dataset_indices_file_path = os.path.join(
            current_script_path,
            "..",
            "training-data",
            "subsets-list",
            "30-106-subset.json",
        )

    elif dataset == "second-stratum":
        dataset_indices_file_path = os.path.join(
            current_script_path,
            "..",
            "training-data",
            "subsets-list",
            "30-395-subset.json",
        )

    else:
        raise NotSupportedError(f"Dataset {dataset} is not supported")

    with open(dataset_indices_file_path, "r") as f:
        dataset_indices = json.load(f)

    bugids = []
    for project_name, bugids_list in dataset_indices.items():
        for bugid in bugids_list:
            if project_name in exclude_projects:
                continue
            bugid_label = f"{project_name}:{bugid}"
            if bugid_label in IGNORED_BUGS:
                continue
            bugids.append(bugid_label)
            if test_mode:
                break

    return bugids
