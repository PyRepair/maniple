import os
import shutil
from dataset_manager import (
    load_bugids_from_dataset,
    FIRST_STRATUM_PATH,
    SECOND_STRATUM_PATH,
)


def main():
    s1 = load_bugids_from_dataset("first-stratum", use_supported=True)
    for src_path, bugids in s1:
        for bugid in bugids:
            dest_path = os.path.join(FIRST_STRATUM_PATH, *bugid.split(":"))
            os.makedirs(dest_path, exist_ok=True)
            shutil.copytree(
                os.path.join(src_path, *bugid.split(":")),
                dest_path,
                dirs_exist_ok=True,
            )

    s2 = load_bugids_from_dataset("second-stratum", use_supported=True)
    for src_path, bugids in s2:
        for bugid in bugids:
            dest_path = os.path.join(SECOND_STRATUM_PATH, *bugid.split(":"))
            os.makedirs(dest_path, exist_ok=True)
            shutil.copytree(
                os.path.join(src_path, *bugid.split(":")),
                dest_path,
                dirs_exist_ok=True,
            )


if __name__ == "__main__":
    main()
