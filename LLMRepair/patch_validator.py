import json
import os
import subprocess
from utils import print_in_yellow


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


def validate_patches(bugid: str, bwd: str, flag_overwrite: bool = False):
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
        is_patchfile = "response" in filename and filename.endswith(".json")
        if not is_patchfile:
            continue

        patchfile_path = os.path.join(bwd, filename)
        if not os.path.exists(patchfile_path):
            continue

        result_file_path = os.path.join(bwd, filename.replace("response", "result"))
        if not is_patch_file_ok(patchfile_path, result_file_path, bugid):
            continue

        try:
            commands = (
                f"docker run --rm -it "
                + f"-v /Volumes/SSD2T/envs:/envs pyr:lite "
                + f"-v {os.path.dirname(result_file_path)}:/RUN_CUSTOM_PATCH_DIR "
                + f"run_custom_patch /RUN_CUSTOM_PATCH_DIR/{os.path.basename(patchfile_path)} "
                + f"--output-file /RUN_CUSTOM_PATCH_DIR{os.path.basename(result_file_path)} "
                + f"--separate-envs --envs-dir /envs"
            )
            commands = commands.split(" ")
            subprocess.run(
                commands,
                check=True,
                capture_output=True,
            )

        except subprocess.CalledProcessError as e:
            log_file_name = filename.replace("response", "log").replace(".json", ".txt")
            error_log_path = os.path.join(bwd, log_file_name)
            msg = e.stderr.decode("utf-8") + "\n" + e.stdout.decode("utf-8")
            with open(os.path.join(error_log_path), "w") as f:
                f.write(msg)
            with open(result_file_path, "w") as f:
                json.dump({bugid: 8}, f, indent=4)
