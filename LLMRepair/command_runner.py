import json
from multiprocessing.spawn import prepare
from optparse import Option
import subprocess
import os
from typing import Optional
from utils import print_in_yellow, print_in_red


def run_clone_command(
    bugid: str, envs_dir: Optional[str] = None, use_docker=False, overwrite=False
) -> bool:
    path_bugid_name = bugid.replace(":", "_")

    repo_dir = None
    if envs_dir is not None:
        repo_dir = os.path.join(envs_dir, "repos", path_bugid_name)
        if not overwrite and os.path.exists(repo_dir):
            print_in_yellow(f"Skipping cloning {bugid} because it already exists")
            return False

    print(f"Cloning {bugid}")

    try:
        if use_docker:
            command = ["docker", "run", "--rm", "-it"]
            if envs_dir is not None:
                command += ["-v", f"{envs_dir}:/envs"]
            command.append("pyr:lite")

            command += ["bgp", "clone", "--restart", "--bugids", bugid]
            if envs_dir is not None:
                command += ["--envs-dir", "/envs"]

        else:
            command = ["bgp", "clone", "--restart", "--bugids", bugid]
            if envs_dir is not None:
                command += ["--envs-dir", envs_dir]

        # Run the subprocess
        subprocess.run(command, capture_output=True, check=True)

    except KeyboardInterrupt:
        print("Ctrl+C pressed. Program exiting...")
        if repo_dir is not None:
            print_in_yellow(f"Warning: {repo_dir} may not be fully cloned")
        exit(0)

    except subprocess.CalledProcessError as e:
        print_in_red(f"Failed to clone {bugid}")
        with open(f"logs/{path_bugid_name}_clone_fail_log.txt", "w") as f:
            f.write(e.stdout.decode("utf-8") + e.stderr.decode("utf-8"))
        return False

    return True


def run_prepare_command(
    bugid: str, envs_dir: Optional[str] = None, use_docker=False, overwrite=False
) -> bool:
    path_bugid_name = bugid.replace(":", "_")

    prepare_env_dir = None
    if envs_dir is not None:
        prepare_env_dir = os.path.join(envs_dir, "envs", path_bugid_name)
        if not overwrite and os.path.exists(prepare_env_dir):
            print_in_yellow(f"Skipping preparing {bugid} because it already exists")
            return False

    print(f"Preparing {bugid}")

    try:
        # Start building the command
        if use_docker:
            command = ["docker", "run", "--rm", "-it"]
            if envs_dir is not None:
                command += ["-v", f"{envs_dir}:/envs"]
            command += ["pyr:lite", "bgp", "prep", "--restart", "--bugids", bugid]
            if envs_dir is not None:
                command += ["--envs-dir", "/envs"]
        else:
            command = ["bgp", "prep", "--restart", "--bugids", bugid]
            if envs_dir is not None:
                command += ["--envs-dir", envs_dir]

        # Run the subprocess
        output = subprocess.run(command, capture_output=True)

        all_output = output.stdout.decode("utf-8") + output.stderr.decode("utf-8")
        if "TestStatus.PASS" not in all_output:
            print_in_red(f"Failed to prepare {bugid}")
            with open(f"logs/{path_bugid_name}_prep_fail_log.txt", "w") as f:
                f.write(all_output)
            return False

    except KeyboardInterrupt:
        print("Ctrl+C pressed. Program exiting...")
        if prepare_env_dir is not None:
            print_in_yellow(f"Warning: {prepare_env_dir} may not be fully prepared")
        exit(0)

    return True


def ensure_clone_and_prep_complete(
    bugid: str, envs_dir: Optional[str] = None, use_docker=False, overwrite=False
) -> bool:
    r = run_clone_command(bugid, envs_dir, use_docker, overwrite)
    return r and run_prepare_command(bugid, envs_dir, use_docker, overwrite)


def run_extract_features_command(
    bugid: str,
    feature_json_path: str,
    envs_dir: Optional[str] = None,
    use_docker=False,
    overwrite=False,
) -> bool:
    if not overwrite and os.path.exists(feature_json_path):
        print_in_yellow(
            f"Skipping extracting features for {bugid} because it already exists"
        )
        return False

    try:
        if use_docker:
            command = ["docker", "run", "--rm", "-it"]
            if envs_dir is not None:
                command += ["-v", f"{envs_dir}:/envs"]
            command += ["pyr:lite", "bgp", "extract_features", "--bugids", bugid]
            if envs_dir is not None:
                command += ["--envs-dir", "/envs"]
        else:
            command = ["bgp", "extract_features", "--bugids", bugid]
            if envs_dir is not None:
                command += ["--envs-dir", envs_dir]

        # Adding feature-json argument for both scenarios
        command += ["--feature-json", feature_json_path]

        # Run the subprocess
        subprocess.run(command, capture_output=True, check=True)

    except KeyboardInterrupt:
        print_in_yellow(f"WARNING: {bugid} is interrupted")
        return False

    except subprocess.CalledProcessError as e:
        print_in_red(
            f"FATAL: bgp extract_features failed with error code {e.returncode}"
        )
        with open(f"{bugid}_extract_feature_error.log", "w") as f:
            f.write(e.stdout.decode("utf-8"))
        return False

    return True


def run_validate_patch_command(
    bugid: str,
    input_patch_json_path: str,
    output_result_json_path: str,
    envs_dir: Optional[str] = None,
    use_docker=False,
    overwrite=False,
) -> bool:
    if not overwrite and os.path.exists(output_result_json_path):
        print_in_yellow(
            f"Skipping validating patch for {bugid} because it already exists"
        )
        return False

    try:
        if use_docker:
            command = ["docker", "run", "--rm", "-it"]
            if envs_dir is not None:
                command += ["-v", f"{envs_dir}:/envs", "pyr:lite"]
            command += [
                "-v",
                f"{os.path.dirname(input_patch_json_path)}:/RUN_CUSTOM_PATCH_DIR",
            ]
            command += [
                "run_custom_patch",
                f"/RUN_CUSTOM_PATCH_DIR/{os.path.basename(input_patch_json_path)}",
            ]
            command += [
                "--output-file",
                f"/RUN_CUSTOM_PATCH_DIR/{os.path.basename(output_result_json_path)}",
            ]
            if envs_dir is not None:
                command += ["--envs-dir", "/envs"]
        else:
            command = ["run_custom_patch", input_patch_json_path]
            command += ["--output-file", output_result_json_path]
            if envs_dir is not None:
                command += ["--envs-dir", envs_dir]

        # Run the subprocess
        subprocess.run(command, check=True, capture_output=True)

    except KeyboardInterrupt:
        print_in_yellow(f"WARNING: {bugid} validation is interrupted")
        return False

    except subprocess.CalledProcessError as e:
        error_log_path = input_patch_json_path.replace("response", "log").replace(
            ".json", ".txt"
        )
        msg = e.stderr.decode("utf-8") + "\n" + e.stdout.decode("utf-8")
        with open(os.path.join(error_log_path), "w") as f:
            f.write(msg)
        with open(output_result_json_path, "w") as f:
            json.dump({bugid: 8}, f, indent=4)
        return False

    return True
