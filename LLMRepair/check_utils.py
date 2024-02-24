from pathlib import Path
from typing import List
import json
import numpy as np

def pass_at_k(n, c, k):
    """
    :param n: total number of samples
    :param c: number of correct samples
    :param k: k in pass@$k$
    """
    if n - c < k:
        return 1.0

    return 1.0 - np.prod(1.0 - k / np.arange(n - c + 1, n + 1))


def bugid_has_fix(bugid: str, bugid_folder: Path) -> bool:
    return bugid_patches(bugid, bugid_folder) != []


def bugid_patches(bugid: str, bugid_folder: Path) -> List[Path]:
    patches = []
    for file in bugid_folder.iterdir():
        if "result" in file.name and file.name.endswith(".json"):
            with open(file, "r") as json_file:
                result_data = json.load(json_file)

            first_key = list(result_data.keys())[0]
            first_value = result_data[first_key]

            if first_value == 0:
                patches.append(file)
    return patches
