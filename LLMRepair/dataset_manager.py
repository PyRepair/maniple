import json
from typing import List, Literal, Tuple, Union
import os

from utils import NotSupportedError

BGP100PATH = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "training-data",
        "106-dataset",
    )
)

BGP215PATH = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "training-data",
        "395-dataset",
    )
)

FIRST_STRATUM_PATH = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "training-data",
        "16-100-dataset",
    )
)

SECOND_STRATUM_PATH = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "training-data",
        "16-215-dataset",
    )
)

DatasetType = Union[
    Literal["BGP100"],
    Literal["BGP215"],
    Literal["first-stratum"],
    Literal["second-stratum"],
    Literal["all"],
]


def split_bugids_from_dataset(
    bugids: List[str],
    exclude_projects=[],
    include_projects=[],
) -> List[Tuple[str, List[str]]]:
    s1 = _load_bugids_from_dataset_impl(
        "BGP100",
        exclude_projects,
        include_projects,
    )
    s2 = _load_bugids_from_dataset_impl(
        "BGP215",
        exclude_projects,
        include_projects,
    )

    s1_results = []
    s2_results = []
    for bugid in bugids:
        if bugid in s1:
            s1_results.append(bugid)
        elif bugid in s2:
            s2_results.append(bugid)
        else:
            raise NotSupportedError(f"Bugid {bugid} is not supported")

    return [
        (
            BGP100PATH,
            s1_results,
        ),
        (
            BGP215PATH,
            s2_results,
        ),
    ]


def load_bugids_from_dataset(
    dataset: DatasetType,
    exclude_projects=[],
    include_projects=[],
) -> List[Tuple[str, List[str]]]:
    results = []

    if dataset == "BGP100":
        results.append(
            (
                BGP100PATH,
                _load_bugids_from_dataset_impl(
                    "BGP100",
                    exclude_projects=exclude_projects,
                    include_projects=include_projects,
                ),
            )
        )

    elif dataset == "BGP215":
        results.append(
            (
                BGP215PATH,
                _load_bugids_from_dataset_impl(
                    "BGP215",
                    exclude_projects=exclude_projects,
                    include_projects=include_projects,
                ),
            )
        )

    elif dataset == "first-stratum":
        results.append(
            (
                FIRST_STRATUM_PATH,
                _load_bugids_from_dataset_impl(
                    "first-stratum",
                    exclude_projects=exclude_projects,
                    include_projects=include_projects,
                ),
            )
        )

    elif dataset == "second-stratum":
        results.append(
            (
                SECOND_STRATUM_PATH,
                _load_bugids_from_dataset_impl(
                    "second-stratum",
                    exclude_projects=exclude_projects,
                    include_projects=include_projects,
                ),
            )
        )

    elif dataset == "all":
        results.append(
            (
                BGP100PATH,
                _load_bugids_from_dataset_impl(
                    "BGP100",
                    exclude_projects=exclude_projects,
                    include_projects=include_projects,
                ),
            )
        )
        results.append(
            (
                BGP215PATH,
                _load_bugids_from_dataset_impl(
                    "BGP215",
                    exclude_projects=exclude_projects,
                    include_projects=include_projects,
                ),
            )
        )

    return results


def _load_bugids_from_dataset_impl(
    dataset: DatasetType,
    exclude_projects=[],
    include_projects=[],
):
    subset_list_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "..",
        "experiment-initialization-resources",
        "datasets-list",
    )

    if dataset == "BGP100":
        dataset_indices_file_path = os.path.join(
            subset_list_path,
            "100-106-dataset.json",
        )

    elif dataset == "BGP215":
        dataset_indices_file_path = os.path.join(
            subset_list_path,
            "215-395-dataset.json",
        )

    elif dataset == "first-stratum":
        dataset_indices_file_path = os.path.join(
            subset_list_path,
            "16-100-dataset.json",
        )

    elif dataset == "second-stratum":
        dataset_indices_file_path = os.path.join(
            subset_list_path,
            "16-215-dataset.json",
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
            if include_projects and project_name not in include_projects:
                continue

            bugid_label = f"{project_name}:{bugid}"

            bugids.append(bugid_label)

    return bugids
