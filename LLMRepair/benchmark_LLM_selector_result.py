from pathlib import Path
import pickle

from utils import print_in_red, print_in_yellow, iter_bugid_folders, pass_at_k


def is_this_bitvector_correct_helper(answers, six_digit_bitvector: str, project_name: str, bugid: int):
    # prepend 1 for source code bit placeholder
    # append 1 for COT technique bit placeholder
    query_bitvector = "1" + six_digit_bitvector + "1"

    projects_answer = answers.get(query_bitvector)
    if projects_answer is None:
        return False

    bugids_answer = projects_answer.get(project_name)
    if bugids_answer is None:
        return False

    return bugid in bugids_answer


def count_bitvector_success_trials(answers_list, six_digit_bitvector: str, project_name: str, bugid: int):
    success = 0
    for answers in answers_list:
        if is_this_bitvector_correct_helper(answers, six_digit_bitvector, project_name, bugid):
            success += 1
    return success


def main():
    with open("../logs/data.pkl", "rb") as f:
        answers_list = pickle.load(f)
        num_trials = len(answers_list)

    success_patches_counter = 0
    success_bugfix_counter = 0
    total_counter = 0

    bug_dir = Path.cwd().parent / "training-data" / "16-16-dataset-llm-feature-selector"
    for bugid, project_folder, bugid_folder in iter_bugid_folders(bug_dir):
        with open(bugid_folder / "bitvector.txt", "r") as bitvector_file:
            bitvector = bitvector_file.read().strip()

        success_count = count_bitvector_success_trials(
            answers_list,
            bitvector,
            project_folder.name,
            int(bugid_folder.name)
        )

        if success_count > 0:
            success_bugfix_counter += 1
        success_patches_counter += success_count
        total_counter += num_trials

    for k in range(1, 11):
        print_in_yellow(f"pass@{k}: {pass_at_k(total_counter, success_patches_counter, k)}")
    print_in_yellow(f"total fix patches: {success_patches_counter}")
    print_in_yellow(f"total bugfix: {success_bugfix_counter}")


if __name__ == '__main__':
    main()
