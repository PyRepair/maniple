import copy
import json
import os.path
import random


def save_bitvector(filename: str, bitvector: dict):
    with open(filename, "w") as f:
        json.dump(bitvector, f, indent=4)


def generate_binary_codes(digit_length):
    all_codes = []
    for index in range(2 ** digit_length):
        all_codes.append([int(digit) for digit in bin(index)[2:].zfill(digit_length)])
    return all_codes


bitvector_map = {
    "1.1.1": 1,
    "1.1.2": 1,
    "1.3.1": 1,
    "1.3.2": 1,
    "1.4.1": 1,
    "1.2.1": 1,
    "1.4.2": 1,
    "1.2.2": 1,
    "1.5.1": 1,
    "1.5.2": 1,
    "2.1.1": 1,
    "2.1.2": 1,
    "2.2.1": 1,
    "2.2.2": 1,
    "2.3.1": 1,
    "2.3.2": 1,
    "3.1.1": 1,
    "3.1.2": 1,
    "cot": 1
}


strata_bitvector_map = {
    "1": {
        "1.1.1": 1,
        "1.1.2": 1,
        "1.2.1": 1,
        "1.2.2": 1
    },
    "2": {
        "1.3.1": 1,
        "1.3.2": 1
    },
    "3": {
        "1.4.2": 1,
        "1.4.1": 1
    },
    "4": {
        "1.5.1": 1,
        "1.5.2": 1,
    },
    "5": {
        "2.1.1": 1,
        "2.1.2": 1
    },
    "6": {
        "2.2.1": 1,
        "2.2.2": 1
    },
    "7": {
        "2.3.1": 1,
        "2.3.2": 1
    },
    "8": {
        "3.1.1": 1,
        "3.1.2": 1
    },
    "9": {
        "cot": 1
    }
}

if __name__ == "__main__":
    database_path = os.path.join("experiment-initialization-resources", "strata-bitvectors")

    if not os.path.exists(database_path):
        os.makedirs(database_path)


    # "traversal" or "random"
    mode = "traversal"
    random_num_samples = 5

    if mode == "random":
        for i in range(random_num_samples):
            strata_bitvector = copy.deepcopy(strata_bitvector_map)
            code = ""
            for fact_class in strata_bitvector.keys():
                if fact_class == "1" or fact_class == "9":
                    continue

                fact_strata: dict = strata_bitvector[fact_class]
                select = random.randint(0, 1)
                if select == 1:
                    for fact_label in fact_strata.keys():
                        fact_strata[fact_label] = 1
                else:
                    for fact_label in fact_strata.keys():
                        fact_strata[fact_label] = 0

                code += str(select)

            save_bitvector(os.path.join(database_path, f"{code}_bitvector.json"), strata_bitvector)

    else:
        num_of_optional_strata = 7
        codes = generate_binary_codes(num_of_optional_strata)

        for code in codes:
            strata_bitvector = copy.deepcopy(strata_bitvector_map)
            for index in range(len(code)):
                strata: dict = strata_bitvector[str(index + 2)]
                for fact in strata.keys():
                    strata[fact] = code[index]

            code_str = "1" + ''.join(map(str, code)) + "1"
            print(code_str)
            save_bitvector(os.path.join(database_path, f"{code_str}_bitvector.json"), strata_bitvector)
