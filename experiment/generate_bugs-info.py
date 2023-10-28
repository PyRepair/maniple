import argparse
import json
import os
from typing import Dict, List


def get_value(content: str) -> str:
    value = content.split("=")[1]
    return value[1:-2]


def extract_bugs_info(project_path: str, bug_id: int, project_link: str) -> Dict:
    with open(os.path.join(project_path, "bugs", str(bug_id), "bug.info")) as f:
        content = f.readlines()
        buggy_commit = get_value(content[1])
        fix_commit = get_value(content[2])
        test_file = get_value(content[3])

        bug_info = {
            "id": bug_id,
            "fix_commit_link": project_link + "/commit/" + fix_commit,
            "buggy_commit_link": project_link + "/commit/" + buggy_commit,
            "test_file": test_file,
        }

    return bug_info


def write_bugs_info(write_path: str, bugs_info: Dict):
    with open(write_path, "w") as f:
        json.dump(bugs_info, f, indent=4)


def extract_project_github_link(project_path: str) -> str:
    with open(os.path.join(project_path, "project.info")) as f:
        lines = f.readlines()
        return get_value(lines[0])


def match_project_dir(project_path_list: List[str], project_name: str) -> str:
    for path in project_path_list:
        if project_name in path.lower():
            return path


def main():
    parser = argparse.ArgumentParser(description="Create prompt and write result")
    parser.add_argument(
        "-d",
        "--database",
        help="Database name, should be a folder name under the database directory",
        type=str,
        required=True,
    )

    args = parser.parse_args()

    database = args.database
    bugs_data: Dict = json.load(
        open(
            os.path.join("..", "database", "subsets-list", f"{database}.json"),
            "r",
            encoding="utf-8",
        )
    )

    bgp_path = os.path.join(
        "..", "benchmarks", "PyRepair", "benchmarks", "BugsInPy", "projects"
    )
    project_path_list = [f.path for f in os.scandir(bgp_path) if f.is_dir()]

    bugs_info_path = os.path.join("..", "database", database, "bugs-info")
    os.makedirs(bugs_info_path, exist_ok=True)

    for project in bugs_data.keys():
        project_path = match_project_dir(project_path_list, project)
        project_link = extract_project_github_link(project_path)

        bugs_info = {"project": project, "project_link": project_link, "bugs": []}

        for bug_id in bugs_data[project]:
            bugs_info["bugs"].append(
                extract_bugs_info(project_path, bug_id, project_link)
            )

        write_bugs_info(os.path.join(bugs_info_path, f"{project}.json"), bugs_info)


if __name__ == "__main__":
    main()
