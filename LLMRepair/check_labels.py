import json
import os.path

dataset = ["16-100-dataset", "16-215-dataset"]
dataset_path = []
for dataset in dataset:
    dataset_path.append(os.path.join("..", "training-data", dataset))


def collect_result_table(target_trial: int):
    result_table = {}

    for path in dataset_path:
        for project in os.listdir(path):
            project_path = os.path.join(path, project)
            for bid in os.listdir(project_path):
                bug_path = os.path.join(project_path, bid)
                for file in os.listdir(bug_path):
                    file_path = os.path.join(bug_path, file)
                    if not ("response" in file_path and "json" in file_path):
                        continue

                    with open(file_path, "r") as response_file:
                        response_data = json.load(response_file)
                        bitvector = ""

                        for bit in response_data[project][0]["available_strata"].values():
                            bitvector += str(bit)

                    if int(file[file.rfind("_") + 1: file.rfind(".")]) != target_trial:
                        continue

                    if bitvector not in result_table:
                        result_table[bitvector] = {}

                    if project not in result_table[bitvector]:
                        result_table[bitvector][project] = []

                    result_file_path = file_path.replace("response", "result")

                    with open(result_file_path, "r") as result_file:
                        result_data = json.load(result_file)
                        label = next(iter(result_data.values()))

                        if label == 0:
                            result_table[bitvector][project].append(int(bid))

    return result_table


def merge_result_table(result_table_1: dict, result_table_2: dict):
    result_table = result_table_1.copy()
    for bitvector in result_table_1:
        for project in result_table_1[bitvector]:
            result_table[bitvector][project] = result_table_1[bitvector][project] + result_table_2[bitvector][project]

            result_table[bitvector][project] = list(set(result_table[bitvector][project]))

    return result_table


def calculate_result_table_size(result_table: dict):
    table_size = 0
    for projects in result_table.values():
        for bug_list in projects.values():
            table_size += len(bug_list)

    return table_size


for trial in range(1, 11):
    if trial == 1:
        aggregate_result = collect_result_table(1)
        size = calculate_result_table_size(aggregate_result)
        print(f"Positive label number after combine trial {trial}: {size}")
        continue

    next_trial_result = collect_result_table(trial)

    aggregate_result = merge_result_table(aggregate_result, next_trial_result)

    original_size = size

    size = calculate_result_table_size(aggregate_result)

    print(f"Positive label number after combine trial {trial}: {size}")
    print(f"Improve: {((size / original_size) * 100) - 100}%")
