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
    dataset: DatasetType,
    exclude_projects=[],
    include_projects=[],
    use_supported=True,
    test_mode=False,
):
    subset_list_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "..",
        "training-data",
        "subsets-list",
    )

    if dataset == "106subset":
        dataset_indices_file_path = os.path.join(
            subset_list_path,
            "106-dataset.json",
        )

    elif dataset == "395subset":
        dataset_indices_file_path = os.path.join(
            subset_list_path,
            "395-dataset.json",
        )

    elif dataset == "first-stratum":
        dataset_indices_file_path = os.path.join(
            subset_list_path,
            "30-106-subset.json",
        )

    elif dataset == "second-stratum":
        dataset_indices_file_path = os.path.join(
            subset_list_path,
            "30-395-subset.json",
        )

    else:
        raise NotSupportedError(f"Dataset {dataset} is not supported")

    with open(dataset_indices_file_path, "r") as f:
        dataset_indices = json.load(f)

    support_list = []
    with open(os.path.join(subset_list_path, "supported106.txt"), "r") as f:
        supported106 = f.read().strip().split(",")
        support_list.extend(supported106)
    with open(os.path.join(subset_list_path, "supported395.txt"), "r") as f:
        supported395 = f.read().strip().split(",")
        support_list.extend(supported395)

    print(f"Support list length: {len(support_list)}")

    bugids = []
    for project_name, bugids_list in dataset_indices.items():
        for bugid in bugids_list:
            if project_name in exclude_projects:
                continue
            if include_projects and project_name not in include_projects:
                continue

            bugid_label = f"{project_name}:{bugid}"
            if use_supported and bugid_label not in support_list:
                continue

            if bugid_label in IGNORED_BUGS:
                continue

            bugids.append(bugid_label)
            if test_mode:
                break

    return bugids
