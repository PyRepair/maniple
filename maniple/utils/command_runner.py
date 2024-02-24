import json
import signal
import subprocess
import os
from typing import Optional
from maniple.utils.misc import print_in_green, print_in_yellow, print_in_red


def run_clone_command(
    bugid: str,
    envs_dir: Optional[str] = None,
    use_docker=False,
    overwrite=False,
    verbose_logging=False,
) -> bool:
    path_bugid_name = bugid.replace(":", "_")

    repo_dir = None
    if envs_dir is not None:
        envs_dir = os.path.abspath(envs_dir)
        repo_dir = os.path.join(envs_dir, "repos", path_bugid_name)
        if not overwrite and os.path.exists(repo_dir):
            if verbose_logging:
                print_in_yellow(f"Skipping cloning {bugid} because it already exists")
            return True

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

        if verbose_logging:
            print(f"Cloning {bugid} using command: '{' '.join(command)}'")

        # Run the subprocess
        subprocess.run(command, check=True)

    except subprocess.CalledProcessError as e:
        print_in_red(f"Failed to clone {bugid}")
        os.makedirs("logs", exist_ok=True)
        with open(f"logs/{path_bugid_name}_clone_fail_log.txt", "w") as f:
            f.write(e.stdout.decode("utf-8") + e.stderr.decode("utf-8"))
        return False

    return True


def run_prepare_command(
    bugid: str,
    envs_dir: Optional[str] = None,
    use_docker=False,
    overwrite=False,
    restart=True,
    verbose_logging=False,
) -> bool:
    path_bugid_name = bugid.replace(":", "_")

    prepare_env_dir = None
    if envs_dir is not None:
        envs_dir = os.path.abspath(envs_dir)
        prepare_env_dir = os.path.join(envs_dir, "envs", path_bugid_name)
        if not overwrite and os.path.exists(prepare_env_dir):
            if verbose_logging:
                print_in_yellow(f"Skipping preparing {bugid} because it already exists")
            return True

    # Start building the command
    if use_docker:
        command = ["docker", "run", "--rm", "-it"]
        if envs_dir is not None:
            command += ["-v", f"{envs_dir}:/envs"]
        command += ["pyr:lite", "bgp", "prep", "--bugids", bugid]
        if restart:
            command += ["--restart"]
        if envs_dir is not None:
            command += ["--envs-dir", "/envs"]
    else:
        command = ["bgp", "prep", "--bugids", bugid]
        if restart:
            command += ["--restart"]
        if envs_dir is not None:
            command += ["--envs-dir", envs_dir]

    if verbose_logging:
        print(f"Preparing {bugid} using command: '{' '.join(command)}'")

    # Run the subprocess
    output = subprocess.run(command, capture_output=True)

    all_output = output.stdout.decode("utf-8") + output.stderr.decode("utf-8")
    if "TestStatus.PASS" not in all_output:
        print_in_red(f"Failed to prepare {bugid}")
        os.makedirs("logs", exist_ok=True)
        with open(f"logs/{path_bugid_name}_prep_fail_log.txt", "w") as f:
            f.write(all_output)
        return False

    if restart:
        print_in_green(f"Successfully prepared {bugid}")

    return True


def ensure_clone_and_prep_complete(
    bugid: str,
    envs_dir: Optional[str] = None,
    use_docker=False,
    overwrite=False,
    verbose_logging=False,
) -> bool:
    if not run_clone_command(bugid, envs_dir, use_docker, overwrite, verbose_logging):
        return False

    return run_prepare_command(
        bugid,
        envs_dir,
        use_docker,
        overwrite,
        restart=True,
        verbose_logging=verbose_logging,
    )


def run_extract_features_command(
    bugid: str,
    feature_json_path: str,
    envs_dir: Optional[str] = None,
    use_docker=False,
    overwrite=False,
    verbose_logging=False,
) -> bool:
    if not overwrite and os.path.exists(feature_json_path):
        if verbose_logging:
            print_in_yellow(
                f"Skipping extracting features for {bugid} because it already exists"
            )
        return True

    if envs_dir is not None:
        envs_dir = os.path.abspath(envs_dir)
    feature_json_path = os.path.abspath(feature_json_path)

    try:
        if use_docker:
            command = ["docker", "run", "--rm", "-it"]
            if envs_dir is not None:
                command += ["-v", f"{envs_dir}:/envs"]
            command += ["-v", f"{os.path.dirname(feature_json_path)}:/RUN_FEATURE_DIR"]
            command += ["pyr:lite", "bgp", "extract_features", "--bugids", bugid]
            if envs_dir is not None:
                command += ["--envs-dir", "/envs"]
            command += [
                "--feature-json",
                f"/RUN_FEATURE_DIR/{os.path.basename(feature_json_path)}",
            ]
        else:
            command = ["bgp", "extract_features", "--bugids", bugid]
            if envs_dir is not None:
                command += ["--envs-dir", envs_dir]
            command += ["--feature-json", feature_json_path]

        if verbose_logging:
            print(
                f"Extracting features for {bugid} using command: '{' '.join(command)}'"
            )

        # Run the subprocess
        subprocess.run(command, capture_output=True, check=True)

    except subprocess.CalledProcessError as e:
        print_in_red(
            f"FATAL: bgp extract_features failed with error code {e.returncode}"
        )
        logpath = os.path.join(
            os.getcwd(), "logs", f"{bugid.replace(':', '_')}_extract_feature_error.txt"
        )
        with open(logpath, "w") as f:
            f.write(e.stdout.decode("utf-8"))
        return False

    return True


def run_validate_patch_command(
    bugid: str,
    input_patch_json_path: str,
    output_result_json_path: str,
    timeout: int,
    envs_dir: Optional[str] = None,
    use_docker=False,
    overwrite=False,
    verbose_logging=False,
) -> bool:
    if not overwrite and os.path.exists(output_result_json_path):
        if verbose_logging:
            print_in_yellow(
                f"Skipping validating patch for {bugid} because it already exists"
            )
        return True

    if envs_dir is not None:
        envs_dir = os.path.abspath(envs_dir)
    input_patch_json_path = os.path.abspath(input_patch_json_path)
    output_result_json_path = os.path.abspath(output_result_json_path)

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

    if verbose_logging:
        print(f"Validating patch for {bugid} using command: '{' '.join(command)}'")

    # Nikhil's approach, use native Popen to shutdown long process
    with subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, start_new_session=True
    ) as proc:
        try:
            stdout, stderr = proc.communicate(timeout=timeout)

            if proc.returncode != 0:
                error_log_path = input_patch_json_path.replace(
                    "response", "log"
                ).replace(".json", ".txt")
                msg = stderr.decode("utf-8") + "\n" + stdout.decode("utf-8")
                with open(os.path.join(error_log_path), "w") as f:
                    f.write(msg)

                with open(output_result_json_path, "w") as f:
                    json.dump({bugid: 8}, f, indent=4)

                return False

        except subprocess.TimeoutExpired:
            os.killpg(proc.pid, signal.SIGTERM)
            proc.communicate()

            print_in_red(f"Timeout for {input_patch_json_path}")
            with open(output_result_json_path, "w") as f:
                json.dump({bugid: 2}, f, indent=4)
            return False

    return True
