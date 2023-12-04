import json
import os
import subprocess
from utils import print_in_red, print_in_yellow


def validate_patches(bugid: str, bwd: str, flag_overwrite: bool = False):
    # 0 pass test
    # 1 failed test
    # 2 invalid fix patch input for run custom patch (also include crash)
    # 4 run custom patch time out
    # 404 exteract fix patch = "" (response generation failed to pass parser)

    if flag_overwrite:
        try:
            print_in_yellow(f"Preparing {bugid} before submitting patches...")
            subprocess.run(["bgp", "prep", "--bugids", bugid], check=True)
        except subprocess.CalledProcessError as e:
            print_in_red(e.stderr.decode("utf-8"))
            return

    for filename in os.listdir(bwd):
        is_patchfile = "response" in filename and filename.endswith(".json")
        if not is_patchfile:
            continue

        patchfile_path = os.path.join(bwd, filename)
        result_file_path = os.path.join(bwd, filename.replace("response", "result"))
        error_log_path = os.path.join(
            bwd,
            filename.replace("response", "log").replace(".json", ".txt"),
        )

        try:
            subprocess.run(
                ["run_custom_patch", patchfile_path, "--output-file", result_file_path],
                check=True,
                capture_output=True,
            )
        except subprocess.CalledProcessError as e:
            msg = e.stderr.decode("utf-8") + "\n" + e.stdout.decode("utf-8")
            with open(os.path.join(error_log_path), "w") as f:
                f.write(msg)
            with open(result_file_path, "w") as f:
                json.dump({bugid: 2}, f, indent=4)
