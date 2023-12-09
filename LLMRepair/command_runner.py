import json
import subprocess
import os
from utils import print_in_yellow, print_in_red


def run_clone_command(
    bugid: str, envs_dir: str, use_docker=False, overwrite=False
) -> bool:
    path_bugid_name = bugid.replace(":", "_")
    repo_dir = os.path.join(envs_dir, "repos", path_bugid_name)
    if not overwrite and os.path.exists(repo_dir):
        print_in_yellow(f"Skipping cloning {bugid} because it already exists")
        return False

    print(f"Cloning {bugid}")

    try:
        if use_docker:
            subprocess.run(
                (
                    f"docker run --rm -it -v {envs_dir}:/envs pyr:lite "
                    + f"bgp clone --restart --bugids {bugid} --envs-dir /envs"
                ).split(" "),
                capture_output=True,
                check=True,
            )
        else:
            cmd = f"bgp clone --restart --bugids {bugid} --envs-dir {envs_dir}"
            subprocess.run(
                cmd.split(" "),
                capture_output=True,
                check=True,
            )

    except KeyboardInterrupt:
        print("Ctrl+C pressed. Program exiting...")
        print_in_yellow(f"Warning: {repo_dir} may not be fully cloned")
        exit(0)

    except subprocess.CalledProcessError as e:
        print_in_red(f"Failed to clone {bugid}")
        with open(f"logs/{path_bugid_name}_clone_fail_log.txt", "w") as f:
            f.write(e.stdout.decode("utf-8") + e.stderr.decode("utf-8"))
        return False

    return True


def run_prepare_command(
    bugid: str, envs_dir: str, use_docker=False, overwrite=False
) -> bool:
    path_bugid_name = bugid.replace(":", "_")
    env_dir = os.path.join(envs_dir, "envs", path_bugid_name)
    if not overwrite and os.path.exists(env_dir):
        print_in_yellow(f"Skipping preparing {bugid} because it already exists")
        return False

    print(f"Preparing {bugid}")

    try:
        if use_docker:
            output = subprocess.run(
                (
                    f"docker run --rm -it -v {envs_dir}:/envs "
                    + f"pyr:lite bgp prep --restart --bugids {bugid} --envs-dir /envs"
                ).split(" "),
                capture_output=True,
            )
        else:
            output = subprocess.run(
                (f"bgp prep --restart --bugids {bugid} --envs-dir {envs_dir}").split(
                    " "
                ),
                capture_output=True,
            )

        all_output = output.stdout.decode("utf-8") + output.stderr.decode("utf-8")
        if "TestStatus.PASS" not in all_output:
            print_in_red(f"Failed to prepare {bugid}")
            with open(f"logs/{path_bugid_name}_prep_fail_log.txt", "w") as f:
                f.write(all_output)
            return False

    except KeyboardInterrupt:
        print("Ctrl+C pressed. Program exiting...")
        print_in_yellow(f"Warning: {env_dir} may not be fully prepared")
        exit(0)

    return True


def ensure_clone_and_prep_complete(
    bugid: str, envs_dir: str, use_docker=False, overwrite=False
) -> bool:
    r = run_clone_command(bugid, envs_dir, use_docker, overwrite)
    return r and run_prepare_command(bugid, envs_dir, use_docker, overwrite)


def run_extract_features_command(
    bugid: str, envs_dir: str, feature_json_path: str, use_docker=False, overwrite=False
) -> bool:
    if not overwrite and os.path.exists(feature_json_path):
        print_in_yellow(
            f"Skipping extracting features for {bugid} because it already exists"
        )
        return False

    try:
        if use_docker:
            subprocess.run(
                (
                    f"docker run --rm -it -v {envs_dir}:/envs pyr:lite "
                    + f"bgp extract_features --bugids {bugid} --envs-dir /envs "
                    + f"--feature-json {feature_json_path}"
                ).split(" "),
                capture_output=True,
                check=True,
            )
        else:
            subprocess.run(
                (
                    f"bgp extract_features --bugids {bugid} --envs-dir {envs_dir} "
                    + f"--feature-json {feature_json_path}"
                ).split(" "),
                capture_output=True,
                check=True,
            )

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
    envs_dir: str,
    input_patch_json_path: str,
    output_result_json_path: str,
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
            commands = (
                f"docker run --rm -it "
                + f"-v {envs_dir}:/envs pyr:lite "
                + f"-v {os.path.dirname(input_patch_json_path)}:/RUN_CUSTOM_PATCH_DIR "
                + f"run_custom_patch /RUN_CUSTOM_PATCH_DIR/{os.path.basename(input_patch_json_path)} "
                + f"--output-file /RUN_CUSTOM_PATCH_DIR{os.path.basename(output_result_json_path)} "
                + f"--envs-dir /envs"
            ).split(" ")
            subprocess.run(
                commands,
                check=True,
                capture_output=True,
            )
        else:
            commands = (
                f"run_custom_patch {input_patch_json_path} "
                + f"--output-file {output_result_json_path} "
                + f"--envs-dir {envs_dir}"
            ).split(" ")
            subprocess.run(
                commands,
                check=True,
                capture_output=True,
            )

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
