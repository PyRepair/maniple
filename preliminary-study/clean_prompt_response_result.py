import os

stratum_path = "../preliminary-study/first-stratum"
first_stratum_path = os.listdir(stratum_path)

for bug_dir in first_stratum_path:

    bug_path = os.path.join(stratum_path, bug_dir)
    responses_files = [path for path in os.listdir(bug_path) if "prompt" in path]

    for file in responses_files:
        file_path = os.path.join(bug_path, file)
        os.remove(file_path)
