import json
import os
from typing import Optional

from command_runner import (
    ensure_clone_and_prep_complete,
    run_prepare_command,
    run_validate_patch_command,
)
from maniple.utils.misc import print_in_green, print_in_red, print_in_yellow


def is_patch_file_ok(patchfile_path: str, result_file_path: str, bugid: str) -> bool:
    with open(patchfile_path) as f:
        patchfile = json.load(f)

    project_name = bugid.split(":")[0]

    replace_code = patchfile[project_name][0]["replace_code"]
    if replace_code is None:
        print_in_yellow(f"Patch {patchfile_path} is None, skip...")
        with open(result_file_path, "w") as f:
            json.dump({bugid: 6}, f, indent=4)
        return False

    if replace_code == "":
        print_in_yellow(f"Patch {patchfile_path} is empty, skip...")
        with open(result_file_path, "w") as f:
            json.dump({bugid: 7}, f, indent=4)
        return False

    return True


def run_validation_multiple_times(
    bugid: str,
    patchfile_path: str,
    result_file_path: str,
    timeout: int,
    envs_dir: Optional[str] = None,
    use_docker=False,
    overwrite=False,
    verbose_logging=False,
    times=3,
):
    running_status_success = True

    for i in range(times):
        if verbose_logging:
            print(f"Running validation {i + 1}...")

        # run validation
        result_status = run_validate_patch_command(
            bugid,
            patchfile_path,
            result_file_path,
            timeout,
            envs_dir,
            use_docker=use_docker,
            overwrite=overwrite,
            verbose_logging=verbose_logging,
        )
        running_status_success &= result_status

        with open(result_file_path) as f:
            patchfile = json.load(f)
        repair_status = patchfile[bugid]
        if repair_status != 0:
            break

    if running_status_success:
        print_in_green(f"Successfully validated patch for {result_file_path}")
    else:
        print_in_red(f"Failed to validate patch for {result_file_path}")


def validate_patches(
    bugid: str,
    bwd: str,
    envs_dir: Optional[str] = None,
    use_docker=False,
    overwrite=False,
    timeout=30,
    verbose_logging=False,
):
    """
    Result status code: (1-5 from pytest, 6-7 from LLMRepair)
    PyTest code 0: All tests were collected and passed successfully
    PyTest code 1: Tests were collected and run but some of the tests failed
    PyTest code 2: Test execution was interrupted by the user
    PyTest code 3: Internal error happened while executing tests
    PyTest code 4: pytest command line usage error
    PyTest code 5: No tests were collected
    LLMRepair code 6: fix patch is None
    LLMRepair code 7: fix patch is empty string
    code 8: Run custom patch exception (bug from Nikhil, see error log)
    """

    # assume bug has already been prepped
    for filename in os.listdir(bwd):
        # making sure that the input files are actually fine
        is_patchfile = "response" in filename and filename.endswith(".json")
        if not is_patchfile:
            continue

        patchfile_path = os.path.join(bwd, filename)
        if not os.path.exists(patchfile_path):
            continue

        result_file_path = os.path.join(bwd, filename.replace("response", "result"))
        if not is_patch_file_ok(patchfile_path, result_file_path, bugid):
            continue

        # ensure this bug is prepped
        if not ensure_clone_and_prep_complete(
            bugid, envs_dir, use_docker, overwrite=False
        ):
            continue

        # coordinate with Nihil, accuracy can only be ensured by running prepare command
        if not run_prepare_command(
            bugid,
            envs_dir,
            use_docker,
            overwrite=True,
            restart=False,
            verbose_logging=verbose_logging,
        ):
            continue

        # run validation
        run_validation_multiple_times(
            bugid,
            patchfile_path,
            result_file_path,
            timeout,
            envs_dir,
            use_docker=use_docker,
            overwrite=overwrite,
            verbose_logging=verbose_logging,
            times=get_run_times_for_bugid(bugid),
        )


def get_run_times_for_bugid(bugid: str):
    # projects_need_rerun = ["keras", "tqdm", "black", "PySnooper"]
    # if any(bugid.startswith(pn) for pn in projects_need_rerun):
    #     return 10
    # else:
    #     return 1

    # Update 8th Jan, 2024: Use 10 times for each bugs by default
    # This is because we have less bugs (16 + 16) to test and sufficient computing resources to verify results.
    
    return 10
