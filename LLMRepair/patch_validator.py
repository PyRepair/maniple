import os
import subprocess
from utils import print_in_red


def validate_patches(bugid: str, output_dir: str):
    full_bugdir_path = os.path.join(output_dir, "-".join(bugid.split(":")))
    if not os.path.exists(full_bugdir_path):
        print_in_red(f"ERROR: {full_bugdir_path} does not exist")
        return
    
    # 0 pass test
    # 1 failed test
    # 2 invalid fix patch input for run custom patch (also include crash)
    # 4 run custom patch time out
    # 404 exteract fix patch = "" (response generation failed to pass parser)

    # subprocess.run(["bgp", "prep", "--bugids", bugid], check=True)

    for filename in os.listdir(full_bugdir_path):
        is_patchfile = "response" in filename and filename.endswith(".json")
        if not is_patchfile:
            continue

        patchfile_path = os.path.join(full_bugdir_path, filename)
        result_file_path = os.path.join(
            full_bugdir_path, filename.replace("response", "result")
        )
        error_log_path = os.path.join(
            full_bugdir_path,
            filename.replace("response", "log").replace(".json", ".txt"),
        )

        # subprocess.run(["bgp", "checkout_buggy", "--bugids", bugid], check=True)
        output = subprocess.run(
            ["run_custom_patch", patchfile_path, "--output-file", result_file_path],
            check=True,
            capture_output=True,
        )
        if output.stderr:
            with open(os.path.join(error_log_path), "w") as f:
                f.write(output.stderr.decode("utf-8"))
